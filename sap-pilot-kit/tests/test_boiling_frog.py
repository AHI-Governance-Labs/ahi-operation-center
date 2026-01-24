"""
Tests for SAP Pilot Kit - Boiling Frog Tester
"""
from unittest.mock import patch
from sap_pilot_kit.boiling_frog_tester import simulate_stress_test

def test_simulate_stress_test():
    """
    Test the boiling frog simulation script.
    Mocks time.sleep to ensure fast execution.
    Mocks print to silence output.
    Mocks generate_certificate to avoid file creation.
    """
    with patch('time.sleep'), \
         patch('builtins.print'), \
         patch('sap_pilot_kit.ice_w_logger.ICEWLogger.generate_certificate') as mock_gen_cert:

        simulate_stress_test()

        # Verify that it completed and attempted to generate a certificate
        # The script is designed to fail (block output) at some level.
        assert mock_gen_cert.called
