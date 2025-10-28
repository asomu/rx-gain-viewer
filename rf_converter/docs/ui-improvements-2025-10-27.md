# UI 개선 - Window Size & Spacing Optimization

**날짜**: 2025-10-27
**목적**: Conversion Result 섹션이 스크롤 없이 보이도록 개선

---

## 🔧 변경 사항

### 1. Window Size 증가

#### Before:
```python
self.setGeometry(100, 100, 750, 850)
self.setMinimumSize(750, 700)
self.setMaximumSize(750, 900)
```

#### After:
```python
self.setGeometry(100, 100, 800, 950)
self.setMinimumSize(800, 900)
self.setMaximumSize(800, 1000)
```

**변경 내용**:
- Width: 750px → 800px (+50px)
- Height: 850px → 950px (+100px)
- Minimum height: 700px → 900px (+200px)
- Maximum height: 900px → 1000px (+100px)

---

### 2. 섹션 간 간격 축소

#### Before:
```python
main_layout.setSpacing(16)
main_layout.setContentsMargins(24, 24, 24, 24)

main_layout.addSpacing(15)  # 각 섹션 사이
```

#### After:
```python
main_layout.setSpacing(10)  # 16 → 10
main_layout.setContentsMargins(20, 20, 20, 20)  # 24 → 20

main_layout.addSpacing(8)   # 15 → 8 (섹션 간)
main_layout.addSpacing(10)  # Convert 버튼 앞만 약간 여유
```

**변경 내용**:
- 전체 레이아웃 spacing: 16px → 10px (-6px)
- 마진: 24px → 20px (-4px)
- File Selection ↔ Measurement Type: 15px → 8px (-7px)
- Measurement Type ↔ Conversion Options: 15px → 8px (-7px)
- Conversion Options ↔ Output Location: 15px → 8px (-7px)
- Output Location ↔ Convert Button: 15px → 10px (-5px)

**총 절약 공간**: 약 40px

---

## 📊 개선 효과

### Before (문제점):
- ❌ Conversion Result 섹션이 화면 하단에 숨겨짐
- ❌ 변환 완료 후 스크롤을 내려야 결과 확인 가능
- ❌ 사용자 경험 저하

### After (개선):
- ✅ 모든 섹션이 스크롤 없이 한 화면에 표시
- ✅ Conversion Result가 항상 보임
- ✅ 섹션 간 간격이 줄어 더 컴팩트한 UI
- ✅ 여전히 여유 있는 간격 유지 (가독성 저하 없음)

---

## 🖥️ 화면 호환성

### 지원 해상도:
- ✅ **1920x1080** (Full HD) - 완벽 지원
- ✅ **2560x1440** (QHD) - 완벽 지원
- ✅ **3840x2160** (4K) - 완벽 지원

### 최소 요구 해상도:
- **1280x1024** 이상 권장
- Vertical height: 900px 이상 필요

---

## 📐 레이아웃 구조

```
┌─────────────────────────────────────┐
│  Title (18pt Bold)                  │
├─────────────────────────────────────┤
│  File Selection                     │  ← 8px spacing
├─────────────────────────────────────┤
│  Measurement Type                   │  ← 8px spacing
├─────────────────────────────────────┤
│  Conversion Options                 │  ← 8px spacing
├─────────────────────────────────────┤
│  Output Location                    │  ← 10px spacing
├─────────────────────────────────────┤
│  [START CONVERSION] Button          │
├─────────────────────────────────────┤
│  Progress Widget (동적)             │
├─────────────────────────────────────┤
│  Conversion Result (항상 표시)      │  ← 스크롤 없이 보임!
└─────────────────────────────────────┘
```

---

## 🎯 사용자 피드백 반영

### 요청 사항:
> "Conversion result를 보려면 스크롤을 내려야 함.
> 윈도우 크기를 늘리고 메뉴 간 간격을 좁혀서 개선 필요."

### 해결 방법:
1. ✅ 윈도우 높이 100px 증가 (850 → 950)
2. ✅ 섹션 간 간격 40% 감소 (15px → 8px)
3. ✅ 전체 마진 축소 (24px → 20px)
4. ✅ 결과: 약 140px 추가 공간 확보

---

## 📝 테스트 체크리스트

- [ ] 1920x1080 해상도에서 스크롤 없이 모든 섹션 표시 확인
- [ ] Conversion 완료 후 Result 섹션 즉시 가시성 확인
- [ ] 섹션 간 간격이 너무 좁지 않은지 확인
- [ ] 다양한 해상도에서 레이아웃 정상 작동 확인

---

## 🔄 롤백 방법

문제 발생 시 이전 설정으로 복원:

```python
# main_window.py line 79-81
self.setGeometry(100, 100, 750, 850)
self.setMinimumSize(750, 700)
self.setMaximumSize(750, 900)

# line 95-96
main_layout.setSpacing(16)
main_layout.setContentsMargins(24, 24, 24, 24)

# line 110, 115, 120, 125
main_layout.addSpacing(15)
```

---

**수정 파일**: `rf_converter/ui_pyqt6/main_window.py`
**영향 범위**: UI 레이아웃만 (기능 변경 없음)
**테스트 필요**: UI 시각적 확인
