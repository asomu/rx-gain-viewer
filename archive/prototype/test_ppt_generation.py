#!/usr/bin/env python3
"""
PPT 자동 생성 테스트
기존 템플릿에 슬라이드 추가 + 이미지 삽입
"""

from pathlib import Path
from parsers.csv_parser import CsvParser
from utils.chart_generator import ChartGenerator
from utils.ppt_generator import PptGenerator


def test_ppt_generation():
    """PPT 자동 생성 테스트"""

    print("=" * 70)
    print("PPT Auto-Generation Test")
    print("=" * 70)
    print()

    # CSV 파일 로드
    csv_path = Path("data/Bellagio_POC_Rx.csv")
    parser = CsvParser(csv_path)
    parser.load_consolidated()

    # 테스트 조건 3개
    test_conditions = [
        ("B41", "G0_H", "ANT1"),
        ("B41", "G0_L", "ANT1"),
        ("B41", "G1", "ANT1"),
    ]

    # 출력 디렉토리
    output_dir = Path("ppt_test")
    output_dir.mkdir(exist_ok=True)

    # 1단계: 벡터 이미지 생성 (SVG)
    print("[Step 1/3] Generating vector images (SVG)...")
    image_files = []

    for band, lna, port in test_conditions:
        print(f"  Creating: {band} {lna} {port}")

        grid_data = parser.get_grid_data(band, lna, port)
        fig = ChartGenerator.create_compact_grid(
            grid_data=grid_data,
            band=band,
            lna_gain_state=lna,
            input_port=port,
            compact_size=(250, 150)
        )

        # PNG로 저장 (python-pptx는 SVG 미지원)
        png_path = output_dir / f"{band}_{lna}_{port}.png"
        ChartGenerator.export_to_image(fig, str(png_path), width=1920, height=1200)
        image_files.append(png_path)

    print(f"  [OK] {len(image_files)} images created")
    print()

    # 2단계: PPT 생성
    print("[Step 2/3] Creating PowerPoint...")
    ppt_output = output_dir / "RF_Analysis_Report.pptx"

    # PPT 생성기
    generator = PptGenerator()

    for img_path in image_files:
        # 파일명에서 정보 추출
        stem = img_path.stem
        parts = stem.split('_')
        band = parts[0]
        lna = parts[1]
        port = parts[2]

        title = f"{band} {lna} {port} LNA Gain"
        print(f"  Adding slide: {title}")

        generator.add_slide_with_image(title, img_path)

    generator.save(ppt_output)
    print()

    # 3단계: 결과 확인
    print("[Step 3/3] Results")
    print(f"  Images: {output_dir}/")
    print(f"  PPT: {ppt_output}")
    print()

    print("=" * 70)
    print("Test Complete!")
    print("=" * 70)
    print()
    print("생성된 PPT를 열어보세요:")
    print(f"  {ppt_output.absolute()}")
    print()
    print("각 슬라이드:")
    print("  - 상단: 제목 (Band LNA Port)")
    print("  - 하단: 그리드 차트 (벡터 이미지)")
    print()
    print("만족스러우면 426개 전체를 자동 생성할 수 있습니다!")


if __name__ == "__main__":
    test_ppt_generation()
