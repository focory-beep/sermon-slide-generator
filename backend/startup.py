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
    Google Drive에서 Reference 폴더 다운로드
    이미 존재하면 스킵
    """
    backend_dir = Path(__file__).parent
    reference_dir = backend_dir / "Reference"

    # Reference 폴더가 이미 존재하면 스킵
    if reference_dir.exists() and any(reference_dir.iterdir()):
        print("✅ Reference 데이터가 이미 존재합니다.")
        return True

    print("📥 Reference 데이터 다운로드 시작...")

    try:
        # Google Drive 폴더 ID (환경 변수 또는 기본값)
        folder_id = os.getenv("REFERENCE_FOLDER_ID", "1xr_UXlpNHtOpgHLBbG5Uxpkf5arBghgP")

        # 임시 디렉토리 생성
        temp_dir = backend_dir / "temp_reference"
        temp_dir.mkdir(exist_ok=True)

        # Google Drive 폴더 다운로드
        folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
        print(f"📂 다운로드 URL: {folder_url}")

        # gdown으로 폴더 다운로드
        gdown.download_folder(
            url=folder_url,
            output=str(temp_dir),
            quiet=False,
            use_cookies=False
        )

        # 다운로드된 파일을 Reference 디렉토리로 이동
        downloaded_items = list(temp_dir.iterdir())
        if downloaded_items:
            # Reference 디렉토리 생성
            reference_dir.mkdir(exist_ok=True)

            # 모든 파일/폴더 이동
            for item in downloaded_items:
                dest = reference_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest)

            print(f"✅ Reference 데이터 다운로드 완료: {reference_dir}")

            # 임시 디렉토리 삭제
            shutil.rmtree(temp_dir, ignore_errors=True)
            return True
        else:
            print("⚠️ 다운로드된 파일이 없습니다.")
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
