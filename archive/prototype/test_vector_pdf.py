#!/usr/bin/env python3
"""
벡터 PDF export 테스트
PNG 래스터 방식과 벡터 PDF 직접 export 비교
"""

from pathlib import Path
from parsers.csv_parser import CsvParser
from utils.chart_generator import ChartGenerator

def test_vector_pdf():
    """벡터 PDF vs 래스터 PNG 비교"""

    print("=" * 70)
    print("Vector PDF Export Test")
    print("=" * 70)
    print()

    # CSV 파일 로드
    csv_path = Path("data/Bellagio_POC_Rx.csv")
    if not csv_path.exists():
        print(f"[ERROR] CSV file not found: {csv_path}")
        return

    parser = CsvParser(csv_path)
    parser.load_consolidated()  # Load consolidated format

    # 테스트 조건
    band = "B41"
    lna = "G0_H"
    port = "ANT1"

    print(f"Test Condition: {band} / {lna} / {port}")
    print()

    # 그리드 데이터 가져오기
    grid_data = parser.get_grid_data(band, lna, port)

    if not grid_data:
        print(f"[ERROR] No data found for {band}/{lna}/{port}")
        return

    # 차트 생성
    print("[1/3] Creating chart...")
    fig = ChartGenerator.create_compact_grid(
        grid_data=grid_data,
        band=band,
        lna_gain_state=lna,
        input_port=port,
        compact_size=(250, 150)
    )

    # 출력 디렉토리
    output_dir = Path("vector_pdf_test")
    output_dir.mkdir(exist_ok=True)

    # 방법 1: 래스터 PNG (기존 방식)
    print("[2/3] Exporting RASTER PNG (current method)...")
    png_path = output_dir / f"{band}_{lna}_{port}_RASTER.png"
    ChartGenerator.export_to_image(
        fig,
        str(png_path),
        width=1920,
        height=1200
    )
    png_size = png_path.stat().st_size / 1024
    print(f"  [OK] PNG saved: {png_path.name}")
    print(f"       Size: {png_size:.1f} KB")
    print(f"       Type: Raster image (픽셀 기반, 확대하면 지글지글)")
    print()

    # 방법 2: 벡터 PDF (직접 export)
    print("[3/3] Exporting VECTOR PDF (new method)...")
    pdf_path = output_dir / f"{band}_{lna}_{port}_VECTOR.pdf"
    ChartGenerator.export_to_image(
        fig,
        str(pdf_path),
        width=1920,
        height=1200
    )
    pdf_size = pdf_path.stat().st_size / 1024
    print(f"  [OK] PDF saved: {pdf_path.name}")
    print(f"       Size: {pdf_size:.1f} KB")
    print(f"       Type: Vector graphics (벡터 기반, 확대해도 깨끗함)")
    print()

    print("=" * 70)
    print("Test Complete!")
    print("=" * 70)
    print()
    print("파일 비교:")
    print(f"  RASTER PNG: {png_path}")
    print(f"  VECTOR PDF: {pdf_path}")
    print()
    print("각 파일을 열어서 확대(zoom in)해보세요:")
    print("  - PNG: 확대하면 픽셀이 보이고 지글지글함")
    print("  - PDF: 확대해도 선명함 (벡터 방식)")
    print()
    print("이 벡터 PDF 방식이 마음에 드시면,")
    print("모든 426개 파일을 벡터 PDF로 생성하겠습니다!")

if __name__ == "__main__":
    test_vector_pdf()
