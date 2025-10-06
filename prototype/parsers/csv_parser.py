"""
CSV File Parser
Supports both simple CSV (frequency, gain_db) and consolidated format (89 columns)
"""

from pathlib import Path
from typing import Tuple, Dict, List, Optional
import pandas as pd
import numpy as np


class CsvParser:
    """
    CSV file parser supporting multiple formats:

    1. Simple format (SnP-extracted):
       frequency,gain_db
       2100000000,-15.2

    2. Consolidated format (89 columns):
       Freq Type,RAT,Cfg Band,...,Gain (dB),...
       IB,LTE,B1,...,16.466,...
    """

    # Active RF Path to port name mapping
    PORT_MAPPING = {
        'S0706': ('ANT1', 'RXOUT1'),
        'S0705': ('ANT2', 'RXOUT1'),
        'S0702': ('ANTL', 'RXOUT1'),
        'S0306': ('ANT1', 'RXOUT2'),
        'S0305': ('ANT2', 'RXOUT2'),
        'S0302': ('ANTL', 'RXOUT2'),
        'S0806': ('ANT1', 'RXOUT3'),
        'S0805': ('ANT2', 'RXOUT3'),
        'S0802': ('ANTL', 'RXOUT3'),
        'S0406': ('ANT1', 'RXOUT4'),
        'S0405': ('ANT2', 'RXOUT4'),
        'S0402': ('ANTL', 'RXOUT4'),
    }

    def __init__(self, file_path: str):
        """
        Args:
            file_path: CSV file path
        """
        self.file_path = Path(file_path)
        self.data = None
        self._is_loaded = False
        self._format_type = None  # 'simple' or 'consolidated'

    def load(self, freq_column: str = 'frequency', value_column: str = 'gain_db') -> bool:
        """
        Load CSV file (simple format)

        Args:
            freq_column: Frequency column name
            value_column: Value column name (Gain, S11, etc.)

        Returns:
            Success status
        """
        try:
            self.data = pd.read_csv(self.file_path)
            self.freq_column = freq_column
            self.value_column = value_column
            self._is_loaded = True
            self._format_type = 'simple'
            return True
        except Exception as e:
            raise ValueError(f"Failed to load CSV file: {e}")

    def load_consolidated(self) -> bool:
        """
        Load consolidated format CSV (89 columns)

        Expected columns:
        - Freq Type, RAT, Cfg Band, Debug Band, Frequency
        - Active RF Path, Gain (dB), ...
        - cfg-active_port_1, cfg-active_port_2, cfg-lna_gain_state

        Returns:
            Success status
        """
        try:
            self.data = pd.read_csv(self.file_path)

            # Verify essential columns exist
            required_cols = ['Cfg Band', 'Frequency', 'Active RF Path', 'Gain (dB)']
            missing = [col for col in required_cols if col not in self.data.columns]

            if missing:
                raise ValueError(f"Missing required columns: {missing}")

            self._is_loaded = True
            self._format_type = 'consolidated'
            return True
        except Exception as e:
            raise ValueError(f"Failed to load consolidated CSV: {e}")

    def auto_detect_and_load(self) -> bool:
        """
        Auto-detect CSV format and load appropriately

        Returns:
            Success status
        """
        try:
            # Read first line to detect format
            df_sample = pd.read_csv(self.file_path, nrows=1)

            if 'Cfg Band' in df_sample.columns and 'Active RF Path' in df_sample.columns:
                return self.load_consolidated()
            else:
                return self.load()
        except Exception as e:
            raise ValueError(f"Failed to auto-detect CSV format: {e}")

    def get_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get frequency and value data (simple format)

        Returns:
            (frequency_array, value_array)
        """
        if not self._is_loaded:
            raise ValueError("File must be loaded first with load()")

        if self._format_type != 'simple':
            raise ValueError("Use get_data_by_filter() for consolidated format")

        freq = self.data[self.freq_column].values
        values = self.data[self.value_column].values

        return freq, values

    def get_data_by_filter(
        self,
        band: str,
        active_rf_path: Optional[str] = None,
        lna_gain_state: Optional[str] = None
    ) -> Dict[str, np.ndarray]:
        """
        Get filtered data from consolidated format

        Args:
            band: Band name (e.g., 'B1', 'B3', 'B41')
            active_rf_path: Active RF Path (e.g., 'S0706'), optional
            lna_gain_state: LNA gain state (e.g., 'G0_H'), optional

        Returns:
            Dictionary with frequency, gain, and metadata
        """
        if not self._is_loaded or self._format_type != 'consolidated':
            raise ValueError("Consolidated format must be loaded first with load_consolidated()")

        # Start with band filter
        filtered = self.data[self.data['Cfg Band'] == band].copy()

        # Apply Active RF Path filter if specified
        if active_rf_path:
            filtered = filtered[filtered['Active RF Path'] == active_rf_path]

        # Apply LNA gain state filter if specified
        if lna_gain_state and 'cfg-lna_gain_state' in filtered.columns:
            filtered = filtered[filtered['cfg-lna_gain_state'] == lna_gain_state]

        if filtered.empty:
            return {
                'frequency': np.array([]),
                'gain_db': np.array([]),
                'count': 0
            }

        # Extract port labels
        port_1 = filtered['cfg-active_port_1'].iloc[0] if 'cfg-active_port_1' in filtered.columns else None
        port_2 = filtered['cfg-active_port_2'].iloc[0] if 'cfg-active_port_2' in filtered.columns else None

        return {
            'frequency': filtered['Frequency'].values,
            'gain_db': filtered['Gain (dB)'].values,
            'band': band,
            'active_rf_path': active_rf_path or filtered['Active RF Path'].iloc[0],
            'input_port': port_1,
            'output_port': port_2,
            'lna_gain_state': lna_gain_state,
            'count': len(filtered)
        }

    def get_available_bands(self) -> List[str]:
        """
        Get list of available bands in consolidated format

        Returns:
            List of band names (sorted)
        """
        if not self._is_loaded or self._format_type != 'consolidated':
            raise ValueError("Consolidated format must be loaded first")

        return sorted(self.data['Cfg Band'].unique().tolist())

    def get_available_paths(self, band: Optional[str] = None) -> List[Dict]:
        """
        Get list of available Active RF Paths

        Args:
            band: Optional band filter

        Returns:
            List of dicts with Active RF Path and port info
        """
        if not self._is_loaded or self._format_type != 'consolidated':
            raise ValueError("Consolidated format must be loaded first")

        df = self.data if band is None else self.data[self.data['Cfg Band'] == band]

        paths = df[['Active RF Path', 'cfg-active_port_1', 'cfg-active_port_2']].drop_duplicates()

        result = []
        for _, row in paths.iterrows():
            rf_path = row['Active RF Path']
            port_1 = row['cfg-active_port_1']
            port_2 = row['cfg-active_port_2']

            result.append({
                'active_rf_path': rf_path,
                'input_port': port_1,
                'output_port': port_2,
                'port_label': f"{port_1}→{port_2}"
            })

        return result

    def get_band_frequency_range(self, band: str) -> Tuple[float, float]:
        """
        Get frequency range for a specific band

        Args:
            band: Band name

        Returns:
            (min_freq, max_freq) in MHz
        """
        if not self._is_loaded or self._format_type != 'consolidated':
            raise ValueError("Consolidated format must be loaded first")

        band_data = self.data[self.data['Cfg Band'] == band]
        if band_data.empty:
            return (None, None)

        return (band_data['Frequency'].min(), band_data['Frequency'].max())

    def get_ca_combinations(self, band: Optional[str] = None) -> List[str]:
        """
        Get list of CA combinations (from debug-nplexer_bank column)

        Args:
            band: Optional band filter

        Returns:
            List of CA combination strings (sorted)
        """
        if not self._is_loaded or self._format_type != 'consolidated':
            raise ValueError("Consolidated format must be loaded first")

        if 'debug-nplexer_bank' not in self.data.columns:
            return []

        df = self.data if band is None else self.data[self.data['Cfg Band'] == band]

        ca_combinations = df['debug-nplexer_bank'].unique().tolist()

        # Sort: single band first, then CA combinations
        def sort_key(ca):
            # Count '+' to determine if it's CA or single band
            if '+' in str(ca):
                return (1, str(ca))  # CA combinations
            else:
                return (0, str(ca))  # Single band

        return sorted(ca_combinations, key=sort_key)

    def get_lna_gain_states(self, band: Optional[str] = None) -> List[str]:
        """
        Get list of LNA gain states

        Args:
            band: Optional band filter

        Returns:
            List of LNA gain state strings (sorted)
        """
        if not self._is_loaded or self._format_type != 'consolidated':
            raise ValueError("Consolidated format must be loaded first")

        if 'cfg-lna_gain_state' not in self.data.columns:
            return []

        df = self.data if band is None else self.data[self.data['Cfg Band'] == band]

        gain_states = df['cfg-lna_gain_state'].unique().tolist()

        # Sort: G0_H, G0_L, then G1-G5
        def sort_key(state):
            state_str = str(state)
            if state_str.startswith('G0'):
                return (0, state_str)
            else:
                return (1, state_str)

        return sorted(gain_states, key=sort_key)

    def get_input_ports(self, band: Optional[str] = None) -> List[str]:
        """
        Get list of input ports (ANT1, ANT2, ANTL)

        Args:
            band: Optional band filter

        Returns:
            List of input port names (sorted)
        """
        if not self._is_loaded or self._format_type != 'consolidated':
            raise ValueError("Consolidated format must be loaded first")

        if 'cfg-active_port_1' not in self.data.columns:
            return []

        df = self.data if band is None else self.data[self.data['Cfg Band'] == band]

        ports = df['cfg-active_port_1'].unique().tolist()

        # Sort: ANT1, ANT2, ANTL
        port_order = {'ANT1': 0, 'ANT2': 1, 'ANTL': 2}
        return sorted(ports, key=lambda p: port_order.get(p, 99))

    def get_grid_data(
        self,
        band: str,
        lna_gain_state: str,
        input_port: str
    ) -> Dict[str, Dict[str, Dict]]:
        """
        Get complete grid data for visualization

        Grid structure:
        - Rows: RXOUT1, RXOUT2, RXOUT3, RXOUT4
        - Columns: CA combinations for the band

        Args:
            band: Band name (e.g., 'B1', 'B41')
            lna_gain_state: LNA gain state (e.g., 'G0_H', 'G1')
            input_port: Input port name (e.g., 'ANT1', 'ANT2', 'ANTL')

        Returns:
            Nested dict structure:
            {
                'ca_combination_1': {
                    'RXOUT1': {'frequency': [...], 'gain_db': [...]},
                    'RXOUT2': {'frequency': [...], 'gain_db': [...]},
                    'RXOUT3': {'frequency': [...], 'gain_db': [...]},
                    'RXOUT4': {'frequency': [...], 'gain_db': [...]}
                },
                'ca_combination_2': { ... }
            }
        """
        if not self._is_loaded or self._format_type != 'consolidated':
            raise ValueError("Consolidated format must be loaded first")

        # Get CA combinations for this band
        ca_combinations = self.get_ca_combinations(band)

        # Output ports (rows)
        output_ports = ['RXOUT1', 'RXOUT2', 'RXOUT3', 'RXOUT4']

        result = {}

        for ca_combo in ca_combinations:
            result[ca_combo] = {}

            for output_port in output_ports:
                # Filter data
                filtered = self.data[
                    (self.data['Cfg Band'] == band) &
                    (self.data['debug-nplexer_bank'] == ca_combo) &
                    (self.data['cfg-lna_gain_state'] == lna_gain_state) &
                    (self.data['cfg-active_port_1'] == input_port) &
                    (self.data['cfg-active_port_2'] == output_port)
                ]

                if filtered.empty:
                    result[ca_combo][output_port] = {
                        'frequency': np.array([]),
                        'gain_db': np.array([]),
                        'count': 0
                    }
                else:
                    result[ca_combo][output_port] = {
                        'frequency': filtered['Frequency'].values,
                        'gain_db': filtered['Gain (dB)'].values,
                        'count': len(filtered)
                    }

        return result

    @property
    def frequency_range(self) -> Tuple[float, float]:
        """Frequency range"""
        if not self._is_loaded:
            return None

        if self._format_type == 'consolidated':
            freq = self.data['Frequency']
        else:
            freq = self.data[self.freq_column]

        return (freq.min(), freq.max())

    @property
    def value_range(self) -> Tuple[float, float]:
        """Value range (Gain min/max)"""
        if not self._is_loaded:
            return None

        if self._format_type == 'consolidated':
            values = self.data['Gain (dB)']
        else:
            values = self.data[self.value_column]

        return (values.min(), values.max())

    @property
    def format_type(self) -> Optional[str]:
        """Get current format type ('simple' or 'consolidated')"""
        return self._format_type

    def __repr__(self):
        if self._is_loaded:
            if self._format_type == 'consolidated':
                bands = len(self.data['Cfg Band'].unique())
                paths = len(self.data['Active RF Path'].unique())
                return (f"CsvParser('{self.file_path.name}', "
                        f"format='{self._format_type}', "
                        f"points={len(self.data)}, "
                        f"bands={bands}, paths={paths})")
            else:
                return (f"CsvParser('{self.file_path.name}', "
                        f"format='{self._format_type}', "
                        f"points={len(self.data)}, "
                        f"freq_range={self.frequency_range})")
        return f"CsvParser('{self.file_path.name}', not loaded)"
