"""
SnP (Touchstone) 파일 파서
scikit-rf 라이브러리 기반
"""

from pathlib import Path
from typing import Tuple, Optional
import numpy as np


class SnpParser:
    """
    Touchstone 형식의 SnP 파일 파싱

    지원 파일:
    - .s2p, .s10p, .s12p 등
    - Frequency, S-parameters (magnitude, phase)
    """

    def __init__(self, file_path: str):
        """
        Args:
            file_path: SnP 파일 경로
        """
        self.file_path = Path(file_path)
        self.network = None
        self._is_loaded = False

    def load(self) -> bool:
        """
        SnP 파일 로드

        Returns:
            성공 여부
        """
        try:
            import skrf as rf
            self.network = rf.Network(str(self.file_path))
            self._is_loaded = True
            return True
        except ImportError:
            raise ImportError("scikit-rf가 설치되지 않았습니다. 'pip install scikit-rf' 실행")
        except Exception as e:
            raise ValueError(f"SnP 파일 로드 실패: {e}")

    def get_s_parameter(
        self,
        m: int,
        n: int,
        format: str = 'db'
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        S-parameter 데이터 추출

        Args:
            m: 출력 포트 번호 (1-based)
            n: 입력 포트 번호 (1-based)
            format: 'db' (dB), 'mag' (magnitude), 'deg' (phase degree)

        Returns:
            (frequency_array, s_parameter_array)

        Example:
            >>> parser = SnpParser('test.s10p')
            >>> parser.load()
            >>> freq, s21 = parser.get_s_parameter(2, 1, 'db')  # S21 in dB
        """
        if not self._is_loaded:
            raise ValueError("파일을 먼저 load() 해야 합니다")

        # scikit-rf는 0-based indexing
        s_param = self.network.s[:, m-1, n-1]

        if format == 'db':
            data = 20 * np.log10(np.abs(s_param))
        elif format == 'mag':
            data = np.abs(s_param)
        elif format == 'deg':
            data = np.angle(s_param, deg=True)
        else:
            raise ValueError(f"Unknown format: {format}")

        return self.network.f, data

    def get_gain(
        self,
        input_port: int,
        output_port: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Gain (S21) 추출 - dB 단위

        Args:
            input_port: 입력 포트 (1-based)
            output_port: 출력 포트 (1-based)

        Returns:
            (frequency_Hz, gain_dB)
        """
        return self.get_s_parameter(output_port, input_port, 'db')

    def get_return_loss(self, port: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Return Loss (S11, S22 등) 추출 - dB 단위

        Args:
            port: 포트 번호 (1-based)

        Returns:
            (frequency_Hz, return_loss_dB)
        """
        return self.get_s_parameter(port, port, 'db')

    @property
    def frequency_range(self) -> Optional[Tuple[float, float]]:
        """주파수 범위 (Hz)"""
        if not self._is_loaded:
            return None
        return (self.network.f[0], self.network.f[-1])

    @property
    def num_ports(self) -> Optional[int]:
        """포트 개수"""
        if not self._is_loaded:
            return None
        return self.network.s.shape[1]

    def __repr__(self):
        if self._is_loaded:
            return f"SnpParser('{self.file_path.name}', ports={self.num_ports}, freq_range={self.frequency_range})"
        return f"SnpParser('{self.file_path.name}', not loaded)"
