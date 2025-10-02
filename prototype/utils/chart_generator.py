"""
Plotly 기반 차트 생성 유틸리티
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class ChartGenerator:
    """
    Plotly를 사용한 인터랙티브 차트 생성
    """

    @staticmethod
    def create_single_chart(
        freq: np.ndarray,
        gain: np.ndarray,
        title: str = "Gain vs Frequency",
        xlabel: str = "Frequency (GHz)",
        ylabel: str = "Gain (dB)",
        line_color: str = "blue"
    ) -> go.Figure:
        """
        단일 Gain 차트 생성

        Args:
            freq: 주파수 배열
            gain: Gain 배열
            title: 차트 제목
            xlabel: X축 레이블
            ylabel: Y축 레이블
            line_color: 선 색상

        Returns:
            Plotly Figure 객체
        """
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=freq,
            y=gain,
            mode='lines',
            name='Gain',
            line=dict(color=line_color, width=2),
            hovertemplate='Freq: %{x:.3f} GHz<br>Gain: %{y:.2f} dB<extra></extra>'
        ))

        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor='center'),
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            hovermode='x unified',
            template='plotly_white',
            height=400
        )

        return fig

    @staticmethod
    def create_grid_layout(
        data_grid: List[List[Dict]],
        row_labels: List[str],
        col_labels: List[str],
        title: str = "S-parameter Analysis Grid",
        subplot_height: int = 300
    ) -> go.Figure:
        """
        그리드 레이아웃으로 여러 차트 배치

        Args:
            data_grid: [행][열] 형태의 데이터
                       각 셀: {'freq': array, 'gain': array, 'label': str}
            row_labels: 행 레이블 리스트 (예: ['RxOut1', 'RxOut2'])
            col_labels: 열 레이블 리스트 (예: ['B1', 'B1_B3'])
            title: 전체 제목
            subplot_height: 서브플롯 높이 (픽셀)

        Returns:
            Plotly Figure 객체

        Example:
            >>> data = [
            ...     [{'freq': f1, 'gain': g1, 'label': 'RxOut1-B1'}, ...],
            ...     [{'freq': f2, 'gain': g2, 'label': 'RxOut2-B1'}, ...]
            ... ]
            >>> fig = ChartGenerator.create_grid_layout(
            ...     data, ['RxOut1', 'RxOut2'], ['B1', 'B1_B3']
            ... )
        """
        rows = len(row_labels)
        cols = len(col_labels)

        # 서브플롯 제목 생성
        subplot_titles = []
        for row_idx in range(rows):
            for col_idx in range(cols):
                subplot_titles.append(f"{row_labels[row_idx]} - {col_labels[col_idx]}")

        # 서브플롯 생성
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=subplot_titles,
            vertical_spacing=0.1,
            horizontal_spacing=0.08
        )

        # 데이터 추가
        for row_idx in range(rows):
            for col_idx in range(cols):
                if row_idx < len(data_grid) and col_idx < len(data_grid[row_idx]):
                    cell_data = data_grid[row_idx][col_idx]

                    if cell_data and 'freq' in cell_data and 'gain' in cell_data:
                        fig.add_trace(
                            go.Scatter(
                                x=cell_data['freq'],
                                y=cell_data['gain'],
                                mode='lines',
                                name=cell_data.get('label', ''),
                                showlegend=False,
                                line=dict(width=2),
                                hovertemplate='Freq: %{x:.3f} GHz<br>Gain: %{y:.2f} dB<extra></extra>'
                            ),
                            row=row_idx + 1,
                            col=col_idx + 1
                        )

        # 레이아웃 설정
        fig.update_xaxes(title_text="Frequency (GHz)")
        fig.update_yaxes(title_text="Gain (dB)")

        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor='center'),
            height=subplot_height * rows,
            hovermode='x unified',
            template='plotly_white'
        )

        return fig

    @staticmethod
    def create_comparison_chart(
        data_list: List[Dict],
        title: str = "Gain Comparison",
        xlabel: str = "Frequency (GHz)",
        ylabel: str = "Gain (dB)"
    ) -> go.Figure:
        """
        여러 데이터 오버레이 비교 차트

        Args:
            data_list: [{'freq': array, 'gain': array, 'label': str, 'color': str}, ...]
            title: 차트 제목
            xlabel: X축 레이블
            ylabel: Y축 레이블

        Returns:
            Plotly Figure 객체
        """
        fig = go.Figure()

        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']

        for idx, data in enumerate(data_list):
            color = data.get('color', colors[idx % len(colors)])
            label = data.get('label', f'Data {idx+1}')

            fig.add_trace(go.Scatter(
                x=data['freq'],
                y=data['gain'],
                mode='lines',
                name=label,
                line=dict(color=color, width=2),
                hovertemplate=f'{label}<br>Freq: %{{x:.3f}} GHz<br>Gain: %{{y:.2f}} dB<extra></extra>'
            ))

        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor='center'),
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            hovermode='x unified',
            template='plotly_white',
            height=500,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )

        return fig

    @staticmethod
    def export_to_html(
        fig: go.Figure,
        output_path: str,
        include_plotlyjs: str = 'cdn',
        auto_open: bool = False
    ) -> None:
        """
        차트를 HTML 파일로 저장

        Args:
            fig: Plotly Figure 객체
            output_path: 출력 파일 경로
            include_plotlyjs: 'cdn', 'inline', True 중 선택
            auto_open: 저장 후 브라우저로 자동 열기
        """
        fig.write_html(
            output_path,
            include_plotlyjs=include_plotlyjs,
            auto_open=auto_open
        )

    @staticmethod
    def export_to_image(
        fig: go.Figure,
        output_path: str,
        width: int = 1200,
        height: int = 800
    ) -> None:
        """
        차트를 이미지로 저장 (PNG, JPG, SVG, PDF)

        Args:
            fig: Plotly Figure 객체
            output_path: 출력 파일 경로 (확장자로 포맷 결정)
            width: 이미지 너비
            height: 이미지 높이

        Note:
            kaleido 패키지 필요: pip install kaleido
        """
        try:
            fig.write_image(output_path, width=width, height=height)
        except Exception as e:
            raise RuntimeError(f"이미지 저장 실패. kaleido 설치 필요: pip install kaleido\nError: {e}")
