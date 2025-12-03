"""Band notation mapping system for RF Converter.

Provides optional, user-configurable translation from filename band notation
(e.g., "B41[CN]") to project-specific N-plexer bank notation (e.g., "34_39+41").

This module implements a singleton BandMapper class that loads JSON configuration
files and provides O(1) lookup performance for band notation translation.

Example:
    >>> mapper = BandMapper.get_instance()
    >>> success, msg = mapper.load_mapping("path/to/mapping.json")
    >>> if success:
    ...     nplexer = mapper.map("B41[CN]")  # Returns "34_39+41"
"""

from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class BandMapper:
    """Singleton band notation mapper with lazy loading.

    This class provides optional translation from filename band notation
    to project-specific N-plexer bank notation. It uses lazy loading for
    efficiency and graceful error handling to never break conversion.

    Thread-safe for read operations after initial load.

    Attributes:
        SCHEMA_VERSION: Current JSON schema version (1.0)
    """

    _instance: Optional[BandMapper] = None
    SCHEMA_VERSION = "1.0"

    def __init__(self):
        """Private constructor. Use get_instance() instead."""
        self._mapping_dict: Dict[str, str] = {}
        self._file_path: Optional[Path] = None
        self._is_loaded: bool = False
        self._load_errors: List[str] = []
        self._missing_keys: set[str] = set()
        self._metadata: Dict[str, str] = {}

    @classmethod
    def get_instance(cls) -> BandMapper:
        """Get singleton instance.

        Returns:
            The singleton BandMapper instance.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset singleton instance (for testing only).

        Warning:
            This method should only be used in unit tests.
        """
        cls._instance = None

    def load_mapping(self, file_path: str | Path) -> Tuple[bool, str]:
        """Load mapping from JSON file.

        Args:
            file_path: Path to JSON mapping file

        Returns:
            Tuple of (success: bool, message: str)
            - success: True if loaded successfully
            - message: User-friendly status message

        Example:
            >>> mapper = BandMapper.get_instance()
            >>> success, msg = mapper.load_mapping("mapping.json")
            >>> if success:
            ...     print(f"Loaded {len(mapper)} mappings")
        """
        # Reset state
        self._mapping_dict.clear()
        self._load_errors.clear()
        self._missing_keys.clear()
        self._is_loaded = False
        self._file_path = None
        self._metadata.clear()

        # Convert to Path object
        path = Path(file_path)

        # Validate file exists
        if not path.exists():
            error_msg = f"File not found: {path}"
            logger.error(error_msg)
            self._load_errors.append(error_msg)
            return False, f"❌ File not found: {path.name}"

        # Validate file extension
        if path.suffix.lower() != '.json':
            error_msg = f"Invalid file type: {path.suffix} (expected .json)"
            logger.error(error_msg)
            self._load_errors.append(error_msg)
            return False, f"❌ Invalid file type: {path.suffix}"

        # Load and parse JSON
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON format: {e}"
            logger.error(error_msg)
            self._load_errors.append(error_msg)
            return False, f"❌ Invalid JSON format: {str(e)[:50]}"
        except Exception as e:
            error_msg = f"Failed to read file: {e}"
            logger.error(error_msg)
            self._load_errors.append(error_msg)
            return False, f"❌ Failed to read file: {str(e)[:50]}"

        # Validate schema version
        version = data.get('version', '')
        if version != self.SCHEMA_VERSION:
            warning_msg = f"Schema version mismatch: {version} (expected {self.SCHEMA_VERSION})"
            logger.warning(warning_msg)
            # Continue loading but warn user

        # Validate mappings key exists
        if 'mappings' not in data:
            error_msg = "Missing 'mappings' key in JSON"
            logger.error(error_msg)
            self._load_errors.append(error_msg)
            return False, "❌ Invalid format: missing 'mappings'"

        # Validate mappings is a dictionary
        mappings = data['mappings']
        if not isinstance(mappings, dict):
            error_msg = "'mappings' must be a dictionary"
            logger.error(error_msg)
            self._load_errors.append(error_msg)
            return False, "❌ Invalid format: 'mappings' not a dictionary"

        # Validate all keys and values are strings
        invalid_entries = []
        for key, value in mappings.items():
            if not isinstance(key, str) or not isinstance(value, str):
                invalid_entries.append(f"{key}: {value}")

        if invalid_entries:
            error_msg = f"Invalid mapping entries (non-string): {', '.join(invalid_entries[:3])}"
            logger.error(error_msg)
            self._load_errors.append(error_msg)
            return False, f"❌ Invalid entries: {len(invalid_entries)} non-string mappings"

        # Store metadata
        self._metadata['description'] = data.get('description', '')
        self._metadata['project'] = data.get('project', '')
        self._metadata['created_date'] = data.get('created_date', '')

        # Load mappings (immutable copy for thread safety)
        self._mapping_dict = dict(mappings)
        self._file_path = path
        self._is_loaded = True

        # Log success
        mapping_count = len(self._mapping_dict)
        logger.info(f"Successfully loaded {mapping_count} mappings from {path.name}")

        return True, f"✅ Loaded {mapping_count} mappings from {path.name}"

    def map(self, original: str) -> str:
        """Map original band notation to N-plexer bank notation.

        If mapping is not loaded or key not found, returns original value.
        Logs warning once per missing key to avoid log spam.

        Args:
            original: Original band notation (e.g., "B41[CN]")

        Returns:
            Mapped notation if found, otherwise original value.

        Example:
            >>> mapper.map("B41[CN]")  # Returns "34_39+41"
            >>> mapper.map("B1")       # Returns "TM01_A" or "B1" if not mapped
        """
        if not self._is_loaded:
            return original

        if original in self._mapping_dict:
            return self._mapping_dict[original]

        # Log warning once per missing key (avoid log spam)
        if original not in self._missing_keys:
            self._missing_keys.add(original)
            logger.warning(
                f"No mapping found for '{original}', using original value. "
                f"Add to mapping file: {self._file_path.name if self._file_path else 'N/A'}"
            )

        return original

    def is_loaded(self) -> bool:
        """Check if mapping is loaded.

        Returns:
            True if mapping file was successfully loaded.
        """
        return self._is_loaded

    def get_file_path(self) -> Optional[Path]:
        """Get current mapping file path.

        Returns:
            Path object if loaded, None otherwise.
        """
        return self._file_path

    def get_mapping_count(self) -> int:
        """Get number of loaded mappings.

        Returns:
            Number of mappings, 0 if not loaded.
        """
        return len(self._mapping_dict)

    def get_metadata(self) -> Dict[str, str]:
        """Get mapping file metadata.

        Returns:
            Dictionary with description, project, created_date (empty if not loaded).
        """
        return dict(self._metadata)

    def get_load_errors(self) -> List[str]:
        """Get load errors from last load attempt.

        Returns:
            List of error messages (empty if no errors).
        """
        return list(self._load_errors)

    def get_missing_keys(self) -> set[str]:
        """Get set of keys that were requested but not found in mapping.

        Useful for identifying gaps in mapping configuration.

        Returns:
            Set of missing keys encountered during map() calls.
        """
        return set(self._missing_keys)

    @property
    def mappings(self) -> Dict[str, str]:
        """Get current mappings (read-only copy).

        Returns:
            Dictionary of current mappings.
        """
        return dict(self._mapping_dict)

    @mappings.setter
    def mappings(self, value: Dict[str, str]) -> None:
        """Set mappings directly (for dialog Apply button).

        Args:
            value: Dictionary of band mappings

        Raises:
            TypeError: If value is not a dictionary
            ValueError: If any key or value is not a string
        """
        if not isinstance(value, dict):
            raise TypeError("Mappings must be a dictionary")

        # Validate all keys and values are strings
        for key, val in value.items():
            if not isinstance(key, str) or not isinstance(val, str):
                raise ValueError(f"All mappings must be strings: {key}: {val}")

        # Update mappings
        self._mapping_dict = dict(value)
        self._is_loaded = True
        self._file_path = None  # Mark as not file-backed
        self._missing_keys.clear()

        logger.info(f"Mappings set directly: {len(self._mapping_dict)} entries")

    def clear(self) -> None:
        """Clear all mapping data.

        Resets to initial state (not loaded).
        """
        self._mapping_dict.clear()
        self._load_errors.clear()
        self._missing_keys.clear()
        self._is_loaded = False
        self._file_path = None
        self._metadata.clear()
        logger.info("BandMapper cleared")

    def __len__(self) -> int:
        """Return number of loaded mappings."""
        return len(self._mapping_dict)

    def __contains__(self, key: str) -> bool:
        """Check if key exists in mapping."""
        return key in self._mapping_dict

    def __repr__(self) -> str:
        """String representation of BandMapper."""
        if self._is_loaded:
            return f"BandMapper(loaded={len(self._mapping_dict)} mappings, file={self._file_path.name})"
        return "BandMapper(not loaded)"
