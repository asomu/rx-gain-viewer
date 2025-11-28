"""
RF Converter Build Script
PyInstaller를 사용하여 단일 exe 파일 생성

사용법:
    python build.py
    또는
    uv run build.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import time

# ANSI 색상 코드 (Windows Terminal 지원)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """헤더 출력"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_step(step_num, text):
    """단계 출력"""
    print(f"{Colors.OKCYAN}{Colors.BOLD}[Step {step_num}]{Colors.ENDC} {text}")

def print_success(text):
    """성공 메시지"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    """경고 메시지"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    """에러 메시지"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def check_pyinstaller():
    """PyInstaller 설치 확인"""
    try:
        import PyInstaller
        version = PyInstaller.__version__
        print_success(f"PyInstaller {version} 설치됨")
        return True
    except ImportError:
        print_error("PyInstaller가 설치되지 않았습니다")
        print(f"  설치 명령: {Colors.BOLD}uv add pyinstaller{Colors.ENDC}")
        return False

def check_icon():
    """아이콘 파일 확인"""
    icon_path = Path('rf_converter/icon.ico')
    if icon_path.exists():
        size_kb = icon_path.stat().st_size / 1024
        print_success(f"아이콘 파일 확인: {icon_path} ({size_kb:.1f} KB)")
        return True
    else:
        print_error(f"아이콘 파일 없음: {icon_path}")
        return False

def clean_build_dirs():
    """이전 빌드 디렉토리 정리"""
    print_step(1, "이전 빌드 파일 정리")

    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['RF_Converter.exe']

    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            print(f"  삭제 중: {dir_name}/")
            shutil.rmtree(dir_name, ignore_errors=True)
            print_success(f"{dir_name}/ 삭제 완료")

    for file_name in files_to_clean:
        if Path(file_name).exists():
            print(f"  삭제 중: {file_name}")
            Path(file_name).unlink()
            print_success(f"{file_name} 삭제 완료")

    print()

def run_pyinstaller():
    """PyInstaller 실행"""
    print_step(2, "PyInstaller 빌드 시작")

    # spec 파일 경로
    spec_file = Path('rf_converter.spec')

    if not spec_file.exists():
        print_error(f"spec 파일 없음: {spec_file}")
        return False

    print(f"  spec 파일: {spec_file}")
    print(f"  빌드 옵션:")
    print(f"    - 단일 파일 (onefile): ✓")
    print(f"    - GUI 모드 (no console): ✓")
    print(f"    - UPX 압축: ✓")
    print(f"    - Python 최적화 레벨: 2")
    print()

    # PyInstaller 명령 실행
    cmd = [sys.executable, '-m', 'PyInstaller', '--clean', str(spec_file)]

    print(f"{Colors.BOLD}빌드 명령:{Colors.ENDC} {' '.join(cmd)}\n")

    start_time = time.time()

    try:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # 빌드 로그에서 중요 정보만 출력
        for line in result.stdout.split('\n'):
            if any(keyword in line for keyword in ['INFO', 'WARNING', 'ERROR', 'Building', 'Analyzing']):
                print(f"  {line.strip()}")

        elapsed = time.time() - start_time
        print()
        print_success(f"빌드 완료 (소요 시간: {elapsed:.1f}초)")
        return True

    except subprocess.CalledProcessError as e:
        print_error(f"빌드 실패: {e}")
        print(e.output)
        return False

def check_output():
    """빌드 결과 확인"""
    print_step(3, "빌드 결과 확인")

    exe_path = Path('dist/RF_Converter.exe')

    if not exe_path.exists():
        print_error(f"exe 파일 생성 실패: {exe_path}")
        return False

    # 파일 크기 확인
    size_bytes = exe_path.stat().st_size
    size_mb = size_bytes / (1024 * 1024)

    print_success(f"exe 파일 생성 완료!")
    print(f"\n  {Colors.BOLD}파일 정보:{Colors.ENDC}")
    print(f"    경로: {exe_path.absolute()}")
    print(f"    크기: {size_mb:.2f} MB ({size_bytes:,} bytes)")

    # 최적화 팁
    print(f"\n  {Colors.OKBLUE}최적화 정보:{Colors.ENDC}")
    if size_mb > 100:
        print_warning(f"    파일 크기가 큽니다 ({size_mb:.1f} MB)")
        print(f"    - UPX 압축 활성화됨")
        print(f"    - Python 최적화 레벨 2 적용됨")
    else:
        print_success(f"    적정 크기입니다 ({size_mb:.1f} MB)")

    return True

