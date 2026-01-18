"""
Tests for SAP Pilot Kit - ICE-W Logger
"""
import sys
import json
import tempfile
import os
from pathlib import Path

# Add parent directory to path for imports
parent_path = Path(__file__).parent.parent
if str(parent_path) not in sys.path:
    sys.path.insert(0, str(parent_path))

from ice_w_logger import ICEWLogger


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
            log = logger.process_event(unstable_metrics)
        
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
        
        blocked = False
        for _ in range(50):
            log = logger.process_event(unstable_metrics)
            if log['autarchy']['action'] == "BLOCK_OUTPUT":
                blocked = True
                break
        
        assert blocked or logger.state == "INVALIDATED"

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
        """Test certificate generation."""
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
