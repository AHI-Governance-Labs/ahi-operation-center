"""
Tests for SAP Pilot Kit - ICE-W Logger
"""
import json
import tempfile
import os

import pytest
from sap_pilot_kit.ice_w_logger import ICEWLogger


class TestICEWLogger:
    """Test suite for ICEWLogger class."""

    VALID_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    def test_logger_initialization(self):
        """Test that logger initializes correctly."""
        logger = ICEWLogger("TEST-001", self.VALID_HASH)
        
        assert logger.artifact_id == "TEST-001"
        assert logger.sha256 == self.VALID_HASH
        assert logger.state == "SOVEREIGN"
        assert not logger.is_blocked
        assert logger.k_counter == 0
        assert logger.m_counter == 0
        assert logger.p_counter == 0

    def test_logger_initialization_validation(self):
        """Test that logger validates inputs."""
        # Invalid artifact_id (contains special characters)
        with pytest.raises(ValueError, match="Invalid artifact_id"):
            ICEWLogger("TEST<script>", self.VALID_HASH)

        # Invalid sha256 (too short)
        with pytest.raises(ValueError, match="Invalid sha256"):
            ICEWLogger("TEST-001", "short_hash")

        # Invalid sha256 (non-hex)
        with pytest.raises(ValueError, match="Invalid sha256"):
            ICEWLogger("TEST-001", "g" * 64)

    def test_calculate_coherence(self):
        """Test coherence calculation from metrics."""
        logger = ICEWLogger("TEST-001", self.VALID_HASH)
        
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
        logger = ICEWLogger("TEST-001", self.VALID_HASH)
        
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
        logger = ICEWLogger("TEST-001", self.VALID_HASH)
        
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
        logger = ICEWLogger("TEST-001", self.VALID_HASH)
        
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
        logger = ICEWLogger("TEST-001", self.VALID_HASH)
        
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
        logger = ICEWLogger("TEST-001", self.VALID_HASH)
        
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
            
            assert isinstance(data, dict)
            assert "epoch_summaries" in data
            assert "current_window" in data
            assert len(data["current_window"]) == 1
            assert data["current_window"][0]['artifact']['id'] == "TEST-001"
        finally:
            os.unlink(temp_path)

    def test_retention_policy(self):
        """Test that telemetry log is compacted when it reaches the limit."""
        logger = ICEWLogger("TEST-001", self.VALID_HASH)
        # Lower limit for testing
        logger.max_log_size = 50

        metrics = {
            'semantic_stability': 0.9,
            'output_stability': 0.9,
            'constraint_compliance': 0.9,
            'decision_entropy': 0.1
        }

        # Add 50 events (limit is 50)
        for _ in range(50):
            logger.process_event(metrics)

        assert len(logger.telemetry_log) == 50
        assert len(logger.epoch_summaries) == 0

        # 51st event triggers compaction
        logger.process_event(metrics)

        assert len(logger.telemetry_log) == 1
        assert len(logger.epoch_summaries) == 1

        summary = logger.epoch_summaries[0]
        assert summary['event_count'] == 50
        assert summary['metrics']['cn_avg'] > 0.8

    def test_generate_certificate(self):
        """Test certificate generation."""
        logger = ICEWLogger("TEST-001", self.VALID_HASH)
        
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
        assert cert['sha256'] == self.VALID_HASH
        # Validate result field based on is_blocked state
        assert 'result' in cert
        assert cert['result'] in ["PASSED (BLOCKED)", "FAILED"]

    def test_generate_certificate_file_content(self):
        """Test that certificate file is generated with correct content."""
        logger = ICEWLogger("TEST-CERT", self.VALID_HASH)

        # Add an event to have some data
        logger.process_event({
            'semantic_stability': 0.9,
            'output_stability': 0.9,
            'constraint_compliance': 0.9,
            'decision_entropy': 0.1
        })

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            temp_path = f.name

        try:
            logger.generate_certificate(temp_path)

            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Verify placeholders were replaced
            assert "TEST-CERT" in content
            assert self.VALID_HASH in content
            # cert_id uses artifact_id[:8]
            assert "CERT-SAP-2026-TEST-CER" in content
            # Ensure no raw placeholders remain
            assert "{CERT_ID}" not in content
            assert "{DATE}" not in content

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestSAPParameters:
    """Test SAP protocol parameters."""

    def test_default_parameters(self):
        """Test default SAP parameters."""
        valid_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        logger = ICEWLogger("TEST-001", valid_hash)
        
        assert logger.W_size == 100
        assert logger.sigma == 0.73
        assert logger.k_limit == 3
        assert logger.m_limit == 10
        assert logger.p_recovery == 50
