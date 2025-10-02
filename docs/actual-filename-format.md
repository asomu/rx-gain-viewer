# 실제 파일명 형식 분석

**작성일**: 2025-10-02
**실제 측정 프로그램 파일명 형식**

---

## 📋 실제 파일명 예시

```
B1[B7]@MHBIN1_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B41S@2_(G0H).s9p
```

---

## 🔍 상세 분해

```
구조:
{MainBand}[{SubBand}]@{Input}_{Output}_{Config1}_{Config2}_{CABands}_{Condition}.s{N}p

분해:
┌─────────────────┬──────────────────────┐
│ B1[B7]          │ 메인 Band + Sub      │
│ @MHBIN1         │ 입력 포트            │
│ _ANTU&ANT1&ANT2 │ 출력 포트 (ANT 조합) │
│ _X@MIMO         │ MIMO 설정            │
│ _X@TRX          │ TRX 설정             │
│ _B3[B7]@1       │ CA Band 1            │
│ _B41S@2         │ CA Band 2            │
│ _(G0H)          │ 측정 조건            │
│ .s9p            │ 9-port               │
└─────────────────┴──────────────────────┘
```

---

## 🎯 추출 요소 (그리드 생성용)

### **1. 메인 Band** → 탭 구분
```
추출: B1
패턴: ^(B\d+)
용도: 탭 생성 (B1 탭, B3 탭, B41 탭)
```

### **2. CA 조건** → 그리드 열(Column)
```
추출: B3[B7], B41
패턴: _B(\d+)(?:\[B\d+\])?(?:S)?@\d+
변환:
  - B3[B7]@1 → "B3_B7"
  - B41S@2   → "B41"
결과: ["B3_B7", "B41"]
용도: 그리드 열 (CA 조건별)
```

### **3. 포트 조합** → 그리드 행(Row)
```
입력 추출: MHBIN1
출력 추출: ANTU&ANT1&ANT2
패턴:
  - 입력: @(MHB?IN\d+)
  - 출력: _(ANT[U\d&]+)
변환:
  - MHBIN1 + ANTU&ANT1&ANT2 → "MHBIN1→ANTU_ANT1_ANT2"
용도: 그리드 행 (포트 조합별)
```

### **4. 측정 조건** → 메타데이터
```
추출: G0H
패턴: _\(([A-Z0-9]+)\)
용도: 차트 제목, 툴팁
```

---

## 📊 그리드 생성 예시

### **파일 리스트:**
```
1. B1[B7]@MHBIN1_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B41S@2_(G0H).s9p
2. B1[B7]@MHBIN1_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B7S@2_(G0H).s9p
3. B1[B7]@MHBIN2_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B41S@2_(G0H).s9p
4. B1[B7]@MHBIN2_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B7S@2_(G0H).s9p
```

### **자동 감지 결과:**

**탭**: B1

**그리드 (B1 탭)**:
```
                    B3_B7_B41   B3_B7_B7
MHBIN1→ANTU_1_2    [file1]     [file2]
MHBIN2→ANTU_1_2    [file3]     [file4]
```

---

## 🔧 정규식 패턴

### **전체 패턴**
```regex
^(B\d+)(?:\[B\d+\])?\@([A-Z0-9]+)_([A-Z0-9&]+)_.*?(_B\d+(?:\[B\d+\])?\@\d+)+_\(([A-Z0-9]+)\)\.s\d+p$
```

### **개별 요소 추출**

#### 1. 메인 Band
```regex
^(B\d+)
→ 예: "B1"
```

#### 2. 입력 포트
```regex
@([A-Z0-9]+)
→ 예: "MHBIN1", "TXIN1"
```

#### 3. 출력 포트
```regex
_([A-Z0-9&]+)
→ 예: "ANTU&ANT1&ANT2"
처리: & 를 _ 로 변경 → "ANTU_ANT1_ANT2"
```

#### 4. CA Band 리스트
```regex
_B(\d+)(?:\[B(\d+)\])?(S)?@(\d+)
→ 예:
  - "B3[B7]@1" → B3, B7
  - "B41S@2"   → B41
조합: "B3_B7", "B41"
```

#### 5. 측정 조건
```regex
_\(([A-Z0-9]+)\)
→ 예: "G0H", "G1L"
```

---

## 💻 Python 파서 구현

