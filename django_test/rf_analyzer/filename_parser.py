"""
복잡한 측정 파일명 파서

파일명 예시:
B1[B7]@MHBIN1_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B41S@2_(G0H).s9p
"""

import re
from typing import Dict, List, Optional
from collections import defaultdict


class ComplexFilenameParser:
    """
    측정 프로그램에서 생성된 복잡한 파일명 파서
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
        파일명에서 정보 추출

        Args:
            filename: 측정 파일명

        Returns:
            {
                'main_band': 'B1',               # 메인 Band (탭 구분용)
                'input_port': 'MHBIN1',          # 입력 포트
                'output_port': 'ANTU_ANT1_ANT2', # 출력 포트 (& → _)
                'port_label': 'MHBIN1→ANTU_ANT1_ANT2',  # 그리드 행 레이블
                'ca_bands': ['B3_B7', 'B41'],    # CA Band 리스트
                'ca_label': 'B3_B7_B41',         # 그리드 열 레이블
                'condition': 'G0H',              # 측정 조건
                'original': '원본 파일명'
            }

            파싱 실패 시 None 반환
        """
        try:
            # 1. 메인 Band 추출
            main_band_match = re.search(cls.MAIN_BAND_PATTERN, filename)
            if not main_band_match:
                return None
            main_band = main_band_match.group(1)

            # 2. 입력 포트 추출
            input_match = re.search(cls.INPUT_PORT_PATTERN, filename)
            input_port = input_match.group(1) if input_match else None

            # 3. 출력 포트 추출 (& → _ 변환)
            output_match = re.search(cls.OUTPUT_PORT_PATTERN, filename)
            output_port = output_match.group(1).replace('&', '_') if output_match else None

            # 4. CA Bands 추출
            ca_matches = re.findall(cls.CA_BAND_PATTERN, filename)
            ca_bands = []
            for match in ca_matches:
                # match = (main, sub, S, index)
                # 예: B3[B7]@1 → ('3', '7', '', '1')
                #     B41S@2   → ('41', '', 'S', '2')
                main = f"B{match[0]}"
                if match[1]:  # Sub-band 존재
                    ca_bands.append(f"{main}_B{match[1]}")
                else:
                    ca_bands.append(main)

            # 5. 측정 조건 추출
            condition_match = re.search(cls.CONDITION_PATTERN, filename)
            condition = condition_match.group(1) if condition_match else None

            # 6. 레이블 생성
            port_label = None
            if input_port and output_port:
                port_label = f"{input_port}→{output_port}"

            ca_label = None
            if ca_bands:
                ca_label = '_'.join(ca_bands)

            return {
                'main_band': main_band,
                'input_port': input_port,
                'output_port': output_port,
                'port_label': port_label,
                'ca_bands': ca_bands,
                'ca_label': ca_label,
                'condition': condition,
                'original': filename,
                'is_valid': True
            }

        except Exception as e:
            # 파싱 실패 시 디버깅 정보 포함
            return {
                'main_band': None,
                'input_port': None,
                'output_port': None,
                'port_label': None,
                'ca_bands': [],
                'ca_label': None,
                'condition': None,
                'original': filename,
                'is_valid': False,
                'error': str(e)
            }

    @classmethod
    def organize_files(cls, files: List) -> Dict:
        """
        업로드된 파일들을 그리드 구조로 조직화

        Args:
            files: 업로드된 파일 객체 리스트 (Django UploadedFile)

        Returns:
            {
                'B1': {
                    'ca_conditions': ['B3_B7_B41', 'B3_B7_B7'],  # 정렬된 리스트
                    'ports': ['MHBIN1→ANTU_ANT1_ANT2', ...],    # 정렬된 리스트
                    'matrix': {
                        'MHBIN1→ANTU_ANT1_ANT2': {
                            'B3_B7_B41': file_object,
                            'B3_B7_B7': file_object
                        },
                        ...
                    },
                    'file_count': 12,
                    'missing_cells': []  # 누락된 셀 정보
                },
                'B3': {...},
                'warnings': [
                    '파싱 실패: invalid_file.snp',
                    'B1 탭: B3_B7_B41 × MHBIN2→ANTU_ANT1_ANT2 파일 누락'
                ],
                'unparsed_files': [...]  # 파싱 실패한 파일 리스트
            }
        """
        structure = defaultdict(lambda: {
            'ca_conditions': set(),
            'ports': set(),
            'matrix': defaultdict(dict),
            'file_count': 0
        })

        warnings = []
        unparsed_files = []

        for file in files:
            filename = file.name if hasattr(file, 'name') else str(file)
            parsed = cls.parse(filename)

            if not parsed or not parsed.get('is_valid'):
                warnings.append(f'파싱 실패: {filename}')
                unparsed_files.append(file)
                continue

            band = parsed['main_band']
            ca = parsed['ca_label']
            port = parsed['port_label']

            if not band or not ca or not port:
                warnings.append(f'정보 부족: {filename}')
                unparsed_files.append(file)
                continue

            # 구조에 추가
            structure[band]['ca_conditions'].add(ca)
            structure[band]['ports'].add(port)
            structure[band]['matrix'][port][ca] = file
            structure[band]['file_count'] += 1

        # Set → sorted list 변환
        result = {}
        for band, data in structure.items():
            ca_list = sorted(data['ca_conditions'])
            port_list = sorted(data['ports'])

            # 누락된 셀 찾기
            missing_cells = []
            for port in port_list:
                for ca in ca_list:
                    if ca not in data['matrix'].get(port, {}):
                        missing_cells.append(f'{ca} × {port}')

            if missing_cells:
                warnings.append(f'{band} 탭: {len(missing_cells)}개 파일 누락')

            result[band] = {
                'ca_conditions': ca_list,
                'ports': port_list,
                'matrix': dict(data['matrix']),
                'file_count': data['file_count'],
                'missing_cells': missing_cells,
                'expected_count': len(ca_list) * len(port_list)
            }

        result['warnings'] = warnings
        result['unparsed_files'] = unparsed_files

        return result

    @classmethod
    def get_summary(cls, organized: Dict) -> str:
        """
        조직화된 파일 구조의 요약 텍스트 생성

        Returns:
            "B1 탭: 4×3 = 12개 (완료) ✓\nB3 탭: 2×2 = 4개 (⚠️ 1개 누락)"
        """
        lines = []
        bands = [k for k in organized.keys() if k not in ['warnings', 'unparsed_files']]

        for band in sorted(bands):
            data = organized[band]
            rows = len(data['ports'])
            cols = len(data['ca_conditions'])
            expected = data['expected_count']
            actual = data['file_count']

            status = '✓' if actual == expected else f'⚠️ {expected - actual}개 누락'
            lines.append(f"{band} 탭: {rows}×{cols} = {actual}/{expected}개 ({status})")

        if organized.get('warnings'):
            lines.append(f"\n경고 {len(organized['warnings'])}개:")
            for warning in organized['warnings'][:5]:  # 최대 5개만 표시
                lines.append(f"  - {warning}")

        return '\n'.join(lines)


# 테스트 코드
if __name__ == '__main__':
    # 테스트 파일명
    test_filename = "B1[B7]@MHBIN1_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B41S@2_(G0H).s9p"

    result = ComplexFilenameParser.parse(test_filename)

    print("파싱 결과:")
    print(f"  메인 Band: {result['main_band']}")
    print(f"  포트 레이블: {result['port_label']}")
    print(f"  CA 레이블: {result['ca_label']}")
    print(f"  CA Bands: {result['ca_bands']}")
    print(f"  측정 조건: {result['condition']}")
    print(f"  유효: {result['is_valid']}")
