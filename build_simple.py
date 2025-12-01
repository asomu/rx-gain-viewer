"""
RF Converter 빌드 스크립트 (간단 버전)
다른 프로젝트와 동일한 방식으로 직접 PyInstaller 명령어 실행
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def build():
    """RF Converter 실행 파일 빌드"""

    print("=" * 70)
    print("RF Converter v1.1.0 빌드")
    print("=" * 70)
    print()

    # 프로젝트 루트로 이동
    project_root = Path(__file__).parent
    os.chdir(project_root)

    print(f"작업 디렉토리: {project_root}")
    print()

    # 이전 빌드 삭제
    print("[1/3] 이전 빌드 정리 중...")
    for path in ['build', 'dist']:
        if Path(path).exists():
            shutil.rmtree(path)
            print(f"  - 삭제: {path}/")

    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"  - 삭제: {spec_file}")

    print()

    # PyInstaller 명령어 구성
    print("[2/3] PyInstaller 빌드 중...")
    print()

    pyinstaller_cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=RF_Converter',
        '--windowed',  # GUI 모드 (콘솔창 숨김)
        '--onefile',   # 단일 실행 파일
        '--clean',     # 캐시 정리
        '--noconfirm', # 덮어쓰기 확인 안 함
        '--icon=rf_converter/icon.ico',  # 아이콘
        # 숨겨진 import 추가
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        # RF Converter 모듈 (updated 2025-12-01)
        '--hidden-import=rf_converter.core',
        '--hidden-import=rf_converter.core.services.conversion_service',
        '--hidden-import=rf_converter.core.logger',
        '--hidden-import=rf_converter.core.band_mapper',
        '--hidden-import=rf_converter.core.parsers.base_parser',
        '--hidden-import=rf_converter.core.parsers.rx_parser',
        '--hidden-import=rf_converter.core.parsers.snp_reader',
        '--hidden-import=rf_converter.core.converters.csv_writer',
        '--hidden-import=rf_converter.core.models.conversion_result',
        '--hidden-import=rf_converter.ui_pyqt6',
        '--hidden-import=rf_converter.ui_pyqt6.widgets',
        '--hidden-import=rf_converter.ui_pyqt6.widgets.file_selector',
        '--hidden-import=rf_converter.ui_pyqt6.widgets.progress_widget',
        # 데이터 파일 포함
        '--add-data=rf_converter/icon.ico;.',
        '--add-data=rf_converter/core/mappings;core/mappings',
        # 진입점
        'rf_converter/ui_pyqt6/main.py'
    ]

    print(f"명령어: {' '.join(pyinstaller_cmd)}")
    print()

    # 빌드 실행
    result = subprocess.run(pyinstaller_cmd)

    if result.returncode != 0:
        print()
        print("[ERROR] 빌드 실패!")
        return False

    print()
    print("[3/3] 빌드 결과 확인...")

    exe_path = Path('dist/RF_Converter.exe')
    if not exe_path.exists():
        print("[ERROR] 실행 파일을 찾을 수 없습니다!")
        return False

    file_size = exe_path.stat().st_size / (1024 * 1024)  # MB
    print(f"  ✓ 실행 파일: {exe_path}")
    print(f"  ✓ 파일 크기: {file_size:.1f} MB")
    print()

    print("=" * 70)
    print("[SUCCESS] 빌드 완료!")
    print("=" * 70)
    print()
    print("배포 방법:")
    print("  1. dist/RF_Converter.exe 파일을 사용자에게 배포")
    print("  2. 사용자가 실행하면 바로 사용 가능")
    print()
    print("버전 정보:")
    print("  - 버전: 1.1.0")
    print("  - UPX 압축: 비활성화 (빠른 시작)")
    print("  - 아이콘: 그리드 스타일 (파란색)")
    print()

    return True


if __name__ == '__main__':
    try:
        success = build()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] 에러 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
