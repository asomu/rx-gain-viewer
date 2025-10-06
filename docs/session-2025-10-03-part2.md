# Session Log - 2025-10-03 Part 2

**Duration**: ~1.5 hours (continued session)
**Focus**: 벡터 이미지 export & PPT 자동 생성

---

## 📋 Session Overview

Part 1에서 426개 HTML 그리드 생성 완료 후, PDF 품질 문제 발견 및 PPT 자동화 구현.

---

## 🎯 Achievements

### 1. PDF 품질 문제 해결
**문제**: 기존 PDF가 래스터 이미지(PNG → PDF)라서 확대 시 지글지글

**해결**:
- Plotly의 벡터 PDF 직접 export 발견
- `fig.write_image('file.pdf')` - 벡터 방식
- 확대해도 HTML처럼 선명함!

**결과**:
- PNG (래스터): 213 KB, 확대하면 픽셀 보임
- PDF (벡터): 32 KB, 확대해도 선명
- SVG (벡터): 32 KB, 확대해도 선명

### 2. 이미지 포맷 이해
| 포맷 | 타입 | 확대 품질 | PPT 지원 | 파일 크기 | 용도 |
|------|------|----------|----------|----------|------|
| PNG | 래스터 | ❌ 지글지글 | ✅ 필수 | 213 KB | PPT 삽입용 |
| PDF | 벡터 | ✅ 선명 | ⚠️ 부분적 | 32 KB | 보고서, 문서 |
| SVG | 벡터 | ✅ 선명 | ❌ 미지원 | 32 KB | 웹, 디자인 |

**핵심 발견**:
- PNG는 래스터라 본질적으로 픽셀 기반 → 화질 한계 있음
- SVG로 개선 가능하지만 python-pptx가 SVG 미지원
- PPT 작업은 PNG 필수, 고화질 원하면 해상도 높이기

### 3. PPT 자동 생성 구현 ✅

**설치한 라이브러리**:
```bash
uv pip install python-pptx
# Dependencies: lxml, xlsxwriter
```

**생성한 파일**:
- `prototype/utils/ppt_generator.py` - PPT 생성 클래스
- `prototype/test_ppt_generation.py` - 테스트 스크립트

**주요 기능**:
1. **기존 템플릿 PPT 열기** - 회사 템플릿 사용 가능 ✅
2. **슬라이드 자동 추가** - 제목 + 이미지 삽입
3. **배치 생성** - 여러 이미지 → 하나의 PPT

**테스트 결과**:
- 3장 샘플 PPT 생성 성공
- 위치: `C:\Project\html_exporter\ppt_test\RF_Analysis_Report.pptx`
- 크기: 0.4 MB
- 구조: 제목 (상단) + 그리드 차트 (하단)

---

## 📁 Created Files

### 신규 생성
```
prototype/
├── utils/
│   └── ppt_generator.py          # NEW: PPT 자동 생성 클래스
├── test_vector_pdf.py             # NEW: 벡터 vs 래스터 비교
└── test_ppt_generation.py         # NEW: PPT 자동화 테스트

C:/Project/html_exporter/  (root)
├── vector_pdf_test/               # NEW: 벡터 테스트 결과
│   ├── B41_G0_H_ANT1_RASTER.png   # 래스터 비교용
│   ├── B41_G0_H_ANT1_VECTOR.pdf   # 벡터 PDF (32KB, 깨끗함)
│   └── B41_G0_H_ANT1_VECTOR.svg   # 벡터 SVG (32KB, 깨끗함)
└── ppt_test/                      # NEW: PPT 테스트 결과
    ├── B41_G0_H_ANT1.png
    ├── B41_G0_L_ANT1.png
    ├── B41_G1_ANT1.png
    └── RF_Analysis_Report.pptx    # 3장 샘플
```

---

## 🔧 Code Implementation

### 1. PptGenerator 클래스 (NEW)
**File**: `prototype/utils/ppt_generator.py`

**핵심 메서드**:
```python
class PptGenerator:
    def __init__(self, template_path: Optional[Path] = None):
        """
        기존 템플릿 열기 또는 빈 PPT 생성

        Args:
            template_path: 회사 템플릿 PPT 경로 (None이면 빈 PPT)
        """
        if template_path and template_path.exists():
            self.prs = Presentation(str(template_path))
        else:
            self.prs = Presentation()

    def add_slide_with_image(
        self,
        title: str,
        image_path: Path,
        layout_index: int = 5  # 5 = Blank layout
    ):
        """
        제목 + 이미지 슬라이드 추가
        - 상단: 제목 (Arial, 28pt, Bold)
        - 하단: 이미지 (9인치 너비)
        """
        slide_layout = self.prs.slide_layouts[layout_index]
        slide = self.prs.slides.add_slide(slide_layout)

        # 제목 추가
        title_box = slide.shapes.add_textbox(...)

        # 이미지 추가
        slide.shapes.add_picture(str(image_path), ...)

    def save(self, output_path: Path):
        """PPT 파일 저장"""
        self.prs.save(str(output_path))
```

