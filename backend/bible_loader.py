"""
개역개정 성경 데이터 로더
Reference.zip의 성경 데이터를 로드하고 파싱
"""
import os
import re
from typing import Optional, Dict
from .bible_parser import parse_bible_reference

# 성경 책 번호 매핑 (약어 -> 디렉토리명)
BOOK_DIR_MAP = {
    # 구약
    "창": "01_창세기", "출": "02_출애굽기", "레": "03_레위기", "민": "04_민수기", "신": "05_신명기",
    "수": "06_여호수아", "삿": "07_사사기", "룻": "08_룻기",
    "삼상": "09_사무엘상", "삼하": "10_사무엘하", "왕상": "11_열왕기상", "왕하": "12_열왕기하",
    "대상": "13_역대기상", "대하": "14_역대기하", "스": "15_에스라", "느": "16_느헤미야", "에": "17_에스더",
    "욥": "18_욥기", "시": "19_시편", "잠": "20_잠언", "전": "21_전도서", "아": "22_아가",
    "사": "23_이사야", "렘": "24_예레미야", "애": "25_예레미야애가", "겔": "26_에스겔", "단": "27_다니엘",
    "호": "28_호세아", "욜": "29_요엘", "암": "30_아모스", "옵": "31_오바댜", "욘": "32_요나",
    "미": "33_미가", "나": "34_나훔", "합": "35_하박국", "습": "36_스바냐", "학": "37_학개",
    "슥": "38_스가랴", "말": "39_말라기",

    # 신약
    "마": "40_마태복음", "막": "41_마가복음", "눅": "42_누가복음", "요": "43_요한복음",
    "행": "44_사도행전", "롬": "45_로마서",
    "고전": "46_고린도전서", "고후": "47_고린도후서",
    "갈": "48_갈라디아서", "엡": "49_에베소서", "빌": "50_빌립보서", "골": "51_골로새서",
    "살전": "52_데살로니가전서", "살후": "53_데살로니가후서",
    "딤전": "54_디모데전서", "딤후": "55_디모데후서", "딛": "56_디도서", "몬": "57_빌레몬서",
    "히": "58_히브리서", "약": "59_야고보서",
    "벧전": "60_베드로전서", "벧후": "61_베드로후서",
    "요일": "62_요한1서", "요이": "63_요한2서", "요삼": "64_요한3서",
    "유": "65_유다서", "계": "66_요한계시록"
}

# 책 약어 (파일명용)
BOOK_ABBREV_FILE_MAP = {
    "창": "창", "출": "출", "레": "레", "민": "민", "신": "신",
    "수": "수", "삿": "삿", "룻": "룻",
    "삼상": "삼상", "삼하": "삼하", "왕상": "왕상", "왕하": "왕하",
    "대상": "대상", "대하": "대하", "스": "스", "느": "느", "에": "에",
    "욥": "욥", "시": "시", "잠": "잠", "전": "전", "아": "아",
    "사": "사", "렘": "렘", "애": "애", "겔": "겔", "단": "단",
    "호": "호", "욜": "욜", "암": "암", "옵": "옵", "욘": "욘",
    "미": "미", "나": "나", "합": "합", "습": "습", "학": "학",
    "슥": "슥", "말": "말",
    "마": "마", "막": "막", "눅": "눅", "요": "요",
    "행": "행", "롬": "롬",
    "고전": "고전", "고후": "고후",
    "갈": "갈", "엡": "엡", "빌": "빌", "골": "골",
    "살전": "살전", "살후": "살후",
    "딤전": "딤전", "딤후": "딤후", "딛": "딛", "몬": "몬",
    "히": "히", "약": "약",
    "벧전": "벧전", "벧후": "벧후",
    "요일": "요일", "요이": "요이", "요삼": "요삼",
    "유": "유", "계": "계"
}


