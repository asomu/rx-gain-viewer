"""
CSV 파일 파서 (SnP에서 추출된 데이터용)
"""

from pathlib import Path
from typing import Tuple, Dict, List
import pandas as pd
import numpy as np


class CsvParser:
    """
    SnP에서 파싱된 CSV 파일 처리

    예상 CSV 포맷:
    frequency,gain_db
    2100000000,-15.2
    2100100000,-15.3
    ...
    """

    def __init__(self, file_path: str):
        """
        Args:
            file_path: CSV 파일 경로
        """
        self.file_path = Path(file_path)
        self.data = None
        self._is_loaded = False

    def load(self, freq_column: str = 'frequency', value_column: str = 'gain_db') -> bool:
        """
        CSV 파일 로드

        Args:
            freq_column: 주파수 컬럼명
            value_column: 값 컬럼명 (Gain, S11 등)

        Returns:
            성공 여부
        """
        try:
            self.data = pd.read_csv(self.file_path)
            self.freq_column = freq_column
            self.value_column = value_column
            self._is_loaded = True
            return True
        except Exception as e:
            raise ValueError(f"CSV 파일 로드 실패: {e}")

    def get_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        주파수와 값 데이터 반환

        Returns:
            (frequency_array, value_array)
        """
        if not self._is_loaded:
            raise ValueError("파일을 먼저 load() 해야 합니다")

        freq = self.data[self.freq_column].values
        values = self.data[self.value_column].values

        return freq, values

    @property
    def frequency_range(self) -> Tuple[float, float]:
        """주파수 범위"""
        if not self._is_loaded:
            return None
        freq = self.data[self.freq_column]
        return (freq.min(), freq.max())

    @property
    def value_range(self) -> Tuple[float, float]:
        """값 범위 (Gain min/max)"""
        if not self._is_loaded:
            return None
        values = self.data[self.value_column]
        return (values.min(), values.max())

    def __repr__(self):
        if self._is_loaded:
            return f"CsvParser('{self.file_path.name}', points={len(self.data)}, freq_range={self.frequency_range})"
        return f"CsvParser('{self.file_path.name}', not loaded)"
