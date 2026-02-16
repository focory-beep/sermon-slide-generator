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
        print(f"   경로: {reference_dir}")

        # 폴더 내용 확인 (디버깅)
        items = list(reference_dir.iterdir())[:5]
        print(f"   내용 (처음 5개): {[item.name for item in items]}")
        return True

    print("📥 Reference.zip 다운로드 시작...")
    print(f"   대상 경로: {backend_dir}")

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
            print("❌ ZIP 파일 다운로드 실패")
            return False

        print(f"✅ ZIP 파일 다운로드 완료: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")
        print("📦 압축 해제 중...")

        # 임시 디렉토리에 압축 해제
        temp_extract_dir = backend_dir / "temp_extract"
        temp_extract_dir.mkdir(exist_ok=True)

        # ZIP 파일 압축 해제
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_dir)

        print("✅ 압축 해제 완료")

        # ZIP 파일 삭제
        zip_path.unlink()

        # 압축 해제된 파일 구조 확인
        extracted_items = list(temp_extract_dir.iterdir())
        print(f"📁 압축 해제된 항목: {[item.name for item in extracted_items]}")

        # 케이스 1: Reference 폴더가 있는 경우 (Reference/개역개정📖/)
        reference_found = False
        for item in extracted_items:
            if item.name == "Reference" and item.is_dir():
                print(f"✅ Reference 폴더 발견: {item}")
                shutil.move(str(item), str(reference_dir))
                reference_found = True
                break

        # 케이스 2: Reference 폴더 없이 바로 데이터 폴더들이 있는 경우
        if not reference_found:
            print("📁 Reference 폴더가 없습니다. 직접 생성합니다.")
            reference_dir.mkdir(exist_ok=True)

            # 모든 파일/폴더를 Reference로 이동
            for item in extracted_items:
                dest = reference_dir / item.name
                print(f"   이동: {item.name} → {dest}")
                shutil.move(str(item), str(dest))

        # 임시 디렉토리 삭제
        shutil.rmtree(temp_extract_dir, ignore_errors=True)

        # Reference 폴더 확인
        if reference_dir.exists():
            items_in_ref = list(reference_dir.iterdir())
            print(f"✅ Reference 폴더 최종 내용 ({len(items_in_ref)}개 항목):")

            # 처음 10개 항목 출력
            for item in items_in_ref[:10]:
                print(f"   - {item.name}")

            if len(items_in_ref) > 10:
                print(f"   ... 외 {len(items_in_ref) - 10}개")

            # 성경/찬송가 폴더 확인 (인코딩 문제 대응)
            bible_found = False
            hymn_found = False
            for item in items_in_ref:
                # 바이트로 변환해서 인코딩 문제 해결 시도
                try:
                    item_name = item.name
                    # 여러 인코딩 방식 시도
                    for encoding in ['utf-8', 'cp949', 'euc-kr', 'latin-1']:
                        try:
                            if isinstance(item_name, bytes):
                                decoded = item_name.decode(encoding)
                            else:
                                decoded = item_name.encode('latin-1').decode(encoding)

                            if '개역개정' in decoded or '성경' in decoded:
                                bible_found = True
                                print(f"   ✅ 성경 폴더 발견: {item.name} (인코딩: {encoding})")
                                break
                            if '찬송가' in decoded:
                                hymn_found = True
                                print(f"   ✅ 찬송가 폴더 발견: {item.name} (인코딩: {encoding})")
                                break
                        except:
                            continue
                except:
                    pass

                # 기본 검색
                if '개역개정' in item.name or '성경' in item.name:
                    bible_found = True
                    print(f"   ✅ 성경 폴더 발견: {item.name}")
                if '찬송가' in item.name:
                    hymn_found = True
                    print(f"   ✅ 찬송가 폴더 발견: {item.name}")

            if not bible_found:
                print("   ⚠️ 성경 폴더를 찾을 수 없습니다!")
                print("   📁 Reference 폴더 내용을 다시 확인합니다...")
                # 폴더 구조 분석
                for item in items_in_ref:
                    if item.is_dir():
                        subdir_contents = list(item.iterdir())[:5]
                        print(f"      - {item.name}/ ({len(list(item.iterdir()))}개 항목)")
                        if subdir_contents:
                            print(f"        내부: {[x.name for x in subdir_contents]}")

                        # 창세기 폴더 찾기 (숫자로 시작하는 폴더)
                        if item.name.startswith('01_') or item.name.startswith('1_') or '창세기' in item.name:
                            bible_found = True
                            print(f"   ✅ 성경 폴더 발견 (번호 기반): {item.name}")

            if not hymn_found:
                print("   ⚠️ 찬송가 폴더를 찾을 수 없습니다!")

            return True
        else:
            print("❌ Reference 폴더가 생성되지 않았습니다.")
            return False

    except Exception as e:
        print(f"❌ Reference 데이터 다운로드 실패: {e}")
        import traceback
        traceback.print_exc()
        print("⚠️ Reference 데이터 없이 서버를 시작합니다. 일부 기능이 작동하지 않을 수 있습니다.")
        # 실패해도 서버는 시작되도록 함
        return False


def initialize():
    """서버 시작 시 초기화 작업 실행"""
    print("=" * 60)
    print("🚀 서버 초기화 시작...")
    print("=" * 60)
    download_reference_data()
    print("=" * 60)
    print("✅ 서버 초기화 완료!")
    print("=" * 60)


if __name__ == "__main__":
    initialize()
