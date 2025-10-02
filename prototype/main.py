"""
RF S-parameter Analyzer - Prototype Main Script

간단한 사용 예시:
python main.py --input sample.s10p --output result.html
"""

import argparse
from pathlib import Path
from parsers.snp_parser import SnpParser
from utils.sparameter import SParameterAnalyzer
from utils.chart_generator import ChartGenerator


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='RF S-parameter Analyzer')
    parser.add_argument('--input', '-i', type=str, help='Input SnP file path')
    parser.add_argument('--output', '-o', type=str, default='output.html', help='Output HTML file path')
    parser.add_argument('--port-in', type=int, default=1, help='Input port number')
    parser.add_argument('--port-out', type=int, default=2, help='Output port number')

    args = parser.parse_args()

    if not args.input:
        print("Usage:")
        print("  python main.py --input sample.s10p --output result.html")
        print("\nGenerating demo charts...")
        create_demo_chart()
        return

    # SnP 파일 파싱
    print(f"파일 로드 중: {args.input}")
    snp = SnpParser(args.input)
    snp.load()
    print(f"  - 포트 개수: {snp.num_ports}")
    print(f"  - 주파수 범위: {snp.frequency_range[0]/1e9:.3f} - {snp.frequency_range[1]/1e9:.3f} GHz")

    # Gain 데이터 추출
    freq, gain = snp.get_gain(args.port_in, args.port_out)

    # 주파수 단위 변환 (Hz → GHz)
    freq_ghz = SParameterAnalyzer.convert_frequency_unit(freq, 'Hz', 'GHz')

    # 통계 계산
    stats = SParameterAnalyzer.calculate_gain_statistics(gain)
    print(f"\nGain 통계:")
    print(f"  - 평균: {stats['mean']:.2f} dB")
    print(f"  - 최대: {stats['max']:.2f} dB")
    print(f"  - 최소: {stats['min']:.2f} dB")

    # 차트 생성
    print(f"\n차트 생성 중...")
    band = SParameterAnalyzer.detect_band_from_frequency(freq)
    title = f"Gain (S{args.port_out}{args.port_in}) - {band} Band"

    fig = ChartGenerator.create_single_chart(
        freq=freq_ghz,
        gain=gain,
        title=title,
        xlabel="Frequency (GHz)",
        ylabel="Gain (dB)"
    )

    # HTML 저장
    ChartGenerator.export_to_html(fig, args.output, auto_open=True)
    print(f"[OK] Saved: {args.output}")


def create_demo_chart():
    """
    Generate demo charts (for testing without SnP files)
    """
    import numpy as np

    print("Creating demo charts with synthetic data...")

    # 가상 데이터 생성 (B1 대역 LNA Gain)
    freq_ghz = np.linspace(2.11, 2.17, 100)  # 2.11 ~ 2.17 GHz
    gain_db = 12 + 0.5 * np.sin(2 * np.pi * (freq_ghz - 2.11) / 0.06) + \
              np.random.normal(0, 0.1, 100)  # 12dB 기준 ±0.5dB

    # 단일 차트
    fig_single = ChartGenerator.create_single_chart(
        freq=freq_ghz,
        gain=gain_db,
        title="Demo: B1 Band LNA Gain",
        line_color="blue"
    )
    ChartGenerator.export_to_html(fig_single, 'demo_single.html', auto_open=False)
    print("[OK] demo_single.html created")

    # 비교 차트 (3개 조건)
    data_list = [
        {
            'freq': freq_ghz,
            'gain': gain_db,
            'label': 'B1 Only',
            'color': 'blue'
        },
        {
            'freq': freq_ghz,
            'gain': gain_db - 0.5,
            'label': 'B1_B3 CA',
            'color': 'red'
        },
        {
            'freq': freq_ghz,
            'gain': gain_db - 1.0,
            'label': 'B1_B41 CA',
            'color': 'green'
        }
    ]

    fig_compare = ChartGenerator.create_comparison_chart(
        data_list=data_list,
        title="Demo: CA Condition Comparison"
    )
    ChartGenerator.export_to_html(fig_compare, 'demo_comparison.html', auto_open=False)
    print("[OK] demo_comparison.html created")

    # 그리드 레이아웃 (2×3)
    data_grid = []
    for port_idx in range(2):  # RxOut1, RxOut2
        row = []
        for ca_idx in range(3):  # B1, B1_B3, B1_B41
            gain_offset = -(port_idx * 0.5 + ca_idx * 0.3)
            row.append({
                'freq': freq_ghz,
                'gain': gain_db + gain_offset,
                'label': f'RxOut{port_idx+1}-CA{ca_idx+1}'
            })
        data_grid.append(row)

    fig_grid = ChartGenerator.create_grid_layout(
        data_grid=data_grid,
        row_labels=['RxOut1', 'RxOut2'],
        col_labels=['B1', 'B1_B3', 'B1_B41'],
        title="Demo: 2×3 Grid Layout"
    )
    ChartGenerator.export_to_html(fig_grid, 'demo_grid.html', auto_open=True)
    print("[OK] demo_grid.html created and opened in browser")


if __name__ == '__main__':
    main()
