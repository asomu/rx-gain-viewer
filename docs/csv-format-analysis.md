# CSV Format Analysis

**File**: `data/Bellagio_POC_Rx.csv`
**Purpose**: Consolidated measurement data from multiple SnP files
**Created**: 2025-10-03

---

## File Overview

- **Size**: 111 MB
- **Total Rows**: 109,884 (including header)
- **Total Columns**: 89
- **Data Rows**: 109,883 measurement points
- **Unique Bands**: 22 (B1, B2, B3, B4, B7, B11, B21, B25, B30, B32, B34, B38, B39, B40, B40a, B41, B53, B66, B202, n70, n75, n76)
- **Active RF Paths**: 12 unique port combinations

---

## Column Structure (89 Columns)

### Core Measurement Columns (1-15)

| Column | Name | Type | Description | Example |
|--------|------|------|-------------|---------|
| 1 | Freq Type | string | Frequency band type | `IB` (In-Band) |
| 2 | RAT | string | Radio Access Technology | `LTE` |
| 3 | Cfg Band | string | Configuration Band | `B1`, `B3`, `B41` |
| 4 | Debug Band | string | Debug Band (same as Cfg) | `B1` |
| 5 | Frequency | float | Frequency in MHz | `2110`, `2111`, `2112` |
| 6 | Active RF Path | string | Port mapping code ⭐ | `S0706` |
| 7 | Gain (dB) | float | **Primary measurement** | `16.466` |
| 8 | Reverse (dB) | float | Reverse isolation | `-41.231` |
| 9 | Input RL (dB) | float | Input Return Loss | `-9.752` |
| 10 | Output RL (dB) | float | Output Return Loss | `-25.702` |
| 11-15 | Rx Ib Gain Spec * | various | Gain specifications | Spec limits |

### Isolation Measurements (16-62)

47 columns containing isolation and return loss measurements between all port combinations:

**ANT Ports**: ANT1 (S6), ANT2 (S5), ANTL (S2)
**RX Ports**: RXOUT1 (S7), RXOUT2 (S3), RXOUT3 (S8), RXOUT4 (S4)

| Column Range | Measurement Type | Example Column |
|--------------|------------------|----------------|
| 16-21 | ANT1 isolations | `Isolation ANT1 to RXOUT1 S7_6 (dB)` |
| 22-28 | ANT2 isolations | `Isolation ANT2 to RXOUT1 S7_5 (dB)` |
| 29-35 | ANTL isolations | `Isolation ANTL to RXOUT1 S7_2 (dB)` |
| 36-41 | RXOUT1 isolations | `Isolation RXOUT1 to RXOUT2 S3_7 (dB)` |
| 42-48 | RXOUT2 isolations | `RL RXOUT2 to RXOUT2 S3_3 (dB)` |
| 49-55 | RXOUT3 isolations | `RL RXOUT3 to RXOUT3 S8_8 (dB)` |
| 56-62 | RXOUT4 isolations | `RL RXOUT4 to RXOUT4 S4_4 (dB)` |
| 88-89 | Additional RLs | `RL RXOUT1 to RXOUT1 S7_7 (dB)`, `RL ANT1 to ANT1 S6_6 (dB)` |

### Component Metadata (63-67)

| Column | Name | Example Value |
|--------|------|---------------|
| 63 | component_name | `DSM_HB` |
| 64 | component_vendor | `BROADCOM` |
| 65 | component_version | `POC` |
| 66 | vendor_partnumber | `AFEM-8293-AP1` |
| 67 | snp | `8` (s8p file) |

### Test Configuration (68-70)

| Column | Name | Description |
|--------|------|-------------|
| 68 | auto-testconfig_id | Test configuration ID |
| 69 | aux-auxfile_IB_sparams | Path to original In-Band SnP file |
| 70 | aux-auxfile_OB_sparams | Path to original Out-of-Band SnP file |

**Example SnP Path**:
```
/Users/apple/Documents/Prometheus/Vegas/HBDSM/OUTPUT/BRCM/tests_2025-08-07_18-36-38/
Small_Signal_CNS_2_dut_2025-08-07_18-36-38/
1_auxfile_IB_sparams_Aadil_Test_now_Ali_Test_20250807_183737.873240.s8p
```

### Measurement Configuration (71-87)

