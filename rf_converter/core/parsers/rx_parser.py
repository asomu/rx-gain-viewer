"""Rx Gain measurement parser"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from .base_parser import BaseMeasurementParser


class RxGainParser(BaseMeasurementParser):
    """
    Parser for Rx Gain measurements

    Calculates:
    - Gain (dB) from S21
    - Reverse Isolation (dB) from S12
    - Input Return Loss (dB) from S11
    - Output Return Loss (dB) from S22
    """

    def get_measurement_type(self) -> str:
        return 'rx_gain'

    def get_required_s_parameters(self) -> List[str]:
        return ['S21', 'S12', 'S11', 'S22']

    def calculate_metrics(self, s_params_df: pd.DataFrame, metadata: Dict, mapper=None) -> pd.DataFrame:
        """
        Calculate Rx Gain metrics from S-parameters

        S21: Forward transmission (Gain)
        S12: Reverse transmission (Isolation)
        S11: Input reflection (Return Loss)
        S22: Output reflection (Return Loss)

        Args:
            s_params_df: DataFrame with S-parameter data
            metadata: File metadata (band, ports, etc.)
            mapper: Optional BandMapper instance for notation translation
        """
        df = s_params_df.copy()

        # Calculate magnitudes from real/imaginary
        df['S21_mag'] = np.sqrt(df['S21_re']**2 + df['S21_im']**2)
        df['S12_mag'] = np.sqrt(df['S12_re']**2 + df['S12_im']**2)
        df['S11_mag'] = np.sqrt(df['S11_re']**2 + df['S11_im']**2)
        df['S22_mag'] = np.sqrt(df['S22_re']**2 + df['S22_im']**2)

        # Convert to dB
        # Gain = 20*log10(|S21|)
        df['Gain (dB)'] = 20 * np.log10(df['S21_mag'].replace(0, np.nan))

        # Reverse Isolation = 20*log10(|S12|)
        df['Reverse (dB)'] = 20 * np.log10(df['S12_mag'].replace(0, np.nan))

        # Return Loss = -20*log10(|S11|) for positive RL values
        # Or 20*log10(|S11|) for negative values (reflection coefficient)
        df['Input RL (dB)'] = -20 * np.log10(df['S11_mag'].replace(0, np.nan))
        df['Output RL (dB)'] = -20 * np.log10(df['S22_mag'].replace(0, np.nan))

        # Add metadata columns
        df['Freq Type'] = 'IB'  # In-Band
        df['RAT'] = 'LTE'
        df['Cfg Band'] = metadata.get('band', 'Unknown')
        df['Debug Band'] = metadata.get('band', 'Unknown')
        df['Active RF Path'] = self.map_port_to_s_notation(
            metadata.get('port_in', 'ANT1'),
            metadata.get('port_out', 'RXOUT1')
        )
        df['cfg_lna_gain_state'] = metadata.get('lna_state', 'Unknown')
        df['cfg_active_port_1'] = metadata.get('port_in', 'ANT1')
        df['cfg_active_port_2'] = metadata.get('port_out', 'RXOUT1')

        # Original band notation from filename
        ca_config = metadata.get('ca_config', metadata.get('band', ''))
        df['ca_config'] = ca_config

        # Mapped N-plexer bank notation (if mapper enabled)
        if mapper and mapper.is_loaded():
            df['debug-nplexer_bank'] = mapper.map(ca_config)
        else:
            df['debug-nplexer_bank'] = ''  # Empty if mapping not enabled

        # Rename frequency column
        df = df.rename(columns={'frequency': 'Frequency'})

        # Select columns in correct order
        columns = self.get_csv_columns()
        available_columns = [col for col in columns if col in df.columns]

        return df[available_columns]

    def get_csv_columns(self) -> List[str]:
        """
        Return CSV columns matching Bellagio_POC_Rx.csv format

        Note: This is a simplified version. Full Bellagio CSV has 89 columns.
        Extended columns can be added as needed.
        """
        return [
            'Freq Type',
            'RAT',
            'Cfg Band',
            'Debug Band',
            'Frequency',
            'Active RF Path',
            'Gain (dB)',
            'Reverse (dB)',
            'Input RL (dB)',
            'Output RL (dB)',
            'cfg_lna_gain_state',
            'cfg_active_port_1',
            'cfg_active_port_2',
            'ca_config',              # Original band notation from filename
            'debug-nplexer_bank',     # Mapped N-plexer bank notation (optional)
            # Additional columns from Bellagio format can be added here:
            # 'Isolation(B3):S0306 (dB)',
            # 'RL ANT1 to ANT1 (dB)',
            # ... (85 more columns)
        ]
