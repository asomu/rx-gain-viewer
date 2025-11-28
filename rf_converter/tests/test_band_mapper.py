"""
Unit tests for BandMapper class

Tests cover:
- Singleton pattern
- File loading (success/failure scenarios)
- Mapping lookup behavior
- Error handling
- Missing key warnings
- Metadata extraction
"""

import unittest
import json
import tempfile
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.band_mapper import BandMapper


class TestBandMapper(unittest.TestCase):
    """Test suite for BandMapper class"""

    def setUp(self):
        """Reset singleton before each test"""
        BandMapper.reset_instance()
        self.mapper = BandMapper.get_instance()
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up temporary files"""
        for file in self.temp_dir.glob("*"):
            if file.is_file():
                file.unlink()
        self.temp_dir.rmdir()

    def create_temp_mapping_file(self, data):
        """Helper to create temporary JSON mapping file"""
        temp_file = self.temp_dir / "test_mapping.json"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return temp_file

    # ========== Singleton Pattern Tests ==========

    def test_singleton_pattern(self):
        """Test that BandMapper is a singleton"""
        mapper1 = BandMapper.get_instance()
        mapper2 = BandMapper.get_instance()
        self.assertIs(mapper1, mapper2, "Should return same instance")

    def test_singleton_reset(self):
        """Test singleton reset (for testing only)"""
        mapper1 = BandMapper.get_instance()
        BandMapper.reset_instance()
        mapper2 = BandMapper.get_instance()
        self.assertIsNot(mapper1, mapper2, "Should return new instance after reset")

    # ========== File Loading Success Tests ==========

    def test_load_valid_mapping_file(self):
        """Test loading a valid mapping file"""
        data = {
            "version": "1.0",
            "description": "Test mappings",
            "mappings": {
                "B1": "TM01_A",
                "B41[CN]": "34_39+41"
            }
        }
        file_path = self.create_temp_mapping_file(data)

        success, message = self.mapper.load_mapping(file_path)

        self.assertTrue(success, "Should load successfully")
        self.assertIn("2 mappings", message, "Should report correct count")
        self.assertTrue(self.mapper.is_loaded())
        self.assertEqual(len(self.mapper), 2)

    def test_load_comprehensive_mapping(self):
        """Test loading mapping with many entries"""
        mappings = {f"B{i}": f"TM{i:02d}_A" for i in range(1, 51)}
        data = {
            "version": "1.0",
            "mappings": mappings
        }
        file_path = self.create_temp_mapping_file(data)

        success, message = self.mapper.load_mapping(file_path)

        self.assertTrue(success)
        self.assertEqual(len(self.mapper), 50)

    def test_load_with_metadata(self):
        """Test loading file with metadata fields"""
        data = {
            "version": "1.0",
            "description": "Alpha-1C EVB#1 mappings",
            "project": "Alpha-1C",
            "created_date": "2025-11-27",
            "mappings": {
                "B41[CN]": "34_39+41"
            }
        }
        file_path = self.create_temp_mapping_file(data)

        success, _ = self.mapper.load_mapping(file_path)

        self.assertTrue(success)
        metadata = self.mapper.get_metadata()
        self.assertEqual(metadata['description'], "Alpha-1C EVB#1 mappings")
        self.assertEqual(metadata['project'], "Alpha-1C")
        self.assertEqual(metadata['created_date'], "2025-11-27")

    # ========== File Loading Failure Tests ==========

    def test_load_nonexistent_file(self):
        """Test loading a file that doesn't exist"""
        fake_path = self.temp_dir / "nonexistent.json"

        success, message = self.mapper.load_mapping(fake_path)

        self.assertFalse(success, "Should fail for nonexistent file")
        self.assertIn("not found", message.lower())
        self.assertFalse(self.mapper.is_loaded())
        self.assertEqual(len(self.mapper), 0)

    def test_load_invalid_extension(self):
        """Test loading a file with invalid extension"""
        temp_file = self.temp_dir / "test.txt"
        temp_file.write_text("{}", encoding='utf-8')

        success, message = self.mapper.load_mapping(temp_file)

        self.assertFalse(success, "Should fail for non-JSON file")
        self.assertIn("Invalid file type", message)
        self.assertFalse(self.mapper.is_loaded())

    def test_load_invalid_json(self):
        """Test loading a file with invalid JSON"""
        temp_file = self.temp_dir / "invalid.json"
        temp_file.write_text("{ invalid json }", encoding='utf-8')

        success, message = self.mapper.load_mapping(temp_file)

        self.assertFalse(success, "Should fail for invalid JSON")
        self.assertIn("Invalid JSON", message)
        self.assertFalse(self.mapper.is_loaded())

    def test_load_missing_mappings_key(self):
        """Test loading JSON without 'mappings' key"""
        data = {
            "version": "1.0",
            "description": "No mappings here"
        }
        file_path = self.create_temp_mapping_file(data)

        success, message = self.mapper.load_mapping(file_path)

        self.assertFalse(success, "Should fail without mappings key")
        self.assertIn("missing 'mappings'", message.lower())
        self.assertFalse(self.mapper.is_loaded())

    def test_load_mappings_not_dict(self):
        """Test loading JSON where mappings is not a dictionary"""
        data = {
            "version": "1.0",
            "mappings": ["B1", "B2", "B3"]  # List instead of dict
        }
        file_path = self.create_temp_mapping_file(data)

        success, message = self.mapper.load_mapping(file_path)

        self.assertFalse(success, "Should fail if mappings is not dict")
        self.assertIn("not a dictionary", message.lower())
        self.assertFalse(self.mapper.is_loaded())

    def test_load_invalid_mapping_entries(self):
        """Test loading JSON with non-string entries"""
        data = {
            "version": "1.0",
            "mappings": {
                "B1": "TM01_A",
                "B2": 123,  # Invalid: number instead of string
                "B3": None  # Invalid: null value
            }
        }
        file_path = self.create_temp_mapping_file(data)

        success, message = self.mapper.load_mapping(file_path)

        self.assertFalse(success, "Should fail with non-string entries")
        self.assertIn("non-string", message.lower())
        self.assertFalse(self.mapper.is_loaded())

    def test_load_version_mismatch_warning(self):
        """Test loading file with different schema version (should warn but succeed)"""
        data = {
            "version": "2.0",  # Future version
            "mappings": {
                "B1": "TM01_A"
            }
        }
        file_path = self.create_temp_mapping_file(data)

        success, message = self.mapper.load_mapping(file_path)

        # Should succeed but log warning (we can't test log output here)
        self.assertTrue(success, "Should succeed despite version mismatch")

    # ========== Mapping Lookup Tests ==========

    def test_map_existing_key(self):
        """Test mapping an existing key"""
        data = {
            "version": "1.0",
            "mappings": {
                "B41[CN]": "34_39+41",
                "B41[SA]": "41"
            }
        }
        file_path = self.create_temp_mapping_file(data)
        self.mapper.load_mapping(file_path)

        result = self.mapper.map("B41[CN]")

        self.assertEqual(result, "34_39+41")

    def test_map_multiple_keys(self):
        """Test mapping multiple different keys"""
        data = {
            "version": "1.0",
            "mappings": {
                "B1": "TM01_A",
                "B3": "TM03_A",
                "B41[CN]": "34_39+41"
            }
        }
        file_path = self.create_temp_mapping_file(data)
        self.mapper.load_mapping(file_path)

        self.assertEqual(self.mapper.map("B1"), "TM01_A")
        self.assertEqual(self.mapper.map("B3"), "TM03_A")
        self.assertEqual(self.mapper.map("B41[CN]"), "34_39+41")

    def test_map_missing_key_returns_original(self):
        """Test that missing key returns original value"""
        data = {
            "version": "1.0",
            "mappings": {
                "B1": "TM01_A"
            }
        }
        file_path = self.create_temp_mapping_file(data)
        self.mapper.load_mapping(file_path)

        result = self.mapper.map("B999")

        self.assertEqual(result, "B999", "Should return original value")

    def test_map_not_loaded_returns_original(self):
        """Test that mapping without loading returns original value"""
        result = self.mapper.map("B41[CN]")

        self.assertEqual(result, "B41[CN]", "Should return original when not loaded")
        self.assertFalse(self.mapper.is_loaded())

    def test_map_after_clear_returns_original(self):
        """Test that mapping after clear returns original value"""
        data = {
            "version": "1.0",
            "mappings": {"B1": "TM01_A"}
        }
        file_path = self.create_temp_mapping_file(data)
        self.mapper.load_mapping(file_path)

        # Verify mapping works
        self.assertEqual(self.mapper.map("B1"), "TM01_A")

        # Clear and test again
        self.mapper.clear()
        self.assertEqual(self.mapper.map("B1"), "B1", "Should return original after clear")
        self.assertFalse(self.mapper.is_loaded())

    def test_map_tracks_missing_keys(self):
        """Test that missing keys are tracked"""
        data = {
            "version": "1.0",
            "mappings": {"B1": "TM01_A"}
        }
        file_path = self.create_temp_mapping_file(data)
        self.mapper.load_mapping(file_path)

        # Request missing keys
        self.mapper.map("B999")
        self.mapper.map("B888")
        self.mapper.map("B999")  # Duplicate

        missing_keys = self.mapper.get_missing_keys()
        self.assertEqual(len(missing_keys), 2, "Should track unique missing keys")
        self.assertIn("B999", missing_keys)
        self.assertIn("B888", missing_keys)

    # ========== State Management Tests ==========

    def test_clear_resets_all_state(self):
        """Test that clear() resets all internal state"""
        data = {
            "version": "1.0",
            "mappings": {"B1": "TM01_A"}
        }
        file_path = self.create_temp_mapping_file(data)
        self.mapper.load_mapping(file_path)
        self.mapper.map("B999")  # Create missing key

        self.mapper.clear()

        self.assertFalse(self.mapper.is_loaded())
        self.assertEqual(len(self.mapper), 0)
        self.assertIsNone(self.mapper.get_file_path())
        self.assertEqual(len(self.mapper.get_missing_keys()), 0)
        self.assertEqual(len(self.mapper.get_metadata()), 0)

    def test_reload_mapping_clears_previous(self):
        """Test that loading new mapping clears previous state"""
        # Load first mapping
        data1 = {
            "version": "1.0",
            "mappings": {"B1": "TM01_A"}
        }
        file1 = self.create_temp_mapping_file(data1)
        self.mapper.load_mapping(file1)
        self.mapper.map("B999")  # Create missing key

        # Verify first mapping has missing key
        self.assertEqual(len(self.mapper.get_missing_keys()), 1, "Should have missing key from first mapping")

        # Load second mapping
        data2 = {
            "version": "1.0",
            "mappings": {"B2": "TM02_A"}
        }
        file2 = self.temp_dir / "mapping2.json"
        with open(file2, 'w', encoding='utf-8') as f:
            json.dump(data2, f)
        self.mapper.load_mapping(file2)

        # Verify first mapping is cleared
        self.assertEqual(self.mapper.map("B1"), "B1", "Old mapping should be cleared (B1 not in new mapping)")
        self.assertEqual(self.mapper.map("B2"), "TM02_A", "New mapping should work")

        # After reload and mapping B1 (which is now missing), we should have 1 missing key
        missing = self.mapper.get_missing_keys()
        self.assertEqual(len(missing), 1, "Should have new missing key from B1 lookup")
        self.assertIn("B1", missing, "B1 should be tracked as missing")

    # ========== Utility Method Tests ==========

    def test_get_file_path(self):
        """Test getting current mapping file path"""
        data = {
            "version": "1.0",
            "mappings": {"B1": "TM01_A"}
        }
        file_path = self.create_temp_mapping_file(data)
        self.mapper.load_mapping(file_path)

        result_path = self.mapper.get_file_path()

        self.assertEqual(result_path, file_path)
        self.assertIsInstance(result_path, Path)

    def test_get_mapping_count(self):
        """Test getting number of loaded mappings"""
        data = {
            "version": "1.0",
            "mappings": {
                "B1": "TM01_A",
                "B2": "TM02_A",
                "B3": "TM03_A"
            }
        }
        file_path = self.create_temp_mapping_file(data)
        self.mapper.load_mapping(file_path)

        count = self.mapper.get_mapping_count()

        self.assertEqual(count, 3)

    def test_get_load_errors(self):
        """Test getting load errors from failed attempt"""
        fake_path = self.temp_dir / "nonexistent.json"
        self.mapper.load_mapping(fake_path)

        errors = self.mapper.get_load_errors()

        self.assertGreater(len(errors), 0, "Should have error messages")
        self.assertIsInstance(errors[0], str)

    def test_contains_operator(self):
        """Test __contains__ operator"""
        data = {
            "version": "1.0",
            "mappings": {
                "B1": "TM01_A",
                "B41[CN]": "34_39+41"
            }
        }
        file_path = self.create_temp_mapping_file(data)
        self.mapper.load_mapping(file_path)

        self.assertIn("B1", self.mapper)
        self.assertIn("B41[CN]", self.mapper)
        self.assertNotIn("B999", self.mapper)

    def test_repr_string(self):
        """Test __repr__ string representation"""
        # Not loaded
        repr_str = repr(self.mapper)
        self.assertIn("not loaded", repr_str.lower())

        # After loading
        data = {
            "version": "1.0",
            "mappings": {"B1": "TM01_A"}
        }
        file_path = self.create_temp_mapping_file(data)
        self.mapper.load_mapping(file_path)

        repr_str = repr(self.mapper)
        self.assertIn("1 mappings", repr_str)
        self.assertIn(file_path.name, repr_str)


if __name__ == '__main__':
    unittest.main()