| Column | Name | Type | Example | Description |
|--------|------|------|---------|-------------|
| 71 | cfg-rat | string | `LTE` | Radio Access Technology |
| 72 | debug-rat | string | `LTE` | Debug RAT |
| 73 | cfg-rx_band | int | `1` | RX Band number |
| 74 | debug-band | string | `B1` | Debug band label |
| 75 | debug-filter | string | `B1RX` | Filter configuration |
| 76 | debug-nplexer_bank | string | `1_3_40_32+7` | N-plexer bank |
| 77 | debug-module_output | string | `RXOUT1` | Module output port |
| 78 | Measurement Time (s) | float | `14.828` | Measurement duration |
| 79 | cfg-active_port_1 | **string** | `ANT1` | ⭐ **Input port name** |
| 80 | cfg-active_port_2 | **string** | `RXOUT1` | ⭐ **Output port name** |
| 81 | cfg-supply_01-voltage_domain | string | `Vcc` | Voltage domain |
| 82 | cfg-supply_01-voltage_target-V | float | `4` | Supply voltage |
| 83 | cfg-lna_gain_state | string | `G0_H` | LNA gain state ⭐ |
| 84 | cfg-instr_01-start_frequency-MHz | int | `2110` | Start frequency |
| 85 | cfg-instr_01-stop_frequency-MHz | int | `2170` | Stop frequency |
| 86 | cfg-evb_route_rx | string | `DSM_HB-LTE-B1-...` | EVB routing |
| 87 | cfg-target_power-dBm | int | `-90` | Target power |

---

## Active RF Path Mapping ⭐

The `Active RF Path` column (col 6) uses S-parameter notation `S[output][input]` where:
- **First 2 digits**: Output port (S-parameter row index)
- **Last 2 digits**: Input port (S-parameter column index)

### Port Index to Name Mapping

| Index | Port Name | Type | S-param Notation |
|-------|-----------|------|------------------|
| 2 | ANTL | Input | S_2 |
| 3 | RXOUT2 | Output | S3_ |
| 4 | RXOUT4 | Output | S4_ |
| 5 | ANT2 | Input | S_5 |
| 6 | ANT1 | Input | S_6 |
| 7 | RXOUT1 | Output | S7_ |
| 8 | RXOUT3 | Output | S8_ |

### Complete Active RF Path Reference

| Active RF Path | Input Port | Output Port | Gain Column | Use Case |
|----------------|------------|-------------|-------------|----------|
| **S0706** | **ANT1** | **RXOUT1** | **Col 7** | Primary RX path ⭐ |
| **S0705** | **ANT2** | **RXOUT1** | **Col 7** | Secondary RX path |
| S0702 | ANTL | RXOUT1 | Col 7 | Low band RX |
| S0306 | ANT1 | RXOUT2 | Col 7 | RX diversity |
| S0305 | ANT2 | RXOUT2 | Col 7 | RX diversity |
| S0302 | ANTL | RXOUT2 | Col 7 | RX diversity |
| S0806 | ANT1 | RXOUT3 | Col 7 | Additional RX |
| S0805 | ANT2 | RXOUT3 | Col 7 | Additional RX |
| S0802 | ANTL | RXOUT3 | Col 7 | Additional RX |
| S0406 | ANT1 | RXOUT4 | Col 7 | Additional RX |
| S0405 | ANT2 | RXOUT4 | Col 7 | Additional RX |
| S0402 | ANTL | RXOUT4 | Col 7 | Additional RX |

**Note**: The Gain (dB) value in column 7 corresponds to the Gain measurement for the specified Active RF Path.

---

## Data Organization for Grid Layout

### Grid Structure Mapping

**Tabs** (Band-based):
- Extract from `Cfg Band` (column 3)
- Group: B1, B3, B7, B41, etc.

**Rows** (Port combinations):
- Extract from `cfg-active_port_1` → `cfg-active_port_2` (columns 79-80)
- Format: `ANT1→RXOUT1`, `ANT2→RXOUT1`, `ANTL→RXOUT1`, etc.
- Alternative: Use `Active RF Path` (column 6) as row identifier

**Columns** (CA conditions):
- **Issue**: CSV does not contain explicit CA band information
- **Workaround**: Use `cfg-lna_gain_state` (column 83) or other configuration parameters
- **Alternative**: Single column per band (no CA comparison in CSV format)

**Cell Data**:
- X-axis: Frequency (column 5)
- Y-axis: Gain (dB) (column 7)
- Filter: `Cfg Band` + `Active RF Path` combination

---

## Data Extraction Examples

### Example 1: Extract B1 Band, ANT1→RXOUT1 Data

