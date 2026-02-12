"""
API 테스트 스크립트
간단한 예제 데이터로 PPT 생성을 테스트합니다.
"""
import requests
import json

# API URL
API_URL = "http://localhost:8000"

# 테스트 데이터
test_data = {
    "title": "주일 예배",
    "date": "2026년 2월 16일",
    "worship_orders": [
        {"title": "예배로의 부름", "detail": None},
        {"title": "찬송", "detail": "542장 구주 예수 의지함이"},
        {"title": "기도", "detail": "담임목사"},
        {"title": "성경봉독", "detail": "요한복음 3:16-21"},
        {"title": "설교", "detail": "하나님이 세상을 이처럼 사랑하사"},
        {"title": "헌금", "detail": "봉헌기도"},
        {"title": "축도", "detail": None}
    ],
    "scriptures": [
        {
            "reference": "요한복음 3:16-17",
            "translation": "개역개정",
            "text": "하나님이 세상을 이처럼 사랑하사 독생자를 주셨으니 이는 그를 믿는 자마다 멸망하지 않고 영생을 얻게 하려 하심이라 하나님이 그 아들을 세상에 보내신 것은 세상을 심판하려 하심이 아니요 그로 말미암아 세상이 구원을 받게 하려 하심이라"
        },
        {
            "reference": "John 3:16-17",
            "translation": "NIV",
            "text": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life. For God did not send his Son into the world to condemn the world, but to save the world through him."
        },
        {
            "reference": "Johannes 3:16-17",
            "translation": "Luther 2017",
            "text": "Denn so sehr hat Gott die Welt geliebt, dass er seinen eingeborenen Sohn gab, damit jeder, der an ihn glaubt, nicht verlorengeht, sondern ewiges Leben hat. Denn Gott hat seinen Sohn nicht in die Welt gesandt, damit er die Welt richte, sondern damit die Welt durch ihn gerettet werde."
        }
    ],
    "config": {
        "font_name": "맑은 고딕",
        "font_size": 32,
        "title_font_size": 44,
        "background_color": "#FFFFFF",
        "text_color": "#000000",
        "title_color": "#1a365d",
        "max_chars_per_slide": 200
    }
}

def test_generate_presentation():
    """PPT 생성 API 테스트"""
    print("🧪 PPT 생성 API 테스트 시작...")
    print(f"📡 API URL: {API_URL}/generate-presentation")

    try:
        # API 호출
        response = requests.post(
            f"{API_URL}/generate-presentation",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            # 파일 저장
            filename = f"test_presentation_{test_data['date']}.pptx"
            with open(filename, 'wb') as f:
                f.write(response.content)

            print(f"✅ 성공! PPT 파일이 생성되었습니다: {filename}")
            print(f"📊 파일 크기: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ 오류 발생! 상태 코드: {response.status_code}")
            print(f"오류 메시지: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ 연결 오류: 서버가 실행 중인지 확인해주세요.")
        print("서버 시작: python backend/main.py")
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {str(e)}")
        return False

def test_api_health():
    """API 상태 확인"""
    print("🏥 API 헬스 체크...")
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            print("✅ API 서버 정상 작동 중")
            print(f"응답: {response.json()}")
            return True
        else:
            print(f"⚠️ 비정상 응답: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API 서버에 연결할 수 없습니다.")
        return False

if __name__ == "__main__":
    print("="*60)
    print("  📖 Sermon Slide Generator - API 테스트")
    print("="*60)
    print()

    # 1. 헬스 체크
    if test_api_health():
        print()
        # 2. PPT 생성 테스트
        test_generate_presentation()
    else:
        print("\n서버를 먼저 실행해주세요:")
        print("  python backend/main.py")

    print()
    print("="*60)
