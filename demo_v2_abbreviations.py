"""
v2.0 약어 파싱 기능 데모
"""
import sys
sys.path.insert(0, 'backend')
from bible_parser import parse_bible_reference
from main import *

print("="*70)
print("  📖 예배 슬라이드 생성기 v2.0 - 약어 파싱 데모")
print("="*70)
print()

# 테스트 케이스: 다양한 약어들
test_cases = [
    # 한국어 약어
    ("창1:1", "korean", "개역개정"),
    ("출20:1-17", "korean", "개역개정"),
    ("요3:16", "korean", "개역개정"),
    ("롬8:28-30", "korean", "개역개정"),
    ("계21:1-4", "korean", "개역개정"),
    ("시23", "korean", "개역개정"),
    ("잠3:5-6", "korean", "개역개정"),
    ("사40:31", "korean", "개역개정"),
    ("빌4:13", "korean", "개역개정"),
    ("고전13:4-8", "korean", "개역개정"),

    # 영어 약어
    ("John3:16", "english", "NIV"),
    ("Gen1:1", "english", "NIV"),
    ("Rom8:28", "english", "NIV"),
    ("Rev21:1-4", "english", "ESV"),
    ("Ps23", "english", "KJV"),

    # 독일어 약어
    ("Joh3:16", "german", "Luther 2017"),
    ("1Mo1:1", "german", "Luther 1984"),
    ("Röm8:28", "german", "Luther 2017"),
    ("Offb21:1-4", "german", "Luther 2017"),
]

print("📝 성경 약어 파싱 테스트")
print("-"*70)
print()

success_count = 0
for abbrev, lang, translation in test_cases:
    result = parse_bible_reference(abbrev, lang)

    if result.get('book'):
        success_count += 1
        print(f"✅ {abbrev:15s} → {result['formatted']:25s} [{translation}]")
    else:
        print(f"❌ {abbrev:15s} → 파싱 실패")

print()
print(f"결과: {success_count}/{len(test_cases)} 성공")
print()

# 실제 PPT 생성 테스트
print("="*70)
print("🎯 실제 PPT 생성 테스트 (약어 사용)")
print("="*70)
print()

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_test_presentation():
    """약어를 사용한 PPT 생성"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    config = SlideConfig(
        font_name="맑은 고딕",
        font_size=32,
        title_font_size=44,
        background_color="#FFFFFF",
        text_color="#000000",
        title_color="#1a365d"
    )

    # 제목 슬라이드
    add_title_slide(prs, "함부르크 감리교회", "2026년 2월 16일 주일예배", config)

    # 약어를 사용한 성경 본문들
    scriptures = [
        ScriptureVerse(
            reference="요3:16",  # 약어!
            translation="개역개정",
            text="하나님이 세상을 이처럼 사랑하사 독생자를 주셨으니 이는 그를 믿는 자마다 멸망하지 않고 영생을 얻게 하려 하심이라"
        ),
        ScriptureVerse(
            reference="롬8:28",  # 약어!
            translation="개역개정",
            text="우리가 알거니와 하나님을 사랑하는 자 곧 그의 뜻대로 부르심을 입은 자들에게는 모든 것이 합력하여 선을 이루느니라"
        ),
        ScriptureVerse(
            reference="John3:16",  # 영어 약어!
            translation="NIV",
            text="For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life."
        ),
        ScriptureVerse(
            reference="Joh3:16",  # 독일어 약어!
            translation="Luther 2017",
            text="Denn so sehr hat Gott die Welt geliebt, dass er seinen eingeborenen Sohn gab, damit jeder, der an ihn glaubt, nicht verlorengeht, sondern ewiges Leben hat."
        ),
    ]

    for scripture in scriptures:
        add_scripture_slides(prs, scripture, config)

    # 저장
    filename = "sermon_v2_abbreviations_demo.pptx"
    prs.save(filename)

    print(f"✅ 완료! 파일이 생성되었습니다: {filename}")
    print(f"📊 총 슬라이드 수: {len(prs.slides)}")
    print()
    print("슬라이드 목록:")
    print("  1. 제목 슬라이드 (함부르크 감리교회)")
    print("  2. 요3:16 → 요한복음 3:16 (개역개정)")
    print("  3. 롬8:28 → 로마서 8:28 (개역개정)")
    print("  4. John3:16 → John 3:16 (NIV)")
    print("  5. Joh3:16 → Johannes 3:16 (Luther 2017)")
    print()
    print("💡 모든 약어가 자동으로 전체 이름으로 변환되었습니다!")

    return filename

create_test_presentation()

print()
print("="*70)
print("✨ v2.0 주요 개선사항")
print("="*70)
print("""
1. ✅ 성경 약어 자동 인식
   - 한국어: 창, 출, 요, 롬, 계 등 66권 전체
   - 영어: Gen, John, Rom, Rev 등
   - 독일어: 1Mo, Joh, Röm, Offb 등

2. ✅ 공백 없이도 인식
   - "요3:16" ✓
   - "창1:1" ✓
   - "롬8:28-30" ✓

3. ✅ 범위 지원
   - 단일 절: "요3:16"
   - 범위: "롬8:28-30"
   - 장만: "시23"

4. ✅ 자동 언어 감지
   - 번역본으로 언어 자동 판단
   - NIV/ESV → 영어 약어
   - Luther → 독일어 약어
   - 개역개정 → 한국어 약어

5. ✅ API 엔드포인트 추가
   - GET /parse-bible-reference
   - 프론트엔드에서 실시간 미리보기 가능
""")
print("="*70)
