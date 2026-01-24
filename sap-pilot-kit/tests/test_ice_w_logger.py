"""
Tests for SAP Pilot Kit - ICE-W Logger
"""
import json
import tempfile
import os

from sap_pilot_kit.ice_w_logger import ICEWLogger


class TestICEWLogger:
    """Test suite for ICEWLogger class."""

    def test_logger_initialization(self):
        """Test that logger initializes correctly."""
        logger = ICEWLogger("TEST-001", "abc123")
        
        assert logger.artifact_id == "TEST-001"
        assert logger.sha256 == "abc123"
        assert logger.state == "SOVEREIGN"
        assert not logger.is_blocked
        assert logger.k_counter == 0
        assert logger.m_counter == 0
        assert logger.p_counter == 0

    def test_calculate_coherence(self):
        """Test coherence calculation from metrics."""
        logger = ICEWLogger("TEST-001", "abc123")
        
        metrics = {
            'semantic_stability': 0.8,
            'output_stability': 0.9,
            'constraint_compliance': 1.0,
            'decision_entropy': 0.1  # Low entropy = high coherence
        }
        
        cn = logger.calculate_coherence(metrics)
        # Expected: (0.8 + 0.9 + 1.0 + 0.9) / 4 = 0.9
        assert 0.89 <= cn <= 0.91

    def test_process_event_sovereign(self):
        """Test processing event in SOVEREIGN state."""
        logger = ICEWLogger("TEST-001", "abc123")
        
        metrics = {
            'semantic_stability': 0.98,
            'output_stability': 0.99,
            'constraint_compliance': 1.0,
            'decision_entropy': 0.05
        }
        
        log = logger.process_event(metrics)
        
        assert log['schema_version'] == "SAP-Telemetry-0.1"
        assert log['artifact']['id'] == "TEST-001"
        assert log['event']['state'] == "SOVEREIGN"
        assert log['autarchy']['action'] == "ALLOW"
        assert 'cn' in log['metrics']

    def test_state_transition_to_degraded(self):
        """Test state transition from SOVEREIGN to DEGRADED."""
        logger = ICEWLogger("TEST-001", "abc123")
        
        # Build up window with stable events
        stable_metrics = {
            'semantic_stability': 0.98,
            'output_stability': 0.99,
            'constraint_compliance': 1.0,
            'decision_entropy': 0.05
        }
        for _ in range(15):
            logger.process_event(stable_metrics)
        
        # Now introduce unstable events
        unstable_metrics = {
            'semantic_stability': 0.4,
            'output_stability': 0.4,
            'constraint_compliance': 0.1,
            'decision_entropy': 0.9
        }
        
        # Process several unstable events to trigger state change
        for _ in range(10):
            logger.process_event(unstable_metrics)
        
        # Should eventually transition to DEGRADED or INVALIDATED
        assert logger.state in ["DEGRADED", "INVALIDATED"]

    def test_output_blocking(self):
        """Test that output gets blocked when INVALIDATED."""
        logger = ICEWLogger("TEST-001", "abc123")
        
        # Build baseline
        stable_metrics = {
            'semantic_stability': 0.98,
            'output_stability': 0.99,
            'constraint_compliance': 1.0,
            'decision_entropy': 0.05
        }
        for _ in range(15):
            logger.process_event(stable_metrics)
        
        # Apply extreme stress
        unstable_metrics = {
            'semantic_stability': 0.1,
            'output_stability': 0.1,
            'constraint_compliance': 0.0,
            'decision_entropy': 0.95
        }
        
        for _ in range(50):
            log = logger.process_event(unstable_metrics)
            if log['autarchy']['action'] == "BLOCK_OUTPUT":
                break
        
        # Per SAP protocol: when INVALIDATED, output must be blocked
        assert logger.state == "INVALIDATED"
        assert logger.is_blocked

    def test_telemetry_log_accumulation(self):
        """Test that telemetry log accumulates events."""
        logger = ICEWLogger("TEST-001", "abc123")
        
        metrics = {
            'semantic_stability': 0.9,
            'output_stability': 0.9,
            'constraint_compliance': 0.9,
            'decision_entropy': 0.1
        }
        
        for _ in range(5):
            logger.process_event(metrics)
        
        assert len(logger.telemetry_log) == 5

    def test_export_telemetry(self):
        """Test exporting telemetry to JSON."""
        logger = ICEWLogger("TEST-001", "abc123")
        
        metrics = {
            'semantic_stability': 0.9,
            'output_stability': 0.9,
            'constraint_compliance': 0.9,
            'decision_entropy': 0.1
        }
        logger.process_event(metrics)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            logger.export_telemetry(temp_path)
            
            with open(temp_path, 'r') as f:
                data = json.load(f)
            
            assert isinstance(data, list)
            assert len(data) == 1
            assert data[0]['artifact']['id'] == "TEST-001"
        finally:
            os.unlink(temp_path)

    def test_generate_certificate(self):
        """Test certificate generation (dict only)."""
        logger = ICEWLogger("TEST-001", "abc123")
        
        metrics = {
            'semantic_stability': 0.9,
            'output_stability': 0.9,
            'constraint_compliance': 0.9,
            'decision_entropy': 0.1
        }
        logger.process_event(metrics)
        
        cert = logger.generate_certificate()
        
        assert 'certificate_id' in cert
        assert 'issue_date' in cert
        assert cert['artifact_id'] == "TEST-001"
        assert cert['sha256'] == "abc123"
        # Validate result field based on is_blocked state
        assert 'result' in cert
        assert cert['result'] in ["PASSED (BLOCKED)", "FAILED"]

    def test_full_state_cycle(self):
        """
        Test the full state cycle:
        SOVEREIGN -> DEGRADED -> INVALIDATED -> Recovery -> SOVEREIGN
        """
        logger = ICEWLogger("TEST-CYCLE", "hash")
        # Ensure we can control thresholds
        logger.W_size = 5 # Small window for faster drift detection
        logger.k_limit = 2
        logger.m_limit = 3
        logger.p_recovery = 5

        # 1. Fill window with stable events (Cn ~ 1.0)
        stable = {
            'semantic_stability': 1.0,
            'output_stability': 1.0,
            'constraint_compliance': 1.0,
            'decision_entropy': 0.0
        }
        for _ in range(10):
            logger.process_event(stable)
        assert logger.state == "SOVEREIGN"

        # 2. Trigger drift -> DEGRADED
        # A low score will cause high delta_cn against the stable window
        unstable = {
            'semantic_stability': 0.0,
            'output_stability': 0.0,
            'constraint_compliance': 0.0,
            'decision_entropy': 1.0
        } # Cn = 0.0

        # Violations count up to k_limit (2)
        logger.process_event(unstable) # k=1
        logger.process_event(unstable) # k=2 -> DEGRADED
        assert logger.state == "DEGRADED"

        # 3. Trigger INVALIDATED
        # Violations count up to m_limit (3) while in DEGRADED
        logger.process_event(unstable) # m=1
        logger.process_event(unstable) # m=2
        logger.process_event(unstable) # m=3 -> INVALIDATED
        assert logger.state == "INVALIDATED"
        assert logger.is_blocked

        # 4. Recovery
        # Process p_recovery (5) stable events.
        # We need to feed enough stable events until window stabilizes and we stop crossing threshold.
        # Then p_counter will start counting.

        recovered = False
        for _ in range(50):
            logger.process_event(stable)
            if logger.state == "SOVEREIGN":
                recovered = True
                break

        assert recovered
        assert logger.state == "SOVEREIGN"
        assert not logger.is_blocked

    def test_generate_certificate_markdown(self):
        """Test generating a markdown certificate with mocked file I/O."""
        logger = ICEWLogger("TEST-MD", "hash")

        # Mock os.path.exists to return True for template
        with patch('os.path.exists') as mock_exists, \
             patch('builtins.open', mock_open(read_data="Template: [CERT_ID] [STATUS]")) as mock_file:

            mock_exists.return_value = True

            cert = logger.generate_certificate("output.md")

            # Check if file was opened for writing
            mock_file.assert_called_with("output.md", 'w', encoding='utf-8')

            # Check content written (simplified check)
            handle = mock_file()
            handle.write.assert_called()
            args, _ = handle.write.call_args
            content = args[0]
            assert "Template: CERT-SAP-" in content
            assert "SOVEREIGN" in content or "FAILED" in content

    def test_generate_certificate_json_file(self):
        """Test generating a JSON certificate file."""
        logger = ICEWLogger("TEST-JSON", "hash")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            logger.generate_certificate(temp_path)

            with open(temp_path, 'r') as f:
                data = json.load(f)

            assert data['artifact_id'] == "TEST-JSON"
        finally:
            os.unlink(temp_path)

    def test_generate_certificate_missing_template(self):
        """Test generating MD when template is missing."""
        logger = ICEWLogger("TEST-NO-TMPL", "hash")

        with patch('os.path.exists') as mock_exists, \
             patch('builtins.print') as mock_print:

            mock_exists.return_value = False # Template not found

            logger.generate_certificate("output.md")

            # Check if print was called with a warning message
            assert mock_print.called
            args, _ = mock_print.call_args
            assert args[0].startswith("Warning: Template not found at")

    def test_recovery_logic_direct(self):
        """
        Directly test the recovery logic block (lines 166-181 approx).
        """
        logger = ICEWLogger("TEST-RECOVERY", "hash")
        logger.state = "INVALIDATED"
        logger.is_blocked = True
        logger.p_recovery = 3

        # 1. crossed = True -> reset p_counter
        logger.p_counter = 2
        logger._update_state(crossed=True)
        assert logger.p_counter == 0
        assert logger.state == "INVALIDATED"

        # 2. crossed = False -> increment p_counter
        logger._update_state(crossed=False) # p=1
        assert logger.p_counter == 1

        logger._update_state(crossed=False) # p=2
        assert logger.p_counter == 2

        logger._update_state(crossed=False) # p=3 -> Recovery!
        assert logger.state == "SOVEREIGN"
        assert logger.p_counter == 0
        assert logger.m_counter == 0
        assert logger.k_counter == 0
        assert not logger.is_blocked

    def test_recovery_from_degraded(self):
        """
        Test recovery from DEGRADED state back to SOVEREIGN
        before hitting INVALIDATED.
        """
        logger = ICEWLogger("TEST-RECOV-DEG", "hash")
        logger.k_limit = 2

        # 1. Go to DEGRADED
        # k=1
        logger._update_state(crossed=True)
        # k=2 -> DEGRADED
        logger._update_state(crossed=True)
        assert logger.state == "DEGRADED"

        # Now we are in DEGRADED. m_counter logic:
        # When entering DEGRADED, m_counter is incremented.

        # If we get a stable event:
        logger._update_state(crossed=False)
        # m_counter decrements.
        # state becomes SOVEREIGN if m_counter hits 0.

        assert logger.state == "SOVEREIGN"


class TestSAPParameters:
    """Test SAP protocol parameters."""

    def test_default_parameters(self):
        """Test default SAP parameters."""
        logger = ICEWLogger("TEST-001", "abc123")
        
        assert logger.W_size == 100
        assert logger.sigma == 0.73
        assert logger.k_limit == 3
        assert logger.m_limit == 10
        assert logger.p_recovery == 50
