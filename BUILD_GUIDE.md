# RF Converter 빌드 가이드

PyInstaller를 사용하여 단일 실행 파일(exe) 생성 방법

---

## 📋 사전 요구사항

### 1. Python 환경
- Python 3.11 이상
- uv 패키지 관리자 (또는 pip)

### 2. 필수 패키지 설치
```bash
# uv 사용 (권장)
uv sync

# PyInstaller가 없다면
uv add pyinstaller
```

---

## 🚀 빌드 방법

### 빠른 빌드 (권장)

```bash
# build.py 스크립트 실행
python build.py
```

또는

```bash
uv run build.py
```

### 수동 빌드

```bash
# PyInstaller 직접 실행
pyinstaller --clean rf_converter.spec
```

---

## 📦 빌드 출력

### 빌드 완료 후 생성되는 파일들

```
dist/
├── RF_Converter.exe    # 실행 파일 (단일 파일)
└── README.txt          # 사용자 가이드
```

### 빌드 디렉토리 (자동 생성/삭제)

```
build/                  # 임시 빌드 파일 (자동 삭제)
__pycache__/           # Python 캐시 (자동 삭제)
```

---

## ⚙️ 빌드 옵션 (rf_converter.spec)

### 최적화 설정

```python
# 단일 파일 모드
onefile = True

# UPX 압축 (파일 크기 30-40% 감소)
upx = True

# Python 최적화 레벨 (0~2, 높을수록 최적화)
optimize = 2

# 콘솔 창 숨기기 (GUI 앱)
console = False
```

### 제외된 모듈 (크기 최적화)

다음 모듈들은 빌드에서 제외되어 파일 크기를 줄입니다:

- `tkinter` - 사용하지 않는 GUI 프레임워크
- `matplotlib` - 사용하지 않는 그래프 라이브러리
- `IPython`, `jupyter` - 개발 도구
- `django` - 웹 앱 (exe에 불필요)
- `scipy` - 과학 계산 라이브러리
- `pytest`, `unittest` - 테스트 도구

### 포함된 데이터 파일

```python
datas = [
    ('rf_converter/icon.ico', '.'),                    # 아이콘
    ('rf_converter/core/mappings', 'core/mappings'),  # 매핑 예제
]
```

---

## 🔧 빌드 최적화 팁

### 1. UPX 압축 사용

**UPX (Ultimate Packer for eXecutables)** 설치로 추가 30-40% 크기 감소:

```bash
# Windows - Chocolatey로 설치
choco install upx

# 또는 수동 다운로드
# https://github.com/upx/upx/releases
```

UPX 설치 후 자동으로 적용됩니다.

### 2. 불필요한 모듈 제외

`rf_converter.spec` 파일의 `excludes` 리스트에 사용하지 않는 모듈 추가:

```python
excludes=[
    'your_unused_module',
    'another_module',
]
```

### 3. Python 최적화 레벨 조정

```python
# spec 파일에서
optimize=2  # 0: 없음, 1: 기본, 2: 최대
```

---

## 📊 예상 빌드 크기

### 최적화 전
- 파일 크기: ~150-200 MB
- 빌드 시간: 2-3분

### 최적화 후 (UPX + optimize=2)
- 파일 크기: ~80-120 MB
- 빌드 시간: 3-4분 (압축 시간 포함)
- 실행 속도: 차이 없음 (압축 해제는 자동)

---

## 🐛 문제 해결

### 1. PyInstaller 에러

**증상**: `ModuleNotFoundError` 또는 import 에러

**해결**:
```python
# spec 파일의 hiddenimports에 누락된 모듈 추가
hiddenimports=[
    'missing_module',
]
```

### 2. UPX 관련 에러

**증상**: UPX 압축 실패

**해결**:
```python
# spec 파일에서 UPX 비활성화
upx=False,
```

### 3. 실행 파일이 백신에 차단됨

**원인**: PyInstaller로 만든 exe는 false positive 가능

**해결**:
- 백신 프로그램에서 예외 추가
- 또는 코드 서명 인증서 구매 (유료)

### 4. 파일 크기가 너무 큼

**해결 방법**:
1. UPX 설치 및 활성화
2. `excludes` 리스트에 불필요한 모듈 추가
3. `optimize=2` 설정 확인

### 5. 빌드는 되는데 실행이 안됨

**체크리스트**:
```bash
# 1. 개발 환경에서 먼저 테스트
python rf_converter/ui_pyqt6/main.py

# 2. 종속성 확인
pip list

# 3. spec 파일의 datas 경로 확인
```

