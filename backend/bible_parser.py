"""
성경 약어 파싱 및 전체 이름 변환
"""

# 성경 약어 매핑 (한국어)
BIBLE_ABBREVIATIONS_KR = {
    # 구약
    "창": "창세기", "창세기": "창세기",
    "출": "출애굽기", "출애굽기": "출애굽기",
    "레": "레위기", "레위기": "레위기",
    "민": "민수기", "민수기": "민수기",
    "신": "신명기", "신명기": "신명기",
    "수": "여호수아", "여호수아": "여호수아",
    "삿": "사사기", "사사기": "사사기",
    "룻": "룻기", "룻기": "룻기",
    "삼상": "사무엘상", "사무엘상": "사무엘상",
    "삼하": "사무엘하", "사무엘하": "사무엘하",
    "왕상": "열왕기상", "열왕기상": "열왕기상",
    "왕하": "열왕기하", "열왕기하": "열왕기하",
    "대상": "역대상", "역대상": "역대상",
    "대하": "역대하", "역대하": "역대하",
    "스": "에스라", "에스라": "에스라",
    "느": "느헤미야", "느헤미야": "느헤미야",
    "에": "에스더", "에스더": "에스더",
    "욥": "욥기", "욥기": "욥기",
    "시": "시편", "시편": "시편",
    "잠": "잠언", "잠언": "잠언",
    "전": "전도서", "전도서": "전도서",
    "아": "아가", "아가": "아가",
    "사": "이사야", "이사야": "이사야",
    "렘": "예레미야", "예레미야": "예레미야",
    "애": "예레미야애가", "애가": "예레미야애가",
    "겔": "에스겔", "에스겔": "에스겔",
    "단": "다니엘", "다니엘": "다니엘",
    "호": "호세아", "호세아": "호세아",
    "욜": "요엘", "요엘": "요엘",
    "암": "아모스", "아모스": "아모스",
    "옵": "오바댜", "오바댜": "오바댜",
    "욘": "요나", "요나": "요나",
    "미": "미가", "미가": "미가",
    "나": "나훔", "나훔": "나훔",
    "합": "하박국", "하박국": "하박국",
    "습": "스바냐", "스바냐": "스바냐",
    "학": "학개", "학개": "학개",
    "슥": "스가랴", "스가랴": "스가랴",
    "말": "말라기", "말라기": "말라기",

    # 신약
    "마": "마태복음", "마태": "마태복음", "마태복음": "마태복음",
    "막": "마가복음", "마가": "마가복음", "마가복음": "마가복음",
    "눅": "누가복음", "누가": "누가복음", "누가복음": "누가복음",
    "요": "요한복음", "요한": "요한복음", "요한복음": "요한복음",
    "행": "사도행전", "사도행전": "사도행전",
    "롬": "로마서", "로마서": "로마서",
    "고전": "고린도전서", "고린도전서": "고린도전서",
    "고후": "고린도후서", "고린도후서": "고린도후서",
    "갈": "갈라디아서", "갈라디아서": "갈라디아서",
    "엡": "에베소서", "에베소서": "에베소서",
    "빌": "빌립보서", "빌립보서": "빌립보서",
    "골": "골로새서", "골로새서": "골로새서",
    "살전": "데살로니가전서", "데살로니가전서": "데살로니가전서",
    "살후": "데살로니가후서", "데살로니가후서": "데살로니가후서",
    "딤전": "디모데전서", "디모데전서": "디모데전서",
    "딤후": "디모데후서", "디모데후서": "디모데후서",
    "딛": "디도서", "디도서": "디도서",
    "몬": "빌레몬서", "빌레몬서": "빌레몬서",
    "히": "히브리서", "히브리서": "히브리서",
    "약": "야고보서", "야고보서": "야고보서",
    "벧전": "베드로전서", "베드로전서": "베드로전서",
    "벧후": "베드로후서", "베드로후서": "베드로후서",
    "요일": "요한일서", "요한일서": "요한일서",
    "요이": "요한이서", "요한이서": "요한이서",
    "요삼": "요한삼서", "요한삼서": "요한삼서",
    "유": "유다서", "유다서": "유다서",
    "계": "요한계시록", "계시록": "요한계시록", "요한계시록": "요한계시록",
}

