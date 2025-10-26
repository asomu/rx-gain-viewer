"""Conversion result model"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional


@dataclass
class ConversionResult:
    """
    Result of SnP to CSV conversion

    Attributes:
        success: Whether conversion succeeded
        files_processed: Number of successfully processed files
        total_files: Total number of input files
        rows_generated: Number of CSV rows generated
        output_path: Path to output CSV file
        output_size: Size of output file in bytes
        errors: List of error dictionaries with 'file' and 'error' keys
    """
    success: bool
    files_processed: int
    total_files: int
    rows_generated: int = 0
    output_path: Optional[Path] = None
    output_size: int = 0
    errors: List[Dict[str, str]] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

    @property
    def has_errors(self) -> bool:
        """Check if any errors occurred"""
        return len(self.errors) > 0

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_files == 0:
            return 0.0
        return (self.files_processed / self.total_files) * 100

    @property
    def output_size_kb(self) -> float:
        """Output size in KB"""
        return self.output_size / 1024

    @property
    def output_size_mb(self) -> float:
        """Output size in MB"""
        return self.output_size / (1024 * 1024)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'success': self.success,
            'files_processed': self.files_processed,
            'total_files': self.total_files,
            'rows_generated': self.rows_generated,
            'output_path': str(self.output_path) if self.output_path else None,
            'output_size': self.output_size,
            'output_size_kb': round(self.output_size_kb, 2),
            'output_size_mb': round(self.output_size_mb, 2),
            'success_rate': round(self.success_rate, 2),
            'errors': self.errors
        }

    def __str__(self) -> str:
        """Human-readable summary"""
        status = "✅ SUCCESS" if self.success else "❌ FAILED"
        return f"""
{status}
Files: {self.files_processed}/{self.total_files} ({self.success_rate:.1f}%)
Rows: {self.rows_generated}
Output: {self.output_size_kb:.1f} KB
Errors: {len(self.errors)}
"""
