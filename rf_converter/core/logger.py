"""
Logging functionality for RF Converter
Saves conversion history to log files
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
import json


class ConversionLogger:
    """
    Logger for RF Converter operations

    Features:
    - Conversion history logging
    - Error tracking
    - JSON format for easy parsing
    - Automatic log rotation
    """

    def __init__(self, log_dir: Optional[Path] = None):
        """
        Initialize logger

        Args:
            log_dir: Directory for log files (default: ./logs)
        """
        if log_dir is None:
            log_dir = Path.home() / ".rf_converter" / "logs"

        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup Python logging
        self.setup_logging()

        # JSON log file for conversion history
        self.json_log_file = self.log_dir / "conversion_history.json"

    def setup_logging(self):
        """Setup Python logging to file"""
        log_file = self.log_dir / f"rf_converter_{datetime.now():%Y%m%d}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger('RF_Converter')

    def log_conversion_start(self, files: list, output_path: Path, options: dict):
        """Log when conversion starts"""
        self.logger.info(f"=== Conversion Started ===")
        self.logger.info(f"Files: {len(files)} SnP files")
        self.logger.info(f"Output: {output_path}")
        self.logger.info(f"Options: {options}")

    def log_conversion_complete(self, result):
        """Log conversion completion with results"""
        if result.success:
            self.logger.info(f"✅ Conversion Successful")
            self.logger.info(f"   Files processed: {result.files_processed}/{result.total_files}")
            self.logger.info(f"   Rows generated: {result.rows_generated:,}")
            self.logger.info(f"   Output size: {result.output_size_kb:.1f} KB")

            if result.has_errors:
                self.logger.warning(f"   ⚠️ Errors: {len(result.errors)}")
                for error in result.errors[:3]:  # Log first 3 errors
                    self.logger.warning(f"      - {error.get('file')}: {error.get('error')}")
        else:
            self.logger.error(f"❌ Conversion Failed")
            for error in result.errors[:5]:
                self.logger.error(f"   - {error.get('file')}: {error.get('error')}")

        # Save to JSON history
        self.save_conversion_history(result)

    def save_conversion_history(self, result):
        """Save conversion to JSON history file"""
        history = self.load_history()

        entry = {
            'timestamp': datetime.now().isoformat(),
            'success': result.success,
            'files_processed': result.files_processed,
            'total_files': result.total_files,
            'rows_generated': result.rows_generated if result.success else 0,
            'output_path': str(result.output_path) if result.output_path else None,
            'output_size_kb': result.output_size_kb if result.success else 0,
            'errors': result.errors if result.has_errors else []
        }

        history.append(entry)

        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]

        with open(self.json_log_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def load_history(self) -> list:
        """Load conversion history from JSON file"""
        if not self.json_log_file.exists():
            return []

        try:
            with open(self.json_log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load history: {e}")
            return []

    def get_recent_conversions(self, count: int = 10) -> list:
        """Get recent conversion history"""
        history = self.load_history()
        return history[-count:] if len(history) > count else history

    def log_error(self, error_msg: str):
        """Log error message"""
        self.logger.error(error_msg)

    def log_info(self, info_msg: str):
        """Log info message"""
        self.logger.info(info_msg)

    def get_log_directory(self) -> Path:
        """Get log directory path"""
        return self.log_dir


# Singleton instance
_logger_instance = None


def get_logger() -> ConversionLogger:
    """Get global logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = ConversionLogger()
    return _logger_instance
