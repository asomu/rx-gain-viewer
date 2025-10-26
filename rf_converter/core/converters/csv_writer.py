"""CSV file writer"""

from pathlib import Path
import pandas as pd
from typing import Optional


class CsvWriter:
    """
    Write measurement data to CSV file in Bellagio format

    Supports:
    - Incremental writing (append mode)
    - Memory-efficient batch writing
    - Automatic header handling
    """

    def __init__(self, output_path: Path):
        """
        Initialize CSV writer

        Args:
            output_path: Path to output CSV file
        """
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self._data_buffer = []
        self._header_written = False

    def append(self, df: pd.DataFrame):
        """
        Append DataFrame to buffer

        Args:
            df: DataFrame to append
        """
        self._data_buffer.append(df)

    def write(self, df: pd.DataFrame):
        """
        Write DataFrame to CSV immediately

        Args:
            df: DataFrame to write
        """
        df.to_csv(
            self.output_path,
            index=False,
            mode='w',
            encoding='utf-8'
        )
        self._header_written = True

    def flush(self):
        """Write buffered data to file"""
        if not self._data_buffer:
            return

        combined_df = pd.concat(self._data_buffer, ignore_index=True)
        self.write(combined_df)
        self._data_buffer = []

    def save(self):
        """Alias for flush()"""
        self.flush()

    def get_row_count(self) -> int:
        """Get number of rows in buffer"""
        if not self._data_buffer:
            return 0
        return sum(len(df) for df in self._data_buffer)