```python
import re
from typing import Dict, List, Optional

class ComplexFilenameParser:
    """
    복잡한 측정 파일명 파서
    """

    # 정규식 패턴
    MAIN_BAND_PATTERN = r'^(B\d+)'
    INPUT_PORT_PATTERN = r'@([A-Z0-9]+)_'
    OUTPUT_PORT_PATTERN = r'_([A-Z0-9&]+)_'
    CA_BAND_PATTERN = r'_B(\d+)(?:\[B(\d+)\])?(S)?@(\d+)'
    CONDITION_PATTERN = r'_\(([A-Z0-9]+)\)\.s\d+p$'

    @classmethod
    def parse(cls, filename: str) -> Optional[Dict]:
        """
        파일명 파싱

        Args:
            filename: 파일명

        Returns:
            {
                'main_band': 'B1',
                'input_port': 'MHBIN1',
                'output_port': 'ANTU_ANT1_ANT2',
                'ca_bands': ['B3_B7', 'B41'],
                'condition': 'G0H',
                'original': '원본 파일명'
            }
        """
        try:
            # 메인 Band
            main_band_match = re.search(cls.MAIN_BAND_PATTERN, filename)
            if not main_band_match:
                return None
            main_band = main_band_match.group(1)

            # 입력 포트
            input_match = re.search(cls.INPUT_PORT_PATTERN, filename)
            input_port = input_match.group(1) if input_match else None

            # 출력 포트
            output_match = re.search(cls.OUTPUT_PORT_PATTERN, filename)
            output_port = output_match.group(1).replace('&', '_') if output_match else None

            # CA Bands
            ca_matches = re.findall(cls.CA_BAND_PATTERN, filename)
            ca_bands = []
            for match in ca_matches:
                # match = (main, sub, S, index)
                # B3[B7]@1 → ('3', '7', '', '1')
                # B41S@2   → ('41', '', 'S', '2')
                main = f"B{match[0]}"
                if match[1]:  # Sub-band 있음
                    ca_bands.append(f"{main}_B{match[1]}")
                else:
                    ca_bands.append(main)

            # 측정 조건
            condition_match = re.search(cls.CONDITION_PATTERN, filename)
            condition = condition_match.group(1) if condition_match else None

            # 포트 조합 (행 레이블용)
            port_label = f"{input_port}→{output_port}" if input_port and output_port else None

            return {
                'main_band': main_band,
                'input_port': input_port,
                'output_port': output_port,
                'port_label': port_label,
                'ca_bands': ca_bands,
                'ca_label': '_'.join(ca_bands) if ca_bands else None,
                'condition': condition,
                'original': filename
            }

        except Exception as e:
            print(f"파싱 실패: {filename} - {e}")
            return None

    @classmethod
    def organize_files(cls, files: List) -> Dict:
        """
        파일들을 그리드 구조로 조직화

        Returns:
            {
                'B1': {
                    'ca_conditions': ['B3_B7_B41', 'B3_B7_B7'],
                    'ports': ['MHBIN1→ANTU_ANT1_ANT2', 'MHBIN2→ANTU_ANT1_ANT2'],
                    'matrix': {
                        'MHBIN1→ANTU_ANT1_ANT2': {
                            'B3_B7_B41': file1,
                            'B3_B7_B7': file2
                        },
                        'MHBIN2→ANTU_ANT1_ANT2': {
                            'B3_B7_B41': file3,
                            'B3_B7_B7': file4
                        }
                    }
                }
            }
        """
        from collections import defaultdict

        structure = defaultdict(lambda: {
            'ca_conditions': set(),
            'ports': set(),
            'matrix': defaultdict(dict)
        })

        for file in files:
            parsed = cls.parse(file.name if hasattr(file, 'name') else str(file))
            if not parsed:
                continue

            band = parsed['main_band']
            ca = parsed['ca_label']
            port = parsed['port_label']

            if ca and port:
                structure[band]['ca_conditions'].add(ca)
                structure[band]['ports'].add(port)
                structure[band]['matrix'][port][ca] = file

        # Set → sorted list 변환
        result = {}
        for band, data in structure.items():
            result[band] = {
                'ca_conditions': sorted(data['ca_conditions']),
                'ports': sorted(data['ports']),
                'matrix': dict(data['matrix'])
            }

        return result


# 테스트
if __name__ == '__main__':
    filename = "B1[B7]@MHBIN1_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B41S@2_(G0H).s9p"
    result = ComplexFilenameParser.parse(filename)
    print(result)

    # 출력:
    # {
    #     'main_band': 'B1',
    #     'input_port': 'MHBIN1',
    #     'output_port': 'ANTU_ANT1_ANT2',
    #     'port_label': 'MHBIN1→ANTU_ANT1_ANT2',
    #     'ca_bands': ['B3_B7', 'B41'],
    #     'ca_label': 'B3_B7_B41',
    #     'condition': 'G0H',
    #     'original': 'B1[B7]@MHBIN1_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B41S@2_(G0H).s9p'
    # }
```

---

## 🎨 UI 표시 방식

### **그리드 레이블**

**행(Row) 레이블**: 포트 조합
```
MHBIN1→ANTU_ANT1_ANT2
MHBIN2→ANTU_ANT1_ANT2
TXIN1→ANT1
```

**열(Column) 레이블**: CA 조건
```
B3_B7_B41
B3_B7_B7
B41_B7
```

**차트 제목**:
```
B1: MHBIN1→ANTU_ANT1_ANT2 (B3_B7_B41) [G0H]
```

---

## 📝 업데이트 이력

- 2025-10-02: 실제 파일명 분석 및 파서 구현