---

## 📝 build.py 스크립트 사용법

### 기본 사용

```bash
python build.py
```

### 스크립트 기능

1. **사전 확인**
   - PyInstaller 설치 여부
   - 아이콘 파일 존재 여부

2. **빌드 디렉토리 정리**
   - 이전 `build/`, `dist/` 폴더 삭제
   - 캐시 파일 정리

3. **PyInstaller 빌드**
   - `rf_converter.spec` 파일 사용
   - 진행 상황 실시간 표시

4. **결과 확인**
   - exe 파일 크기 표시
   - 빌드 시간 측정

5. **배포 문서 생성**
   - `dist/README.txt` 자동 생성

### 출력 예시

```
======================================================================
                    RF Converter 빌드 스크립트
======================================================================

프로젝트: RF Converter v1.1
빌드 타입: 단일 exe 파일 (onefile)
플랫폼: Windows (64-bit)

[Step 0] 사전 확인
✓ PyInstaller 6.17.0 설치됨
✓ 아이콘 파일 확인: rf_converter/icon.ico (12.3 KB)

[Step 1] 이전 빌드 파일 정리
✓ build/ 삭제 완료
✓ dist/ 삭제 완료

[Step 2] PyInstaller 빌드 시작
  spec 파일: rf_converter.spec
  빌드 옵션:
    - 단일 파일 (onefile): ✓
    - GUI 모드 (no console): ✓
    - UPX 압축: ✓
    - Python 최적화 레벨: 2

빌드 명령: python -m PyInstaller --clean rf_converter.spec

  INFO: Building EXE...
  INFO: Analyzing dependencies...
  INFO: Compressing with UPX...

✓ 빌드 완료 (소요 시간: 187.3초)

[Step 3] 빌드 결과 확인
✓ exe 파일 생성 완료!

  파일 정보:
    경로: C:\Python\Project\rx-gain-viewer\dist\RF_Converter.exe
    크기: 95.47 MB (100,123,456 bytes)

  최적화 정보:
    ✓ 적정 크기입니다 (95.5 MB)

[Step 4] 배포 문서 생성
✓ README.txt 생성: dist\README.txt

======================================================================
                            빌드 완료!
======================================================================

✓ RF_Converter.exe 생성 성공

  배포 파일:
    - dist/RF_Converter.exe
    - dist/README.txt

  다음 단계:
    1. dist/RF_Converter.exe 실행하여 테스트
    2. 정상 작동 확인 후 배포
```

---

## 🚀 배포 준비

### 1. 테스트

```bash
# exe 파일 직접 실행
dist\RF_Converter.exe
```

**체크리스트**:
- [ ] 프로그램이 정상 실행되는가?
- [ ] 모든 기능이 작동하는가?
- [ ] 아이콘이 제대로 표시되는가?
- [ ] Band Mapping 기능이 작동하는가?
- [ ] 파일 변환이 정상적으로 되는가?

### 2. 배포 파일 준비

```
RF_Converter_v1.1/
├── RF_Converter.exe
├── README.txt
└── examples/                   # (선택사항)
    └── mappings/
        ├── example_alpha1c_evb1.json
        ├── example_basic.json
        └── example_comprehensive.json
```

### 3. 압축 및 배포

```bash
# 7-Zip 또는 WinRAR로 압축
RF_Converter_v1.1.zip
```

---

## 📌 주의사항

### 빌드 환경
- **반드시 Windows에서 빌드**해야 Windows exe가 생성됩니다
- Linux/Mac에서 빌드하면 해당 OS용 실행 파일이 생성됩니다

### 첫 실행 시간
- PyInstaller로 만든 exe는 첫 실행 시 압축 해제로 인해 5-10초 소요
- 이후 실행은 빠름

### 백신 프로그램
- PyInstaller exe는 백신 프로그램에서 false positive 가능
- 사용자에게 "허용" 처리 안내 필요

### 업데이트
- 새 버전 배포 시 전체 exe 파일 교체 필요
- 자동 업데이트 기능은 별도 구현 필요

---

## 🔗 참고 자료

- [PyInstaller 공식 문서](https://pyinstaller.org/)
- [UPX 공식 사이트](https://upx.github.io/)
- [RF Converter 개발 문서](docs/rf-converter/)

---

**Last Updated**: 2025-11-27
**Build Script Version**: 1.0
