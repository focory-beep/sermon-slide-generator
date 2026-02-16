"""
새찬송가 데이터 로더
Reference/새찬송가🎼 폴더에서 찬송가 가사 로드
"""
import os
import re
from typing import Optional, Dict, List


class HymnLoader:
    """새찬송가 로더"""

    def __init__(self, hymn_data_path: str = None):
        """
        Args:
            hymn_data_path: Reference/새찬송가🎼 폴더 경로
        """
        if hymn_data_path is None:
            # 기본 경로 설정 (backend/Reference/)
            current_dir = os.path.dirname(__file__)
            base_path = os.path.join(current_dir, "Reference")

            # 새찬송가🎼 폴더 찾기 (인코딩 문제 대응)
            if os.path.exists(base_path):
                found = False
                for item in os.listdir(base_path):
                    item_path = os.path.join(base_path, item)
                    if not os.path.isdir(item_path):
                        continue

                    # 이름으로 검색
                    if '찬송가' in item or '새찬송가' in item:
                        hymn_data_path = item_path
                        found = True
                        print(f"[HymnLoader] 찬송가 폴더 발견: {item}")
                        break

                # 내부 구조로 검색 (인코딩 깨져도 작동)
                # 600개 이상 파일이 있는 폴더 = 찬송가 폴더 (645개)
                if not found:
                    for item in os.listdir(base_path):
                        item_path = os.path.join(base_path, item)
                        if not os.path.isdir(item_path):
                            continue

                        try:
                            files = os.listdir(item_path)
                            file_count = len(files)

                            # 600개 이상 파일 = 찬송가!
                            if file_count >= 600:
                                hymn_data_path = item_path
                                found = True
                                print(f"[HymnLoader] ✅ 찬송가 폴더 발견 (파일 수): {item} ({file_count}개)")
                                break

                            # 또는 _숫자.md 형식 파일이 있는지 확인
                            for file in files[:10]:  # 처음 10개만 확인
                                # "_123.md" 형식 찾기
                                if '_' in file and file.endswith('.md'):
                                    parts = file.split('_')
                                    if len(parts) >= 2:
                                        try:
                                            int(parts[-1].replace('.md', ''))
                                            hymn_data_path = item_path
                                            found = True
                                            print(f"[HymnLoader] ✅ 찬송가 폴더 발견 (파일 형식): {item}")
                                            break
                                        except:
                                            continue
                            if found:
                                break
                        except:
                            continue

                if not found:
                    hymn_data_path = base_path
                    print(f"[HymnLoader] ⚠️ 찬송가 폴더를 찾을 수 없어 Reference를 기본 경로로 사용")

        self.hymn_path = hymn_data_path

    def load_hymn(self, hymn_number: int) -> Optional[Dict]:
        """
        찬송가 로드

        Args:
            hymn_number: 찬송가 번호 (1-645)

        Returns:
            {
                "number": 1,
                "title": "만복의 근원 하나님",
                "verses": [
                    "1절 가사...",
                    "2절 가사...",
                    ...
                ],
                "chorus": "후렴 가사..." (있는 경우)
            }
        """
        try:
            if not self.hymn_path or not os.path.exists(self.hymn_path):
                return None

            # 찬송가 파일 찾기 (번호 기반, 인코딩 무관)
            hymn_file = None

            if os.path.isdir(self.hymn_path):
                # 파일 목록 가져오기
                files = os.listdir(self.hymn_path)

                # "_123.md" 형식으로 번호 찾기
                for file in files:
                    if not file.endswith('.md'):
                        continue

                    # 파일명에서 번호 추출
                    try:
                        # "_123.md" → 123
                        if '_' in file:
                            number_part = file.split('_')[-1].replace('.md', '')
                            file_number = int(number_part)

                            if file_number == hymn_number:
                                hymn_file = os.path.join(self.hymn_path, file)
                                print(f"[HymnLoader] ✅ 찬송가 파일 발견: {file}")
                                break
                    except:
                        continue

            if not hymn_file or not os.path.exists(hymn_file):
                return None

            # 파일 읽기
            with open(hymn_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 파싱
            result = self._parse_hymn_content(content, hymn_number)
            return result

        except Exception as e:
            print(f"Error loading hymn: {e}")
            return None

    def _parse_hymn_content(self, content: str, hymn_number: int) -> Dict:
        """
        찬송가 마크다운 content 파싱

        가정하는 형식:
        # 제목
        ## 1절
        가사...
        ## 2절
        가사...
        ## 후렴
        후렴 가사...
        """
        lines = content.split('\n')

        title = ""
        verses = []
        chorus = ""
        current_verse = ""

        for line in lines:
            line = line.strip()

            # 제목 추출
            if line.startswith('# ') and not title:
                title = line[2:].strip()
                # 번호 제거 (예: "1. 만복의 근원 하나님" -> "만복의 근원 하나님")
                title = re.sub(r'^\d+\.\s*', '', title)

            # 절 구분
            elif line.startswith('## '):
                if current_verse:
                    verses.append(current_verse.strip())
                    current_verse = ""

                section_title = line[3:].strip()
                if '후렴' in section_title or 'Chorus' in section_title:
                    # 후렴은 별도 처리
                    pass
                else:
                    # 절 번호 제거하고 시작
                    current_verse = ""

            # 본문 수집
            elif line and not line.startswith('#'):
                # 네비게이션 링크 제거
                if line.startswith('[[') or line.startswith('[[@'):
                    continue

                if current_verse:
                    current_verse += '\n' + line
                else:
                    current_verse = line

        # 마지막 절 추가
        if current_verse:
            # 후렴 체크
            if '후렴' in current_verse[:20] or 'Chorus' in current_verse[:20]:
                chorus = current_verse.strip()
            else:
                verses.append(current_verse.strip())

        return {
            "number": hymn_number,
            "title": title or f"찬송가 {hymn_number}장",
            "verses": verses,
            "chorus": chorus
        }


# 전역 인스턴스
_hymn_loader = None

def get_hymn_loader() -> HymnLoader:
    """찬송가 로더 싱글톤"""
    global _hymn_loader
    if _hymn_loader is None:
        _hymn_loader = HymnLoader()
    return _hymn_loader
