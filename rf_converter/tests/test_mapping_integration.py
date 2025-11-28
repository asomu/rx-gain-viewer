"""
Integration tests for Band Mapping System

Tests end-to-end CSV generation with band notation mapping.
"""

import unittest
import json
import tempfile
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.band_mapper import BandMapper
from core.parsers.rx_parser import RxGainParser
import pandas as pd
import numpy as np


class TestBandMappingIntegration(unittest.TestCase):
    """Integration tests for band mapping feature"""

    def setUp(self):
        """Reset singleton and create test environment"""
        BandMapper.reset_instance()
        self.mapper = BandMapper.get_instance()
        self.parser = RxGainParser()
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up temporary files"""
        for file in self.temp_dir.glob("*"):
            if file.is_file():
                file.unlink()
        self.temp_dir.rmdir()

    def create_test_s_params_df(self):
        """Create test S-parameter DataFrame"""
        return pd.DataFrame({
            'frequency': [2600.0, 2650.0, 2690.0],
            'S21_re': [0.5, 0.6, 0.55],
            'S21_im': [0.1, 0.15, 0.12],
            'S12_re': [0.01, 0.015, 0.012],
            'S12_im': [0.001, 0.0015, 0.0012],
            'S11_re': [0.1, 0.12, 0.11],
            'S11_im': [0.05, 0.06, 0.055],
            'S22_re': [0.08, 0.09, 0.085],
            'S22_im': [0.04, 0.045, 0.042]
        })

    def create_test_mapping_file(self, mappings):
        """Create temporary JSON mapping file"""
        data = {
            "version": "1.0",
            "description": "Test integration mappings",
            "mappings": mappings
        }
        file_path = self.temp_dir / "test_mapping.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return file_path

    # ========== Integration Tests ==========

    def test_csv_generation_with_mapping(self):
        """Test complete CSV generation with band mapping enabled"""
        # Setup mapping
        mappings = {
            "B41[CN]": "34_39+41",
            "B41[SA]": "41",
            "B41[NA]": "25_30_66+41"
        }
        mapping_file = self.create_test_mapping_file(mappings)
        self.mapper.load_mapping(mapping_file)

        # Create metadata
        metadata = {
            'band': 'B41',
            'ca_config': 'B41[CN]',
            'port_in': 'ANT1',
            'port_out': 'RXOUT1',
            'lna_state': 'G0_H'
        }

        # Generate CSV data
        s_params_df = self.create_test_s_params_df()
        result_df = self.parser.calculate_metrics(s_params_df, metadata, mapper=self.mapper)

        # Verify columns exist
        self.assertIn('ca_config', result_df.columns, "Should have ca_config column")
        self.assertIn('debug-nplexer_bank', result_df.columns, "Should have debug-nplexer_bank column")

        # Verify mapping was applied
        self.assertEqual(result_df['ca_config'].iloc[0], 'B41[CN]', "ca_config should be original")
        self.assertEqual(result_df['debug-nplexer_bank'].iloc[0], '34_39+41', "Should be mapped value")

        # Verify all rows have same mapping
        self.assertTrue(all(result_df['ca_config'] == 'B41[CN]'))
        self.assertTrue(all(result_df['debug-nplexer_bank'] == '34_39+41'))

    def test_csv_generation_without_mapping(self):
        """Test CSV generation with mapping disabled (mapper=None)"""
        # Create metadata
        metadata = {
            'band': 'B41',
            'ca_config': 'B41[CN]',
            'port_in': 'ANT1',
            'port_out': 'RXOUT1',
            'lna_state': 'G0_H'
        }

        # Generate CSV data without mapper
        s_params_df = self.create_test_s_params_df()
        result_df = self.parser.calculate_metrics(s_params_df, metadata, mapper=None)

        # Verify columns exist
        self.assertIn('ca_config', result_df.columns)
        self.assertIn('debug-nplexer_bank', result_df.columns)

        # Verify no mapping was applied
        self.assertEqual(result_df['ca_config'].iloc[0], 'B41[CN]', "ca_config should be original")
        self.assertEqual(result_df['debug-nplexer_bank'].iloc[0], '', "Should be empty without mapper")

    def test_csv_generation_unmapped_band(self):
        """Test CSV generation when band is not in mapping file"""
        # Setup mapping without B1
        mappings = {
            "B41[CN]": "34_39+41"
        }
        mapping_file = self.create_test_mapping_file(mappings)
        self.mapper.load_mapping(mapping_file)

        # Create metadata for B1 (not in mapping)
        metadata = {
            'band': 'B1',
            'ca_config': 'B1',
            'port_in': 'ANT1',
            'port_out': 'RXOUT1',
            'lna_state': 'G0_H'
        }

        # Generate CSV data
        s_params_df = self.create_test_s_params_df()
        result_df = self.parser.calculate_metrics(s_params_df, metadata, mapper=self.mapper)

        # Verify pass-through behavior (original value when not mapped)
        self.assertEqual(result_df['ca_config'].iloc[0], 'B1', "ca_config should be original")
        self.assertEqual(result_df['debug-nplexer_bank'].iloc[0], 'B1', "Should pass through original value")

        # Verify missing key was tracked
        missing_keys = self.mapper.get_missing_keys()
        self.assertIn('B1', missing_keys, "Should track missing key")

    def test_multiple_bands_mapping(self):
        """Test CSV generation with multiple different bands"""
        # Setup comprehensive mapping
        mappings = {
            "B1": "TM01_A",
            "B3": "TM03_A",
            "B41[CN]": "34_39+41",
            "B41[NA]": "25_30_66+41"
        }
        mapping_file = self.create_test_mapping_file(mappings)
        self.mapper.load_mapping(mapping_file)

        # Test each band
        test_cases = [
            ("B1", "B1", "TM01_A"),
            ("B3", "B3", "TM03_A"),
            ("B41", "B41[CN]", "34_39+41"),
            ("B41", "B41[NA]", "25_30_66+41"),
        ]

        for band, ca_config, expected_mapped in test_cases:
            metadata = {
                'band': band,
                'ca_config': ca_config,
                'port_in': 'ANT1',
                'port_out': 'RXOUT1',
                'lna_state': 'G0_H'
            }

            s_params_df = self.create_test_s_params_df()
            result_df = self.parser.calculate_metrics(s_params_df, metadata, mapper=self.mapper)

            self.assertEqual(result_df['ca_config'].iloc[0], ca_config, f"ca_config for {ca_config}")
            self.assertEqual(result_df['debug-nplexer_bank'].iloc[0], expected_mapped, f"mapping for {ca_config}")

    def test_backward_compatibility(self):
        """Test that existing code works without mapper parameter"""
        # Create metadata
        metadata = {
            'band': 'B41',
            'ca_config': 'B41[CN]',
            'port_in': 'ANT1',
            'port_out': 'RXOUT1',
            'lna_state': 'G0_H'
        }

        # Call without mapper parameter (backward compatibility)
        s_params_df = self.create_test_s_params_df()
        result_df = self.parser.calculate_metrics(s_params_df, metadata)

        # Should work without error and have empty debug-nplexer_bank
        self.assertIn('debug-nplexer_bank', result_df.columns)
        self.assertEqual(result_df['debug-nplexer_bank'].iloc[0], '')


if __name__ == '__main__':
    unittest.main()