**템플릿 사용 예시**:
```python
# 기존 회사 템플릿 사용
template_path = Path("company_template.pptx")
generator = PptGenerator(template_path)

# 슬라이드 추가 (기존 슬라이드 유지)
for band, lna, port in conditions:
    title = f"{band} {lna} {port} LNA Gain"
    image = Path(f"{band}_{lna}_{port}.png")
    generator.add_slide_with_image(title, image)

# 저장 (템플릿 + 새 슬라이드들)
generator.save(Path("output.pptx"))
```

### 2. 벡터 Export 활용
**File**: `prototype/utils/chart_generator.py`

**기존 메서드로 벡터 생성 가능**:
```python
# 벡터 PDF (확대해도 선명)
ChartGenerator.export_to_image(
    fig,
    'output.pdf',  # .pdf 확장자
    width=1920,
    height=1200
)

# 벡터 SVG (확대해도 선명, 웹용)
ChartGenerator.export_to_image(
    fig,
    'output.svg',  # .svg 확장자
    width=1920,
    height=1200
)

# 래스터 PNG (PPT용)
ChartGenerator.export_to_image(
    fig,
    'output.png',  # .png 확장자
    width=1920,
    height=1200
)
```

---

## 📊 User Requirements (명확화 및 수정)

### 1. PPT 작업 방식 결정 ✅
**요구사항**:
> "기존에 존재하는 ppt에 페이지를 추가하고 싶은거야. 템플릿도 정해져 있고 title만 상단에 넣고 예를들면 'B1 G0 ANT1 LNA Gain' 이런식으로 넣고 그래프 그리드를 넣고 다시 다음장에 타이틀 바꾸고 한장 넣고"

**구현 상태**: ✅ 완료
- `PptGenerator`가 템플릿 지원
- 기존 슬라이드 유지 + 새 슬라이드 추가
- 제목 형식 커스터마이즈 가능

**선택한 방식**: B (템플릿 사용)
- A: 426개 전체 자동 생성 (1개 PPT에 426 슬라이드)
- **B: 기존 템플릿에 추가** ✅ 사용자 선택
- C: Band별 분리 (B1.pptx, B41.pptx 등)

### 2. 최종 목적 명확화 ✅
**목적**: PPT 보고서 작성
> "ppt에 한장 한장 붙여서 레포트 하고 싶어서"

**구조**:
- 각 조건(Band/LNA/Port)마다 1장의 슬라이드
- 제목: "B41 G0_H ANT1 LNA Gain"
- 내용: 그리드 차트 (4 rows × N columns)
- 총 426장 (데이터 없는 36개 제외)

### 3. 이미지 포맷 선택 ✅
**사용자 질문**:
> "글쎄 잘모르겠다. 그림이라 그런가? 확대하면 지글지글하고 벡터 이미지에 익숙해져서 그런가 화질이 나쁘다고 생각이 된다."
> "그림파일도 방법을 바꿔서 개선되는 지 궁금했어"

**답변**:
- PNG는 래스터 포맷 → 벡터로 못 바꿈
- SVG는 벡터 이미지 포맷 → 확대해도 깨끗함
- 하지만 python-pptx가 SVG 미지원 → PNG 필수

**결정**:
- PPT용: PNG 사용 (필수)
- 고화질 필요 시: 해상도 높이기 (현재 1920x1200)
- 벡터 보관용: PDF/SVG 별도 저장 가능

---

## 💡 Key Learnings

### 1. python-pptx 제약사항
- ✅ PNG, JPG 지원
- ❌ SVG 미지원 (PIL이 SVG 파일 못 읽음)
- ⚠️ PDF 제한적 지원

**에러 경험**:
```
PIL.UnidentifiedImageError: cannot identify image file
```
→ SVG를 PNG로 변경하여 해결

### 2. 벡터 vs 래스터 개념
**벡터 (PDF, SVG)**:
- 수학 공식 기반 그래픽
- 무한 확대 가능
- 파일 크기 작음 (32 KB)
- HTML처럼 선명

**래스터 (PNG, JPG)**:
- 픽셀 기반 이미지
- 해상도 제한
- 확대하면 품질 저하 (지글지글)
- PPT에서 필수

