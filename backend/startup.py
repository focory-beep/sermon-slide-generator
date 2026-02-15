"""
서버 시작 시 실행되는 초기화 스크립트
Google Drive에서 Reference 데이터 자동 다운로드
"""
import os
import gdown
import zipfile
import shutil
from pathlib import Path


def download_reference_data():
    """
    Google Drive에서 Reference.zip 다운로드 및 압축 해제
    이미 존재하면 스킵
    """
    backend_dir = Path(__file__).parent
    reference_dir = backend_dir / "Reference"

    # Reference 폴더가 이미 존재하면 스킵
    if reference_dir.exists() and any(reference_dir.iterdir()):
        print("✅ Reference 데이터가 이미 존재합니다.")
        return True

    print("📥 Reference.zip 다운로드 시작...")

    try:
        # Google Drive ZIP 파일 ID (환경 변수 또는 기본값)
        file_id = os.getenv("REFERENCE_ZIP_ID", "1KHkGUj9WikLdifvc1wg2V_XGVmZTUvXa")

        # ZIP 파일 다운로드 경로
        zip_path = backend_dir / "Reference.zip"

        # Google Drive에서 ZIP 파일 다운로드
        download_url = f"https://drive.google.com/uc?id={file_id}"
        print(f"📂 다운로드 URL: {download_url}")

        gdown.download(
            url=download_url,
            output=str(zip_path),
            quiet=False
        )

        if not zip_path.exists():
            print("⚠️ ZIP 파일 다운로드 실패")
            return False

        print("📦 압축 해제 중...")

        # ZIP 파일 압축 해제
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(backend_dir)

        # ZIP 파일 삭제
        zip_path.unlink()

        # Reference 폴더 확인
        if reference_dir.exists() and any(reference_dir.iterdir()):
            print(f"✅ Reference 데이터 압축 해제 완료: {reference_dir}")
            return True
        else:
            print("⚠️ Reference 폴더가 생성되지 않았습니다.")
            return False

    except Exception as e:
        print(f"❌ Reference 데이터 다운로드 실패: {e}")
        print("⚠️ Reference 데이터 없이 서버를 시작합니다. 일부 기능이 작동하지 않을 수 있습니다.")
        # 실패해도 서버는 시작되도록 함
        return False


def initialize():
    """서버 시작 시 초기화 작업 실행"""
    print("🚀 서버 초기화 시작...")
    download_reference_data()
    print("✅ 서버 초기화 완료!")


if __name__ == "__main__":
    initialize()
