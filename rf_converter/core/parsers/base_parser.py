"""Base abstract class for measurement parsers"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import re


class BaseMeasurementParser(ABC):
    """
    Abstract base class for all measurement type parsers

    Subclasses implement specific measurement types (Rx, Tx, Isolation)
    All parsers share common filename parsing and frequency filtering
    """

    def __init__(self, band_config: Optional[Dict[str, tuple]] = None):
        """
        Initialize parser

        Args:
            band_config: Dictionary mapping band names to (min_freq, max_freq) tuples
                        Example: {'B1': (2110, 2170), 'B7': (2500, 2570)}
        """
        self.band_config = band_config or self._default_band_config()
        self.measurement_type = self.get_measurement_type()

    @staticmethod
    def _default_band_config() -> Dict[str, tuple]:
        """Default LTE band configurations (MHz)"""
        return {
            'B1': (2110, 2170),
            'B2': (1930, 1990),
            'B3': (1805, 1880),
            'B4': (2110, 2155),
            'B5': (869, 894),
            'B7': (2500, 2570),
            'B8': (925, 960),
            'B12': (729, 746),
            'B13': (746, 756),
            'B14': (758, 768),
            'B17': (734, 746),
            'B20': (791, 821),
            'B25': (1930, 1995),
            'B26': (859, 894),
            'B28': (758, 803),
            'B29': (717, 728),
            'B30': (2350, 2360),
            'B38': (2570, 2620),
            'B39': (1880, 1920),
            'B40': (2300, 2400),
            'B41': (2496, 2690),
            'B42': (3400, 3600),
            'B43': (3600, 3800),
            'B48': (3550, 3700),
            'B66': (2110, 2200),
            'B71': (617, 652),
        }

    # ========== Abstract Methods (Must Implement) ==========

    @abstractmethod
    def get_measurement_type(self) -> str:
        """
        Return measurement type identifier

        Returns:
            String like 'rx_gain', 'tx_power', 'isolation'
        """
        pass

    @abstractmethod
    def get_required_s_parameters(self) -> List[str]:
        """
        Return list of required S-parameter names

        Returns:
            List like ['S21', 'S12', 'S11', 'S22']
        """
        pass

    @abstractmethod
    def calculate_metrics(self, s_params_df: pd.DataFrame, metadata: Dict) -> pd.DataFrame:
        """
        Calculate measurement-specific metrics from S-parameters

        Args:
            s_params_df: DataFrame with frequency and S-parameter columns
            metadata: Metadata extracted from filename

        Returns:
            DataFrame with calculated metrics (Gain, RL, etc.)
        """
        pass

    @abstractmethod
    def get_csv_columns(self) -> List[str]:
        """
        Return ordered list of CSV column names

        Returns:
            List of column names matching target CSV format
        """
        pass

    # ========== Common Methods (Shared) ==========

    def parse_file(
        self,
        snp_file: Path,
        freq_filter: bool = True,
        auto_band: bool = True
    ) -> pd.DataFrame:
        """
        Parse single SnP file to DataFrame

        Args:
            snp_file: Path to .s2p file
            freq_filter: Apply band-specific frequency filtering
            auto_band: Auto-detect band from filename

        Returns:
            DataFrame with CSV rows for this file
        """
        from .snp_reader import SnpReader

        # Extract metadata from filename
        metadata = self.parse_filename(snp_file.name)

        # Read SnP file
        reader = SnpReader(snp_file)
        s_params_df = reader.read()

        # Filter frequencies if enabled
        if freq_filter and auto_band:
            band = metadata.get('band')
            if band and band in self.band_config:
                s_params_df = self.filter_frequency(s_params_df, band)

        # Calculate metrics
        result_df = self.calculate_metrics(s_params_df, metadata)

        return result_df

    def parse_filename(self, filename: str) -> Dict:
        """
        Extract metadata from SnP filename

        Filename format: X_ANT1_B1@1_(G0H).s2p

        Returns:
            Dictionary with keys:
            - port_in: Input port (e.g., 'ANT1')
            - band: Band name (e.g., 'B1')
            - port_out: Output port code (e.g., '@1' → 'RXOUT1')
            - lna_state: LNA gain state (e.g., 'G0H' → 'G0_H')
            - ca_config: CA configuration if present
        """
        metadata = {}

        # Remove .s2p extension
        name = filename.replace('.s2p', '').replace('.s1p', '')

        # Split by underscore
        parts = name.split('_')

        # Extract input port (usually second part)
        if len(parts) >= 2:
            metadata['port_in'] = parts[1]  # ANT1, ANT2, etc.

        # Extract band and output port
        # Pattern: B1@1, B1[B7]@2, B41@3, etc.
        band_pattern = r'(B\d+(?:\[B\d+\])?)\@?(\d+)?'
        for part in parts:
            match = re.search(band_pattern, part)
            if match:
                metadata['band'] = self._extract_primary_band(match.group(1))
                metadata['ca_config'] = match.group(1)  # Full CA config
                if match.group(2):
                    metadata['port_out'] = f'RXOUT{match.group(2)}'
                break

        # Extract LNA state from parentheses
        lna_pattern = r'\(([^)]+)\)'
        match = re.search(lna_pattern, name)
        if match:
            lna_raw = match.group(1)
            # Convert G0H → G0_H
            if 'H' in lna_raw or 'L' in lna_raw:
                metadata['lna_state'] = lna_raw.replace('G', 'G').replace('H', '_H').replace('L', '_L')
            else:
                metadata['lna_state'] = lna_raw

        return metadata

    def _extract_primary_band(self, band_str: str) -> str:
        """
        Extract primary band from CA config

        Examples:
            'B1' → 'B1'
            'B1[B7]' → 'B1'
            'B41[B3]' → 'B41'
        """
        match = re.match(r'(B\d+)', band_str)
        return match.group(1) if match else band_str

    def filter_frequency(self, df: pd.DataFrame, band: str) -> pd.DataFrame:
        """
        Filter DataFrame to band-specific frequency range

        Args:
            df: DataFrame with 'frequency' column (in MHz)
            band: Band name (e.g., 'B1')

        Returns:
            Filtered DataFrame
        """
        if band not in self.band_config:
            return df

        freq_min, freq_max = self.band_config[band]

        # Convert Hz to MHz if needed
        if df['frequency'].max() > 10000:  # Likely in Hz
            df = df.copy()
            df['frequency'] = df['frequency'] / 1e6

        return df[(df['frequency'] >= freq_min) & (df['frequency'] <= freq_max)]

    def map_port_to_s_notation(self, port_in: str, port_out: str) -> str:
        """
        Map port names to S-parameter notation

        Examples:
            ANT1, RXOUT1 → S0706
            ANT2, RXOUT2 → S0808

        Port mapping:
            ANT1 → 6, ANT2 → 7, ANT3 → 8, ANT4 → 9
            RXOUT1 → 6, RXOUT2 → 7, RXOUT3 → 8, RXOUT4 → 9
        """
        port_map_in = {
            'ANT1': '07', 'ANT2': '08', 'ANT3': '09', 'ANT4': '10'
        }
        port_map_out = {
            'RXOUT1': '06', 'RXOUT2': '07', 'RXOUT3': '08', 'RXOUT4': '09'
        }

        in_code = port_map_in.get(port_in, '07')
        out_code = port_map_out.get(port_out, '06')

        return f'S{in_code}{out_code}'