class BibleLoader:
    """개역개정 성경 로더"""

    def __init__(self, bible_data_path: str = None):
        """
        Args:
            bible_data_path: Reference/개역개정📖 폴더 경로
        """
        if bible_data_path is None:
            # 기본 경로 설정 (backend/Reference/)
            current_dir = os.path.dirname(__file__)
            bible_data_path = os.path.join(current_dir, "Reference")

            # 개역개정📖 폴더 찾기
            if os.path.exists(bible_data_path):
                for item in os.listdir(bible_data_path):
                    if '개역개정' in item and '📖' in item:
                        bible_data_path = os.path.join(bible_data_path, item)
                        break

        self.bible_path = bible_data_path

    def load_scripture(self, reference: str) -> Optional[str]:
        """
        성경 구절 로드

        Args:
            reference: 성경 참조 (예: "출24:12-18", "고전2:1-5")

        Returns:
            성경 본문 텍스트, 실패시 None
        """
        try:
            print(f"      [BibleLoader] 레퍼런스 파싱: {reference}")

            # 레퍼런스 파싱
            parsed = parse_bible_reference(reference, "korean")
            book_abbrev = parsed.get("book_abbrev")
            chapter = parsed.get("chapter")
            verses = parsed.get("verses")

            print(f"      [BibleLoader] 파싱 결과: book={book_abbrev}, chapter={chapter}, verses={verses}")

            if not book_abbrev or not chapter:
                print(f"      [BibleLoader] ❌ 파싱 실패: book_abbrev 또는 chapter가 없음")
                return None

            # 구절 범위 파싱
            verse_start, verse_end = self._parse_verse_range(verses)
            print(f"      [BibleLoader] 구절 범위: {verse_start}-{verse_end}")

            # 파일 경로 생성
            book_dir = BOOK_DIR_MAP.get(book_abbrev)
            if not book_dir:
                print(f"      [BibleLoader] ❌ book_dir을 찾을 수 없음: {book_abbrev}")
                return None

            file_abbrev = BOOK_ABBREV_FILE_MAP.get(book_abbrev, book_abbrev)
            file_name = f"{file_abbrev} {chapter}.md"
            file_path = os.path.join(self.bible_path, book_dir, file_name)

            print(f"      [BibleLoader] 파일 경로: {file_path}")
            print(f"      [BibleLoader] Bible path: {self.bible_path}")
            print(f"      [BibleLoader] Bible path exists: {os.path.exists(self.bible_path) if self.bible_path else False}")

            # Bible path 내용 확인
            if self.bible_path and os.path.exists(self.bible_path):
                contents = os.listdir(self.bible_path)[:10]
                print(f"      [BibleLoader] Bible path 내용 (처음 10개): {contents}")

            # 파일 읽기
            if not os.path.exists(file_path):
                print(f"      [BibleLoader] ❌ 파일이 존재하지 않음: {file_path}")

                # 상위 디렉토리 확인
                parent_dir = os.path.dirname(file_path)
                if os.path.exists(parent_dir):
                    print(f"      [BibleLoader] 상위 디렉토리 내용: {os.listdir(parent_dir)[:10]}")
                else:
                    print(f"      [BibleLoader] 상위 디렉토리도 존재하지 않음: {parent_dir}")

                return None

            print(f"      [BibleLoader] ✅ 파일 발견, 읽는 중...")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 구절 추출
            verses_text = self._extract_verses(content, verse_start, verse_end)
            print(f"      [BibleLoader] ✅ 구절 추출 완료 ({len(verses_text) if verses_text else 0} 글자)")
            return verses_text

        except Exception as e:
            print(f"      [BibleLoader] ❌ 오류: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _parse_verse_range(self, verses_str: Optional[str]) -> tuple:
        """
        구절 범위 파싱

        Args:
            verses_str: "1", "1-5", "12-18" 등

        Returns:
            (start_verse, end_verse)
        """
        if not verses_str:
            return (1, 999)  # 전체 장

        if '-' in verses_str:
            parts = verses_str.split('-')
            return (int(parts[0]), int(parts[1]))
        else:
            verse_num = int(verses_str)
            return (verse_num, verse_num)

    def _extract_verses(self, content: str, start: int, end: int) -> str:
        """
        마크다운 content에서 특정 구절 범위 추출

        Format:
        ###### 1
        <소제목> 본문...
        ###### 2
        본문...
        """
        lines = content.split('\n')
        result = []
        current_verse = 0
        capturing = False

        for line in lines:
            # 구절 번호 체크
            verse_match = re.match(r'^######\s+(\d+)', line)
            if verse_match:
                current_verse = int(verse_match.group(1))

                if start <= current_verse <= end:
                    capturing = True
                    # 구절 번호는 포함하되 마크다운 제거
                    result.append(f"{current_verse} ")
                elif current_verse > end:
                    break
                else:
                    capturing = False
            elif capturing:
                # 네비게이션 링크 제거
                if line.strip().startswith('[[') or line.strip().startswith('[[@'):
                    continue

                # 빈 줄 스킵
                if not line.strip():
                    continue

                # 소제목 처리: <제목> 형식 제거하거나 유지
                cleaned_line = re.sub(r'<([^>]+)>', '', line)

                # 본문 추가 (줄바꿈 없이 이어붙이기)
                result.append(cleaned_line.strip() + ' ')

        # 결과 정리
        text = ''.join(result).strip()
        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        return text


# 전역 인스턴스
_bible_loader = None

def get_bible_loader() -> BibleLoader:
    """성경 로더 싱글톤"""
    global _bible_loader
    if _bible_loader is None:
        _bible_loader = BibleLoader()
    return _bible_loader