def create_readme():
    """배포용 README 생성"""
    print_step(4, "배포 문서 생성")

    readme_content = """# RF Converter v1.1

## 실행 방법

`RF_Converter.exe`를 더블클릭하여 실행하세요.

## 시스템 요구사항

- Windows 10 이상 (64-bit)
- 최소 2GB RAM
- 100MB 이상의 여유 디스크 공간

## 주요 기능

- 50개 3GPP 밴드 지원 (LTE/5G NR/GSM)
- 자동 밴드 감지
- 지역 코드 지원 (NA, EU, CN, SA)
- Band Mapping 시스템 (선택사항)
- 배치 변환 및 실시간 진행률
- 설정 자동 저장

## Band Mapping 사용법 (선택사항)

1. "Band Mapping (Optional)" 섹션에서 체크박스 클릭
2. "Browse..." 버튼으로 JSON 매핑 파일 선택
3. 변환 시작

매핑 파일 예제는 프로그램과 함께 제공됩니다.

## 문제 해결

### 실행이 안돼요
- 백신 프로그램에서 차단될 수 있습니다 (허용 처리 필요)
- Windows Defender SmartScreen 경고 → "추가 정보" → "실행" 클릭

### 변환이 느려요
- 대용량 파일은 시간이 걸릴 수 있습니다
- 배치 변환 시 파일 개수가 많으면 수 분 소요 가능

## 로그 위치

변환 로그는 다음 위치에 저장됩니다:
```
%USERPROFILE%\\.rf_converter\\logs\\
```

## 버전 정보

- Version: 1.1
- Build Date: 2025-11-27
- 개발: RF Converter Team

---

© 2025 RF Converter. All rights reserved.
"""

    readme_path = Path('dist/README.txt')
    readme_path.write_text(readme_content, encoding='utf-8')
    print_success(f"README.txt 생성: {readme_path}")

def main():
    """메인 빌드 프로세스"""
    print_header("RF Converter 빌드 스크립트")

    print(f"{Colors.BOLD}프로젝트:{Colors.ENDC} RF Converter v1.1")
    print(f"{Colors.BOLD}빌드 타입:{Colors.ENDC} 단일 exe 파일 (onefile)")
    print(f"{Colors.BOLD}플랫폼:{Colors.ENDC} Windows (64-bit)")
    print()

    # 사전 체크
    print_step("0", "사전 확인")
    if not check_pyinstaller():
        return 1
    if not check_icon():
        print_warning("아이콘 없이 빌드를 계속합니다")
    print()

    # 빌드 프로세스
    clean_build_dirs()

    if not run_pyinstaller():
        print_error("\n빌드 실패!")
        return 1

    print()
    if not check_output():
        return 1

    print()
    create_readme()

    # 완료 메시지
    print_header("빌드 완료!")
    print(f"{Colors.OKGREEN}{Colors.BOLD}✓ RF_Converter.exe 생성 성공{Colors.ENDC}")
    print()
    print(f"  {Colors.BOLD}배포 파일:{Colors.ENDC}")
    print(f"    - dist/RF_Converter.exe")
    print(f"    - dist/README.txt")
    print()
    print(f"  {Colors.BOLD}다음 단계:{Colors.ENDC}")
    print(f"    1. dist/RF_Converter.exe 실행하여 테스트")
    print(f"    2. 정상 작동 확인 후 배포")
    print()

    return 0

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}빌드 취소됨{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
