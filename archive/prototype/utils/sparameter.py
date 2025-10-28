"""
S-parameter 분석 유틸리티
"""

from typing import Tuple, List, Dict
import numpy as np


class SParameterAnalyzer:
    """
    S-parameter 데이터 분석 및 처리 유틸리티
    """

    @staticmethod
    def convert_frequency_unit(freq: np.ndarray, from_unit: str = 'Hz', to_unit: str = 'GHz') -> np.ndarray:
        """
        주파수 단위 변환

        Args:
            freq: 주파수 배열
            from_unit: 원본 단위 ('Hz', 'MHz', 'GHz')
            to_unit: 변환 단위 ('Hz', 'MHz', 'GHz')

        Returns:
            변환된 주파수 배열
        """
        units = {'Hz': 1, 'MHz': 1e6, 'GHz': 1e9}

        if from_unit not in units or to_unit not in units:
            raise ValueError(f"지원하지 않는 단위: {from_unit} or {to_unit}")

        # Hz로 변환 후 목표 단위로 변환
        freq_hz = freq * units[from_unit]
        return freq_hz / units[to_unit]

    @staticmethod
    def calculate_gain_statistics(gain_db: np.ndarray) -> Dict[str, float]:
        """
        Gain 통계값 계산

        Args:
            gain_db: Gain 배열 (dB)

        Returns:
            {'mean': 평균, 'max': 최대, 'min': 최소, 'std': 표준편차}
        """
        return {
            'mean': float(np.mean(gain_db)),
            'max': float(np.max(gain_db)),
            'min': float(np.min(gain_db)),
            'std': float(np.std(gain_db))
        }

    @staticmethod
    def find_frequency_range(
        freq: np.ndarray,
        gain: np.ndarray,
        gain_threshold: float
    ) -> Tuple[float, float]:
        """
        특정 Gain 이상인 주파수 대역 찾기

        Args:
            freq: 주파수 배열
            gain: Gain 배열
            gain_threshold: Gain 임계값 (dB)

        Returns:
            (freq_start, freq_end)
        """
        mask = gain >= gain_threshold
        if not np.any(mask):
            return (None, None)

        valid_freq = freq[mask]
        return (valid_freq[0], valid_freq[-1])

    @staticmethod
    def interpolate_data(
        freq: np.ndarray,
        gain: np.ndarray,
        num_points: int = 1000
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        데이터 보간 (스무스한 그래프용)

        Args:
            freq: 주파수 배열
            gain: Gain 배열
            num_points: 보간 후 포인트 수

        Returns:
            (interpolated_freq, interpolated_gain)
        """
        freq_interp = np.linspace(freq[0], freq[-1], num_points)
        gain_interp = np.interp(freq_interp, freq, gain)
        return freq_interp, gain_interp

    @staticmethod
    def auto_y_range(
        gain_values: List[np.ndarray],
        margin_percent: float = 10.0
    ) -> Tuple[float, float]:
        """
        여러 Gain 데이터의 Y축 범위 자동 계산

        Args:
            gain_values: Gain 배열 리스트
            margin_percent: 여백 비율 (%)

        Returns:
            (y_min, y_max)
        """
        all_gains = np.concatenate(gain_values)
        g_min, g_max = all_gains.min(), all_gains.max()

        margin = (g_max - g_min) * (margin_percent / 100)
        return (g_min - margin, g_max + margin)

    @staticmethod
    def detect_band_from_frequency(freq: np.ndarray) -> str:
        """
        주파수 범위에서 LTE Band 자동 감지

        Args:
            freq: 주파수 배열 (Hz)

        Returns:
            Band 이름 (예: 'B1', 'B3')
        """
        freq_mhz = freq[0] / 1e6  # 첫 포인트 기준

        # LTE Band 주파수 매핑 (간략화)
        bands = {
            'B1': (1920, 2170),
            'B3': (1710, 1880),
            'B7': (2500, 2690),
            'B20': (791, 862),
            'B38': (2570, 2620),
            'B41': (2496, 2690),
        }

        for band_name, (f_min, f_max) in bands.items():
            if f_min <= freq_mhz <= f_max:
                return band_name

        return 'Unknown'
