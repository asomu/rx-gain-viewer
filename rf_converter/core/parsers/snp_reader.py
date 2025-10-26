"""Touchstone SnP file reader"""

from pathlib import Path
import pandas as pd
import numpy as np
from typing import Optional


class SnpReader:
    """
    Read Touchstone format SnP files (.s1p, .s2p, .s3p, .s4p)

    Supports:
    - Frequency units: Hz, KHz, MHz, GHz
    - Data format: MA (magnitude/angle), RI (real/imaginary), DB (dB/angle)
    - 2-port S-parameters (S11, S21, S12, S22)
    """

    def __init__(self, file_path: Path):
        """
        Initialize reader

        Args:
            file_path: Path to SnP file
        """
        self.file_path = Path(file_path)
        self.freq_unit = 'Hz'
        self.param_type = 'S'
        self.data_format = 'RI'  # Real/Imaginary
        self.impedance = 50.0
        self.num_ports = self._detect_num_ports()

    def _detect_num_ports(self) -> int:
        """Detect number of ports from file extension (s1p ~ s12p)"""
        ext = self.file_path.suffix.lower()
        
        # Extract port number from extension (.s2p -> 2, .s12p -> 12)
        import re
        match = re.match(r'\.s(\d+)p', ext)
        if match:
            num_ports = int(match.group(1))
            if 1 <= num_ports <= 12:
                return num_ports
        
        raise ValueError(f"Unsupported SnP file extension: {ext} (s1p~s12p supported)")

    def read(self) -> pd.DataFrame:
        """
        Read SnP file and return DataFrame

        Returns:
            DataFrame with columns:
            - frequency: Frequency in MHz
            - S11_re, S11_im: S11 real/imaginary
            - S21_re, S21_im: S21 real/imaginary
            - S12_re, S12_im: S12 real/imaginary
            - S22_re, S22_im: S22 real/imaginary
        """
        with open(self.file_path, 'r') as f:
            lines = f.readlines()

        # Parse header
        data_start_idx = self._parse_header(lines)

        # Parse data
        data_lines = [line.strip() for line in lines[data_start_idx:]
                      if line.strip() and not line.strip().startswith('!')]

        return self._parse_data(data_lines)

    def _parse_header(self, lines: list) -> int:
        """
        Parse header and option line

        Returns:
            Index where data starts
        """
        for idx, line in enumerate(lines):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('!'):
                continue

            # Option line starts with #
            if line.startswith('#'):
                parts = line.split()
                if len(parts) >= 5:
                    self.freq_unit = parts[1].upper()
                    self.param_type = parts[2].upper()
                    self.data_format = parts[3].upper()
                    self.impedance = float(parts[5]) if len(parts) > 5 else 50.0

                return idx + 1

        # No option line found, assume defaults
        return 0

    def _parse_data(self, data_lines: list) -> pd.DataFrame:
        """
        Parse data lines to DataFrame

        Format (2-port RI):
        freq re:S11 im:S11 re:S21 im:S21 re:S12 im:S12 re:S22 im:S22
        """
        data = []

        for line in data_lines:
            values = line.split()
            if len(values) < 9:  # Need at least freq + 4 S-params (re+im each)
                continue

            try:
                freq = float(values[0])
                s11_re, s11_im = float(values[1]), float(values[2])
                s21_re, s21_im = float(values[3]), float(values[4])
                s12_re, s12_im = float(values[5]), float(values[6])
                s22_re, s22_im = float(values[7]), float(values[8])

                data.append({
                    'frequency': self._convert_frequency(freq),
                    'S11_re': s11_re,
                    'S11_im': s11_im,
                    'S21_re': s21_re,
                    'S21_im': s21_im,
                    'S12_re': s12_re,
                    'S12_im': s12_im,
                    'S22_re': s22_re,
                    'S22_im': s22_im,
                })
            except (ValueError, IndexError):
                continue

        df = pd.DataFrame(data)

        # Convert to magnitude/phase if needed
        if self.data_format == 'MA':
            df = self._convert_ma_to_ri(df)
        elif self.data_format == 'DB':
            df = self._convert_db_to_ri(df)

        return df

    def _convert_frequency(self, freq: float) -> float:
        """Convert frequency to MHz"""
        conversions = {
            'HZ': 1e-6,
            'KHZ': 1e-3,
            'MHZ': 1.0,
            'GHZ': 1e3,
        }
        return freq * conversions.get(self.freq_unit, 1e-6)

    def _convert_ma_to_ri(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert Magnitude/Angle to Real/Imaginary

        MA format: magnitude (linear), angle (degrees)
        RI format: real, imaginary
        """
        for param in ['S11', 'S21', 'S12', 'S22']:
            mag_col = f'{param}_re'  # Originally magnitude
            ang_col = f'{param}_im'  # Originally angle in degrees

            if mag_col in df.columns and ang_col in df.columns:
                magnitude = df[mag_col]
                angle_rad = np.radians(df[ang_col])

                df[f'{param}_re'] = magnitude * np.cos(angle_rad)
                df[f'{param}_im'] = magnitude * np.sin(angle_rad)

        return df

    def _convert_db_to_ri(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert dB/Angle to Real/Imaginary

        DB format: dB (20*log10), angle (degrees)
        RI format: real, imaginary
        """
        for param in ['S11', 'S21', 'S12', 'S22']:
            db_col = f'{param}_re'   # Originally dB
            ang_col = f'{param}_im'  # Originally angle in degrees

            if db_col in df.columns and ang_col in df.columns:
                magnitude = 10 ** (df[db_col] / 20)  # Convert dB to linear
                angle_rad = np.radians(df[ang_col])

                df[f'{param}_re'] = magnitude * np.cos(angle_rad)
                df[f'{param}_im'] = magnitude * np.sin(angle_rad)

        return df

    def get_file_info(self) -> dict:
        """Get file metadata"""
        return {
            'filename': self.file_path.name,
            'num_ports': self.num_ports,
            'freq_unit': self.freq_unit,
            'data_format': self.data_format,
            'impedance': self.impedance,
        }