```python
import pandas as pd

df = pd.read_csv('data/Bellagio_POC_Rx.csv')

# Filter for B1 band and S0706 (ANT1→RXOUT1)
b1_ant1_rxout1 = df[
    (df['Cfg Band'] == 'B1') &
    (df['Active RF Path'] == 'S0706')
]

# Extract frequency and gain
frequency = b1_ant1_rxout1['Frequency'].values
gain_db = b1_ant1_rxout1['Gain (dB)'].values

# Result: ~60 frequency points from 2110-2170 MHz
# Gain range: ~16-17 dB
```

### Example 2: Get All Port Combinations for B1

```python
# Find all unique port combinations for B1
b1_data = df[df['Cfg Band'] == 'B1']
port_combinations = b1_data[['Active RF Path', 'cfg-active_port_1', 'cfg-active_port_2']].drop_duplicates()

# Expected result:
# S0706, ANT1, RXOUT1
# S0705, ANT2, RXOUT1
# S0702, ANTL, RXOUT1
# ... (12 combinations)
```

### Example 3: Band Frequency Range Detection

```python
# Auto-detect frequency range for each band
band_ranges = df.groupby('Cfg Band')['Frequency'].agg(['min', 'max'])

# B1: 2110-2170 MHz
# B3: [frequency range]
# B7: [frequency range]
```

---

## CSV vs SnP File Comparison

| Feature | CSV File | SnP File |
|---------|----------|----------|
| **Data Source** | Consolidated | Individual measurement |
| **File Size** | 111 MB (all bands) | ~1 MB (single config) |
| **Bands** | 22 bands in one file | Single band per file |
| **Port Combinations** | 12 paths in one file | Single path per file |
| **Gain Data** | Pre-computed (column 7) | Requires S21 extraction |
| **CA Conditions** | Not explicit | Filename parsing |
| **Parsing Complexity** | Column extraction | scikit-rf library |
| **Use Case** | Batch analysis | Individual file analysis |

---

## Implementation Notes for Parser

### Required Functionality

1. **Column Mapping**:
   - Map column names to indices for robust parsing
   - Handle potential column reordering

2. **Port Label Conversion**:
   - Convert `Active RF Path` → human-readable labels
   - Example: `S0706` → `ANT1→RXOUT1`

3. **Data Filtering**:
   - Filter by Band (column 3)
   - Filter by Active RF Path (column 6)
   - Optional: Filter by LNA gain state (column 83)

4. **Grid Structure Generation**:
   - Group by Band (tabs)
   - Group by Port combination (rows)
   - Single column per band (no CA in CSV)

5. **Frequency Range Handling**:
   - Different bands have different frequency ranges
   - Auto-detect min/max for X-axis scaling

### Parser Output Format

```python
{
    'band': 'B1',
    'port_label': 'ANT1→RXOUT1',
    'active_rf_path': 'S0706',
    'lna_gain_state': 'G0_H',
    'frequency': np.array([2110, 2111, 2112, ...]),
    'gain_db': np.array([16.466, 16.444, 16.443, ...]),
    'component': 'BROADCOM AFEM-8293-AP1',
    'original_snp': '1_auxfile_IB_sparams_...s8p'
}
```

---

## Key Differences from SnP Filename Parsing

### SnP Filename Format (from previous docs)
```
B1[B7]@MHBIN1_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B41S@2_(G0H).s9p
```
- **Contains**: Main band, CA bands, port configuration, condition
- **Missing in CSV**: Explicit CA band information
- **Grid columns**: CA conditions extracted from filename

### CSV Format
```
Row data with 89 columns
```
- **Contains**: Pre-computed measurements, all ports, multiple bands
- **Missing**: CA band information (single measurement condition)
- **Grid columns**: Could use LNA gain state or single column per band

### Recommendation

For CSV-based analysis:
- **Tabs**: Bands (B1, B3, B7, etc.)
- **Rows**: Port combinations (ANT1→RXOUT1, ANT2→RXOUT1, etc.)
- **Columns**: LNA gain states (G0_H, G0_M, G0_L) if available, otherwise single column

For SnP file analysis:
- **Tabs**: Main bands
- **Rows**: Port combinations from filename
- **Columns**: CA conditions from filename

---

## Next Steps

1. ✅ **Document CSV structure** (this file)
2. ⏳ **Update CSV parser** to handle 89-column format
3. ⏳ **Implement filtering** by Band + Active RF Path
4. ⏳ **Test with B1 data** to validate parsing
5. ⏳ **Integrate with chart generator** for grid layout
6. ⏳ **Handle both CSV and SnP** in Django views

---

**Created**: 2025-10-03
**Author**: Claude Code
**Related**: [actual-filename-format.md](actual-filename-format.md), [tech-stack-decision.md](tech-stack-decision.md)