# 영어 약어 매핑
BIBLE_ABBREVIATIONS_EN = {
    # Old Testament
    "gen": "Genesis", "genesis": "Genesis",
    "ex": "Exodus", "exod": "Exodus", "exodus": "Exodus",
    "lev": "Leviticus", "leviticus": "Leviticus",
    "num": "Numbers", "numbers": "Numbers",
    "deut": "Deuteronomy", "dt": "Deuteronomy", "deuteronomy": "Deuteronomy",
    "josh": "Joshua", "joshua": "Joshua",
    "judg": "Judges", "judges": "Judges",
    "ruth": "Ruth",
    "1sam": "1 Samuel", "1 samuel": "1 Samuel",
    "2sam": "2 Samuel", "2 samuel": "2 Samuel",
    "1kgs": "1 Kings", "1 kings": "1 Kings",
    "2kgs": "2 Kings", "2 kings": "2 Kings",
    "1chr": "1 Chronicles", "1 chronicles": "1 Chronicles",
    "2chr": "2 Chronicles", "2 chronicles": "2 Chronicles",
    "ezra": "Ezra",
    "neh": "Nehemiah", "nehemiah": "Nehemiah",
    "esth": "Esther", "esther": "Esther",
    "job": "Job",
    "ps": "Psalms", "psa": "Psalms", "psalms": "Psalms",
    "prov": "Proverbs", "proverbs": "Proverbs",
    "eccl": "Ecclesiastes", "ecclesiastes": "Ecclesiastes",
    "song": "Song of Solomon", "sos": "Song of Solomon",
    "isa": "Isaiah", "isaiah": "Isaiah",
    "jer": "Jeremiah", "jeremiah": "Jeremiah",
    "lam": "Lamentations", "lamentations": "Lamentations",
    "ezek": "Ezekiel", "ezekiel": "Ezekiel",
    "dan": "Daniel", "daniel": "Daniel",
    "hos": "Hosea", "hosea": "Hosea",
    "joel": "Joel",
    "amos": "Amos",
    "obad": "Obadiah", "obadiah": "Obadiah",
    "jonah": "Jonah",
    "mic": "Micah", "micah": "Micah",
    "nah": "Nahum", "nahum": "Nahum",
    "hab": "Habakkuk", "habakkuk": "Habakkuk",
    "zeph": "Zephaniah", "zephaniah": "Zephaniah",
    "hag": "Haggai", "haggai": "Haggai",
    "zech": "Zechariah", "zechariah": "Zechariah",
    "mal": "Malachi", "malachi": "Malachi",

    # New Testament
    "matt": "Matthew", "mt": "Matthew", "matthew": "Matthew",
    "mark": "Mark", "mk": "Mark",
    "luke": "Luke", "lk": "Luke",
    "john": "John", "jn": "John", "joh": "John",
    "acts": "Acts",
    "rom": "Romans", "romans": "Romans",
    "1cor": "1 Corinthians", "1 corinthians": "1 Corinthians",
    "2cor": "2 Corinthians", "2 corinthians": "2 Corinthians",
    "gal": "Galatians", "galatians": "Galatians",
    "eph": "Ephesians", "ephesians": "Ephesians",
    "phil": "Philippians", "philippians": "Philippians",
    "col": "Colossians", "colossians": "Colossians",
    "1thess": "1 Thessalonians", "1 thessalonians": "1 Thessalonians",
    "2thess": "2 Thessalonians", "2 thessalonians": "2 Thessalonians",
    "1tim": "1 Timothy", "1 timothy": "1 Timothy",
    "2tim": "2 Timothy", "2 timothy": "2 Timothy",
    "titus": "Titus", "tit": "Titus",
    "philem": "Philemon", "phlm": "Philemon", "philemon": "Philemon",
    "heb": "Hebrews", "hebrews": "Hebrews",
    "jas": "James", "james": "James",
    "1pet": "1 Peter", "1 peter": "1 Peter",
    "2pet": "2 Peter", "2 peter": "2 Peter",
    "1john": "1 John", "1 john": "1 John",
    "2john": "2 John", "2 john": "2 John",
    "3john": "3 John", "3 john": "3 John",
    "jude": "Jude",
    "rev": "Revelation", "revelation": "Revelation",
}

