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

                # 내부 구조로 검색 (찬_001.md 같은 파일이 있는지)
                if not found:
                    for item in os.listdir(base_path):
                        item_path = os.path.join(base_path, item)
                        if not os.path.isdir(item_path):
                            continue

                        try:
                            files = os.listdir(item_path)
                            for file in files:
                                if file.startswith('찬_') or '찬송가' in file:
                                    hymn_data_path = item_path
                                    found = True
                                    print(f"[HymnLoader] 찬송가 폴더 발견 (구조): {item}")
                                    break
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

            # 찬송가 파일 찾기 (여러 형식 시도)
            possible_patterns = [
                f"찬_{hymn_number:03d}.md",  # 찬_001.md
                f"찬송가_{hymn_number}.md",   # 찬송가_1.md
                f"{hymn_number}.md",          # 1.md
                f"새찬송가_{hymn_number}.md", # 새찬송가_1.md
            ]

            hymn_file = None
            for pattern in possible_patterns:
                test_path = os.path.join(self.hymn_path, pattern)
                if os.path.exists(test_path):
                    hymn_file = test_path
                    break

            # 디렉토리 내 검색
            if not hymn_file and os.path.isdir(self.hymn_path):
                for item in os.listdir(self.hymn_path):
                    if str(hymn_number) in item and item.endswith('.md'):
                        hymn_file = os.path.join(self.hymn_path, item)
                        break

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
