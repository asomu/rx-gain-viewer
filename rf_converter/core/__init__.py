"""
RF Converter Core Module

UI-independent business logic for SnP to CSV conversion.

Main Components:
- ConversionService: Core business logic orchestrator
- BaseMeasurementParser: Abstract parser interface
- RxGainParser: Rx Gain measurement implementation
- SnpReader: Touchstone file format reader
- CsvWriter: CSV file writer
- ConversionResult: Result data model
"""

from .services.conversion_service import ConversionService
from .models.conversion_result import ConversionResult
from .parsers.base_parser import BaseMeasurementParser
from .parsers.rx_parser import RxGainParser
from .parsers.snp_reader import SnpReader
from .converters.csv_writer import CsvWriter

__version__ = '1.0.0'
__all__ = [
    'ConversionService',
    'ConversionResult',
    'BaseMeasurementParser',
    'RxGainParser',
    'SnpReader',
    'CsvWriter',
]
