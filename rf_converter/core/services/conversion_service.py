"""Core conversion service - UI independent"""

from pathlib import Path
from typing import List, Callable, Optional, Dict
import pandas as pd

from ..models.conversion_result import ConversionResult
from ..parsers.base_parser import BaseMeasurementParser
from ..parsers.rx_parser import RxGainParser
from ..converters.csv_writer import CsvWriter


class ConversionService:
    """
    🔑 Core business logic for SnP to CSV conversion

    100% UI independent - All UIs (PyQt6, Flask, CLI) use this service

    Responsibilities:
    - Parser selection based on measurement type
    - File validation
    - Batch conversion with progress tracking
    - Error handling and reporting
    """

    # Supported measurement types
    MEASUREMENT_TYPES = {
        'rx_gain': RxGainParser,
        # Future types:
        # 'tx_power': TxPowerParser,
        # 'isolation': IsolationParser,
    }

    def __init__(self, measurement_type: str = 'rx_gain'):
        """
        Initialize conversion service

        Args:
            measurement_type: Type of measurement ('rx_gain', 'tx_power', etc.)

        Raises:
            ValueError: If measurement type is not supported
        """
        if measurement_type not in self.MEASUREMENT_TYPES:
            supported = ', '.join(self.MEASUREMENT_TYPES.keys())
            raise ValueError(
                f"Unsupported measurement type: '{measurement_type}'. "
                f"Supported types: {supported}"
            )

        self.measurement_type = measurement_type
        self.parser = self._create_parser(measurement_type)

    def _create_parser(self, meas_type: str) -> BaseMeasurementParser:
        """
        Factory method for parser creation

        Args:
            meas_type: Measurement type key

        Returns:
            Instantiated parser
        """
        parser_class = self.MEASUREMENT_TYPES[meas_type]
        return parser_class()

    def convert_files(
        self,
        snp_files: List[Path],
        output_csv: Path,
        options: Optional[Dict] = None,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> ConversionResult:
        """
        Convert SnP files to CSV

        Args:
            snp_files: List of SnP file paths to convert
            output_csv: Output CSV file path
            options: Conversion options dictionary:
                - freq_filter (bool): Apply frequency filtering (default: True)
                - auto_band (bool): Auto-detect band from filename (default: True)
                - full_sweep (bool): Include full frequency sweep (default: False)
                - band_mapper: Optional BandMapper instance for notation translation
            progress_callback: Optional callback function(current, total, filename)
                              Called after each file to report progress

        Returns:
            ConversionResult with conversion statistics and errors
        """
        options = options or {}
        freq_filter = options.get('freq_filter', True)
        auto_band = options.get('auto_band', True)
        band_mapper = options.get('band_mapper', None)

        writer = CsvWriter(output_csv)
        errors = []
        total_files = len(snp_files)

        for idx, snp_file in enumerate(snp_files, 1):
            try:
                # Parse single file (with optional band mapper)
                df = self.parser.parse_file(
                    snp_file,
                    freq_filter=freq_filter,
                    auto_band=auto_band,
                    mapper=band_mapper
                )

                # Append to writer buffer
                writer.append(df)

                # Notify progress (if callback provided)
                if progress_callback:
                    progress_callback(idx, total_files, snp_file.name)

            except Exception as e:
                errors.append({
                    'file': snp_file.name,
                    'error': str(e)
                })

        # Write all data to CSV
        try:
            writer.save()

            # Create result
            if output_csv.exists():
                result = ConversionResult(
                    success=True,
                    files_processed=total_files - len(errors),
                    total_files=total_files,
                    rows_generated=writer.get_row_count(),
                    output_path=output_csv,
                    output_size=output_csv.stat().st_size,
                    errors=errors
                )
            else:
                result = ConversionResult(
                    success=False,
                    files_processed=0,
                    total_files=total_files,
                    errors=[{'file': 'output', 'error': 'Failed to create output file'}]
                )

        except Exception as e:
            result = ConversionResult(
                success=False,
                files_processed=0,
                total_files=total_files,
                errors=[{'file': 'output', 'error': str(e)}]
            )

        return result

    def validate_files(self, snp_files: List[Path]) -> Dict:
        """
        Validate SnP files before conversion

        Args:
            snp_files: List of file paths to validate

        Returns:
            Dictionary with validation results:
            - valid_files: List of valid SnP files
            - invalid_files: List of files with issues
            - total_size: Total size in bytes
            - file_count: Number of files
        """
        valid_files = []
        invalid_files = []
        total_size = 0

        for file_path in snp_files:
            if not file_path.exists():
                invalid_files.append({
                    'file': file_path.name,
                    'reason': 'File does not exist'
                })
                continue

            if not self._is_valid_snp_file(file_path):
                invalid_files.append({
                    'file': file_path.name,
                    'reason': 'Invalid SnP file extension'
                })
                continue

            valid_files.append(file_path)
            total_size += file_path.stat().st_size

        return {
            'valid_files': valid_files,
            'invalid_files': invalid_files,
            'total_size': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'file_count': len(valid_files)
        }

    def _is_valid_snp_file(self, file_path: Path) -> bool:
        """
        Check if file is valid SnP format

        Args:
            file_path: Path to check

        Returns:
            True if valid SnP file
        """
        valid_extensions = [f'.s{i}p' for i in range(1, 13)]  # s1p ~ s12p
        return file_path.suffix.lower() in valid_extensions

    def get_supported_types(self) -> List[str]:
        """
        Get list of supported measurement types

        Returns:
            List of measurement type keys
        """
        return list(self.MEASUREMENT_TYPES.keys())

    def get_parser_info(self) -> Dict:
        """
        Get information about current parser

        Returns:
            Dictionary with parser details
        """
        return {
            'measurement_type': self.measurement_type,
            'required_s_parameters': self.parser.get_required_s_parameters(),
            'csv_columns': self.parser.get_csv_columns(),
            'supported_bands': list(self.parser.band_config.keys())
        }