### 3. Plotly Export 포맷
```python
# 확장자로 포맷 자동 결정
fig.write_image('file.png')  # PNG (래스터)
fig.write_image('file.pdf')  # PDF (벡터) ✨
fig.write_image('file.svg')  # SVG (벡터) ✨
```

---

## 📝 Next Session Tasks

### 1. 템플릿 PPT 준비 필요
**사용자가 준비할 것**:
- 회사 템플릿 PPT 파일 업로드
- 슬라이드 레이아웃 번호 확인 (PPT에서 확인)
- 제목/이미지 위치 조정 필요 여부 확인

**레이아웃 번호 확인 방법**:
1. PPT 열기
2. 홈 → 새 슬라이드 → 레이아웃 선택
3. 사용할 레이아웃이 몇 번째인지 확인
4. `layout_index` 파라미터에 지정

### 2. 426장 PPT 자동 생성
**수정할 파일**: `test_ppt_generation.py`

**변경 사항**:
```python
# Before (테스트 3개)
test_conditions = [
    ("B41", "G0_H", "ANT1"),
    ("B41", "G0_L", "ANT1"),
    ("B41", "G1", "ANT1"),
]

# After (전체 426개)
bands = parser.get_available_bands()  # 22
lna_states = parser.get_lna_gain_states()  # 7
input_ports = parser.get_input_ports()  # 3

# 템플릿 경로 설정
template_path = Path("your_template.pptx")  # 사용자 제공

# 전체 생성
for band in bands:
    for lna in lna_states:
        for port in input_ports:
            # PNG 생성 + PPT 추가
```

**예상 시간**:
- PNG 생성: 426개 × 0.4초 ≈ 3분
- PPT 조합: 1분
- **총 약 4분**

### 3. Optional: 고해상도 PNG 생성
**현재**: 1920x1200 (Full HD+, 213 KB)
**옵션**: 3840x2400 (4K UHD, ~850 KB)

**장점**:
- 픽셀 밀도 2배 → 화질 개선
- 확대 시 지글지글 감소

**단점**:
- 파일 크기 4배 증가
- 생성 시간 증가
- PPT 파일 크기 증가

---

## 🔗 Related Files

**Documentation**:
- `docs/session-2025-10-03-part1.md` - CSV 분석 및 그리드 생성
- `docs/session-2025-10-03-part2.md` - This session (벡터 & PPT)
- `docs/csv-format-analysis.md` - CSV structure
- `CLAUDE.md` - Project overview

**Code**:
- `prototype/utils/ppt_generator.py` - NEW: PPT automation
- `prototype/utils/chart_generator.py` - Chart generation
- `prototype/test_ppt_generation.py` - NEW: PPT test
- `prototype/test_vector_pdf.py` - NEW: Vector comparison
- `prototype/generate_all_grids.py` - Batch generation

**Output**:
- `prototype/output_grids/` - 426 HTML files
- `ppt_test/` - Sample PPT (3 slides)
- `vector_pdf_test/` - Vector format comparison

---

## 📌 Important Notes for Next Session

### 1. 폴더 위치 주의
- `vector_pdf_test/` - **Root 위치** (prototype 밖)
- `ppt_test/` - **Root 위치** (prototype 밖)
- 테스트 스크립트를 prototype에서 실행하면 상위 디렉토리에 생성됨

### 2. 템플릿 사용 시 확인 사항
1. **레이아웃 번호**: PPT 템플릿마다 다름 (보통 5=Blank)
2. **제목 위치**: 자동 생성 (0.5", 0.3") vs 템플릿 레이아웃
3. **이미지 크기**: 현재 9인치 너비 고정
4. **기존 슬라이드**: 템플릿의 기존 슬라이드는 유지됨

### 3. 파일 포맷 선택 가이드
| 용도 | 추천 포맷 | 이유 |
|------|----------|------|
| PPT 삽입 | PNG | python-pptx 요구사항 (필수) |
| 인쇄/출력 | PDF | 벡터, 고품질 |
| 웹 게시 | SVG | 벡터, 반응형 |
| 보관/아카이브 | HTML | 인터랙티브, Plotly 원본 |

### 4. 사용자 요구사항 체크리스트
- ✅ 기존 템플릿 PPT에 슬라이드 추가
- ✅ 제목 형식: "{Band} {LNA} {Port} LNA Gain"
- ✅ 한 장씩 추가 (426장)
- ✅ 그리드 차트 삽입
- ⏳ 템플릿 파일 제공 대기
- ⏳ 레이아웃 번호 확인 대기

---

**Session End**: 2025-10-03 Part 2
**Next Session**: 템플릿 PPT 업로드 → 426장 자동 생성 실행
**Estimated Time**: 4-5분 (PNG 생성 + PPT 조합)
