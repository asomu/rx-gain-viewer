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
            band_config: Dictionary mapping band names to (uplink_range, downlink_range) tuples
                        Example: {'B1': ((1920, 1980), (2110, 2170))}
                        For Rx measurements, use downlink; for Tx measurements, use uplink
        """
        self.band_config = band_config or self._default_band_config()
        self.measurement_type = self.get_measurement_type()

    @staticmethod
    def _default_band_config() -> Dict[str, tuple]:
        """
        Complete 3GPP band configurations (MHz) - Based on TS 36.101

        Format: 'Band': ((uplink_min, uplink_max), (downlink_min, downlink_max))

        - FDD bands: Separate uplink/downlink frequencies
        - TDD bands: Same frequency for both (uplink = downlink)
        - GSM bands: Legacy 2G bands (GSM850, GSM900, DCS1800, PCS1900)

        Usage:
        - Rx Gain measurements: Use downlink (second tuple)
        - Tx Power measurements: Use uplink (first tuple)
        """
        return {
            # ==================== GSM Bands (Legacy) ====================
            'GSM850': ((824, 849), (869, 894)),      # Cellular (Americas)
            'GSM900': ((890, 915), (935, 960)),      # Extended GSM (Global)
            'DCS': ((1710, 1785), (1805, 1880)),     # DCS 1800 (Europe/Asia)
            'PCS': ((1850, 1910), (1930, 1990)),     # PCS 1900 (Americas)

            # ==================== LTE FDD Bands ====================
            'B1': ((1920, 1980), (2110, 2170)),      # IMT (Global)
            'B2': ((1850, 1910), (1930, 1990)),      # PCS (Americas)
            'B3': ((1710, 1785), (1805, 1880)),      # DCS (Europe/Asia)
            'B4': ((1710, 1755), (2110, 2155)),      # AWS-1 (Americas)
            'B5': ((824, 849), (869, 894)),          # Cellular (Americas)
            'B7': ((2500, 2570), (2620, 2690)),      # IMT-E (Europe/Asia)
            'B8': ((880, 915), (925, 960)),          # Extended GSM (Global)
            'B11': ((1427.9, 1447.9), (1475.9, 1495.9)),  # Lower PDC (Japan)
            'B12': ((699, 716), (729, 746)),         # Lower SMH (Americas)
            'B13': ((777, 787), (746, 756)),         # Upper SMH (Americas)
            'B14': ((788, 798), (758, 768)),         # Upper SMH (Public Safety)
            'B17': ((704, 716), (734, 746)),         # Lower SMH (Americas)
            'B18': ((815, 830), (860, 875)),         # Lower 800 (Japan)
            'B19': ((830, 845), (875, 890)),         # Upper 800 (Japan)
            'B20': ((832, 862), (791, 821)),         # Digital Dividend (Europe)
            'B21': ((1447.9, 1462.9), (1495.9, 1510.9)),  # Upper PDC (Japan)
            'B25': ((1850, 1915), (1930, 1995)),     # Extended PCS (Americas)
            'B26': ((814, 849), (859, 894)),         # Extended Cellular (Americas)
            'B28': ((703, 748), (758, 803)),         # APT (Asia-Pacific)
            'B30': ((2305, 2315), (2350, 2360)),     # WCS (Americas)
            'B31': ((452.5, 457.5), (462.5, 467.5)), # NMT (South America)
            'B32': ((1452, 1496), (1452, 1496)),     # L-Band SDL (Supplemental Downlink)
            'B65': ((1920, 2010), (2110, 2200)),     # Extended IMT (Global)
            'B66': ((1710, 1780), (2110, 2200)),     # Extended AWS (Americas)
            'B70': ((1695, 1710), (1995, 2020)),     # Supplementary AWS (Americas)
            'B71': ((663, 698), (617, 652)),         # Digital Dividend (Americas)
            'B72': ((451, 456), (461, 466)),         # PMR (Europe)
            'B73': ((450, 455), (460, 465)),         # PMR (Asia-Pacific)
            'B74': ((1427, 1470), (1475, 1518)),     # Lower L-Band (Global)
            'B85': ((698, 716), (728, 746)),         # Extended Lower SMH (Americas)
            'B87': ((410, 415), (420, 425)),         # PMR (Global)
            'B88': ((412, 417), (422, 427)),         # PMR (Global)

            # ==================== LTE TDD Bands ====================
            # TDD bands use same frequency for uplink/downlink (time-multiplexed)
            'B34': ((2010, 2025), (2010, 2025)),     # IMT
            'B37': ((1910, 1930), (1910, 1930)),     # PCS
            'B38': ((2570, 2620), (2570, 2620)),     # IMT-E
            'B39': ((1880, 1920), (1880, 1920)),     # DCS-IMT Gap
            'B40': ((2300, 2400), (2300, 2400)),     # S-Band (Asia)
            'B41': ((2496, 2690), (2496, 2690)),     # BRS (Global)
            'B42': ((3400, 3600), (3400, 3600)),     # CBRS (Global)
            'B43': ((3600, 3800), (3600, 3800)),     # C-Band (Global)
            'B46': ((5150, 5925), (5150, 5925)),     # U-NII (Unlicensed)
            'B48': ((3550, 3700), (3550, 3700)),     # CBRS (Americas)
            'B50': ((1432, 1517), (1432, 1517)),     # L-Band
            'B51': ((1427, 1432), (1427, 1432)),     # L-Band Extension
            'B53': ((2483.5, 2495), (2483.5, 2495)), # S-Band

            # ==================== Custom/Extended Bands ====================
            'B202': ((2483.5, 2500), (2483.5, 2500)),      # Wide-band sweep (Custom)
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
        auto_band: bool = True,
        mapper=None
    ) -> pd.DataFrame:
        """
        Parse single SnP file to DataFrame

        Args:
            snp_file: Path to .s2p file
            freq_filter: Apply band-specific frequency filtering
            auto_band: Auto-detect band from filename
            mapper: Optional BandMapper instance for notation translation

        Returns:
            DataFrame with CSV rows for this file

        Note:
            Subclasses (RxGainParser, TxPowerParser) automatically use
            the correct frequency direction (rx/tx) in filter_frequency()
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
                # Determine direction from measurement type
                direction = 'tx' if self.measurement_type == 'tx_power' else 'rx'
                s_params_df = self.filter_frequency(s_params_df, band, direction)

        # Calculate metrics (pass mapper to subclass)
        result_df = self.calculate_metrics(s_params_df, metadata, mapper=mapper)

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
        # Pattern: B1@1, B1[B7]@2, B41[NA]@3, B1[MHBIN1]@1, etc.
        # Improved: Allow any content in brackets (not just B\d+)
        band_pattern = r'(B\d+(?:\[[^\]]+\])?)\@?(\d+)?'
        for part in parts:
            match = re.search(band_pattern, part)
            if match:
                metadata['band'] = self._extract_primary_band(match.group(1))
                metadata['ca_config'] = match.group(1)  # Full CA config
                if match.group(2):
                    metadata['port_out'] = f'RXOUT{match.group(2)}'
                break

        # Extract LNA state from parentheses
        # Examples: (G0H) → G0_H, (G0) → G0, (G1) → G1, (G2H) → G2_H
        lna_pattern = r'\(([^)]+)\)'
        match = re.search(lna_pattern, name)
        if match:
            lna_raw = match.group(1)
            # Convert G0H → G0_H, G0L → G0_L, G2H → G2_H, etc.
            # Pattern: G + digit + optional H/L → G + digit + _H/_L
            if re.match(r'G\d+[HL]', lna_raw):
                # G0H → G0_H, G2H → G2_H, G0L → G0_L
                metadata['lna_state'] = re.sub(r'(G\d+)([HL])', r'\1_\2', lna_raw)
            else:
                # G0 → G0, G1 → G1 (no suffix)
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

    def filter_frequency(
        self,
        df: pd.DataFrame,
        band: str,
        direction: str = 'rx'
    ) -> pd.DataFrame:
        """
        Filter DataFrame to band-specific frequency range

        Args:
            df: DataFrame with 'frequency' column (in MHz)
            band: Band name (e.g., 'B1', 'GSM900', 'DCS', 'PCS')
            direction: 'rx' for downlink (Rx Gain), 'tx' for uplink (Tx Power)

        Returns:
            Filtered DataFrame

        Examples:
            >>> # Rx Gain measurement (uses downlink)
            >>> df_rx = parser.filter_frequency(df, 'B1', direction='rx')
            >>> # Tx Power measurement (uses uplink)
            >>> df_tx = parser.filter_frequency(df, 'B1', direction='tx')
        """
        if band not in self.band_config:
            return df

        # Get uplink and downlink ranges
        uplink_range, downlink_range = self.band_config[band]

        # Select appropriate range based on measurement direction
        if direction.lower() == 'tx':
            freq_min, freq_max = uplink_range      # Tx uses uplink
        else:  # Default to 'rx'
            freq_min, freq_max = downlink_range    # Rx uses downlink

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