# 독일어 약어 매핑
BIBLE_ABBREVIATIONS_DE = {
    # Altes Testament
    "1mo": "1. Mose", "gen": "1. Mose", "genesis": "1. Mose",
    "2mo": "Exodus", "ex": "Exodus", "exodus": "Exodus",
    "3mo": "Levitikus", "lev": "Levitikus",
    "4mo": "Numeri", "num": "Numeri",
    "5mo": "Deuteronomium", "dtn": "Deuteronomium",
    "jos": "Josua", "josua": "Josua",
    "ri": "Richter", "richter": "Richter",
    "rut": "Rut", "ruth": "Rut",
    "1sam": "1. Samuel",
    "2sam": "2. Samuel",
    "1kön": "1. Könige", "1kön": "1. Könige",
    "2kön": "2. Könige", "2kön": "2. Könige",
    "1chr": "1. Chronik",
    "2chr": "2. Chronik",
    "esra": "Esra",
    "neh": "Nehemia", "nehemia": "Nehemia",
    "est": "Ester", "esther": "Ester",
    "hiob": "Hiob", "ijob": "Hiob",
    "ps": "Psalm", "psalm": "Psalm", "psalmen": "Psalm",
    "spr": "Sprüche", "sprüche": "Sprüche",
    "pred": "Prediger", "koh": "Kohelet",
    "hld": "Hohelied",
    "jes": "Jesaja", "jesaja": "Jesaja",
    "jer": "Jeremia", "jeremia": "Jeremia",
    "klgl": "Klagelieder",
    "hes": "Hesekiel", "ez": "Ezechiel",
    "dan": "Daniel", "daniel": "Daniel",
    "hos": "Hosea", "hosea": "Hosea",
    "joel": "Joel",
    "am": "Amos", "amos": "Amos",
    "obd": "Obadja",
    "jona": "Jona",
    "mi": "Micha", "micha": "Micha",
    "nah": "Nahum", "nahum": "Nahum",
    "hab": "Habakuk", "habakuk": "Habakuk",
    "zef": "Zefanja", "zefanja": "Zefanja",
    "hag": "Haggai", "haggai": "Haggai",
    "sach": "Sacharja", "sacharja": "Sacharja",
    "mal": "Maleachi", "maleachi": "Maleachi",

    # Neues Testament
    "mt": "Matthäus", "matt": "Matthäus", "matthäus": "Matthäus",
    "mk": "Markus", "markus": "Markus",
    "lk": "Lukas", "lukas": "Lukas",
    "joh": "Johannes", "johannes": "Johannes",
    "apg": "Apostelgeschichte",
    "röm": "Römer", "römer": "Römer",
    "1kor": "1. Korinther",
    "2kor": "2. Korinther",
    "gal": "Galater", "galater": "Galater",
    "eph": "Epheser", "epheser": "Epheser",
    "phil": "Philipper", "philipper": "Philipper",
    "kol": "Kolosser", "kolosser": "Kolosser",
    "1thess": "1. Thessalonicher",
    "2thess": "2. Thessalonicher",
    "1tim": "1. Timotheus",
    "2tim": "2. Timotheus",
    "tit": "Titus", "titus": "Titus",
    "phlm": "Philemon", "philemon": "Philemon",
    "hebr": "Hebräer", "hebräer": "Hebräer",
    "jak": "Jakobus", "jakobus": "Jakobus",
    "1petr": "1. Petrus",
    "2petr": "2. Petrus",
    "1joh": "1. Johannes",
    "2joh": "2. Johannes",
    "3joh": "3. Johannes",
    "jud": "Judas", "judas": "Judas",
    "offb": "Offenbarung", "offenbarung": "Offenbarung",
}

import re

def parse_bible_reference(reference: str, language: str = "korean") -> dict:
    """
    성경 참조를 파싱하여 책, 장, 절 정보를 반환

    예시:
        "요 3:16" -> {"book": "요한복음", "chapter": 3, "verses": "16"}
        "창1:1-5" -> {"book": "창세기", "chapter": 1, "verses": "1-5"}
        "롬8" -> {"book": "로마서", "chapter": 8, "verses": None}
    """
    # 언어별 약어 선택
    if language.lower() in ["korean", "ko", "한국어"]:
        abbreviations = BIBLE_ABBREVIATIONS_KR
    elif language.lower() in ["english", "en", "영어"]:
        abbreviations = BIBLE_ABBREVIATIONS_EN
    elif language.lower() in ["german", "de", "deutsch", "독일어"]:
        abbreviations = BIBLE_ABBREVIATIONS_DE
    else:
        abbreviations = BIBLE_ABBREVIATIONS_KR

    # 공백 제거 및 소문자 변환
    reference = reference.strip()

    # 패턴 매칭: 책이름 장:절
    # 예: "요 3:16", "창세기 1:1-5", "롬8:28-30", "창1:1"
    # 책이름 뒤에 공백 없이 숫자가 올 수 있음 (창1:1)
    pattern = r'^([가-힣a-zA-Z]+)\s*(\d+)(?::(\d+(?:-\d+)?))?$'
    match = re.match(pattern, reference)

    if not match:
        return {
            "original": reference,
            "book": None,
            "chapter": None,
            "verses": None,
            "error": "Invalid format"
        }

    book_abbrev = match.group(1)
    chapter = int(match.group(2)) if match.group(2) else None
    verses = match.group(3) if match.group(3) else None

    # 약어를 전체 이름으로 변환
    book_full = abbreviations.get(book_abbrev, book_abbrev)

    return {
        "original": reference,
        "book": book_full,
        "book_abbrev": book_abbrev,
        "chapter": chapter,
        "verses": verses,
        "formatted": format_reference(book_full, chapter, verses)
    }

def format_reference(book: str, chapter: int = None, verses: str = None) -> str:
    """성경 참조를 포맷팅"""
    result = book
    if chapter:
        result += f" {chapter}"
        if verses:
            result += f":{verses}"
    return result

# 테스트
if __name__ == "__main__":
    test_cases = [
        ("요 3:16", "korean"),
        ("창1:1-5", "korean"),
        ("롬8:28-30", "korean"),
        ("시편 23", "korean"),
        ("계 21:1-4", "korean"),
        ("John 3:16", "english"),
        ("Gen 1:1", "english"),
        ("Joh 3:16", "german"),
    ]

    print("="*60)
    print("성경 참조 파싱 테스트")
    print("="*60)

    for ref, lang in test_cases:
        result = parse_bible_reference(ref, lang)
        print(f"\n입력: {ref} ({lang})")
        print(f"  책: {result['book']}")
        print(f"  장: {result['chapter']}")
        print(f"  절: {result['verses']}")
        print(f"  포맷: {result['formatted']}")
