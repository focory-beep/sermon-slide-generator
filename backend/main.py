from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os
import tempfile
from datetime import datetime
from .bible_parser import parse_bible_reference

app = FastAPI(title="Sermon Slide Generator")

# 정적 파일 서빙 (프론트엔드)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# CORS 설정 (프론트엔드와 통신 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScriptureVerse(BaseModel):
    """성경 구절 모델"""
    reference: str  # 예: "요한복음 3:16"
    text: str
    translation: str  # 예: "개역개정", "NIV", "Luther 1984"

class WorshipOrder(BaseModel):
    """예배 순서 항목"""
    title: str
    detail: Optional[str] = None

class SlideConfig(BaseModel):
    """슬라이드 디자인 설정"""
    font_name: str = "맑은 고딕"
    font_size: int = 32
    title_font_size: int = 44
    background_color: str = "#FFFFFF"  # hex color
    text_color: str = "#000000"
    title_color: str = "#1a365d"
    max_chars_per_slide: int = 200  # 한 슬라이드당 최대 글자 수

class PresentationRequest(BaseModel):
    """PPT 생성 요청"""
    title: str = "주일 예배"
    date: str = datetime.now().strftime("%Y년 %m월 %d일")
    worship_orders: List[WorshipOrder] = []
    scriptures: List[ScriptureVerse] = []
    config: SlideConfig = SlideConfig()

def hex_to_rgb(hex_color: str) -> RGBColor:
    """Hex 색상을 RGB로 변환"""
    hex_color = hex_color.lstrip('#')
    return RGBColor(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16)
    )

def add_title_slide(prs: Presentation, title: str, subtitle: str, config: SlideConfig):
    """제목 슬라이드 추가"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 빈 레이아웃

    # 배경색 설정
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = hex_to_rgb(config.background_color)

    # 제목 텍스트박스
    left = Inches(0.5)
    top = Inches(2)
    width = Inches(9)
    height = Inches(1.5)

    title_box = slide.shapes.add_textbox(left, top, width, height)
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    title_frame.paragraphs[0].font.size = Pt(config.title_font_size + 8)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.name = config.font_name
    title_frame.paragraphs[0].font.color.rgb = hex_to_rgb(config.title_color)

    # 부제목 텍스트박스
    subtitle_box = slide.shapes.add_textbox(left, top + Inches(1.8), width, Inches(1))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = subtitle
    subtitle_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    subtitle_frame.paragraphs[0].font.size = Pt(config.font_size)
    subtitle_frame.paragraphs[0].font.name = config.font_name
    subtitle_frame.paragraphs[0].font.color.rgb = hex_to_rgb(config.text_color)

def add_worship_order_slide(prs: Presentation, orders: List[WorshipOrder], config: SlideConfig):
    """예배 순서 슬라이드 추가"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 배경색
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = hex_to_rgb(config.background_color)

    # 제목
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "예배 순서"
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    title_frame.paragraphs[0].font.size = Pt(config.title_font_size)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.name = config.font_name
    title_frame.paragraphs[0].font.color.rgb = hex_to_rgb(config.title_color)

    # 예배 순서 목록
    content_box = slide.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(7), Inches(4.5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True

    for i, order in enumerate(orders):
        p = content_frame.add_paragraph() if i > 0 else content_frame.paragraphs[0]
        p.text = f"{i+1}. {order.title}"
        if order.detail:
            p.text += f" - {order.detail}"
        p.font.size = Pt(config.font_size - 4)
        p.font.name = config.font_name
        p.font.color.rgb = hex_to_rgb(config.text_color)
        p.space_before = Pt(12)
        p.line_spacing = 1.5

def split_text_into_chunks(text: str, max_chars: int) -> List[str]:
    """긴 텍스트를 슬라이드에 맞게 분할"""
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) + 1 <= max_chars:
            current_chunk += word + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = word + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks if chunks else [text]

def add_scripture_slides(prs: Presentation, scripture: ScriptureVerse, config: SlideConfig):
    """성경 구절 슬라이드 추가 (필요시 여러 슬라이드로 분할)"""
    text_chunks = split_text_into_chunks(scripture.text, config.max_chars_per_slide)

    # 성경 참조 파싱 (약어 -> 전체 이름)
    # 번역본에서 언어 감지
    lang = "korean"
    if scripture.translation.upper() in ["NIV", "ESV", "KJV", "NKJV", "NASB"]:
        lang = "english"
    elif "Luther" in scripture.translation or "Elberfelder" in scripture.translation:
        lang = "german"

    parsed = parse_bible_reference(scripture.reference, lang)
    reference_display = parsed.get("formatted", scripture.reference)

    for i, chunk in enumerate(text_chunks):
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # 배경색
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = hex_to_rgb(config.background_color)

        # 성경 참조 (제목)
        reference_text = reference_display
        if len(text_chunks) > 1:
            reference_text += f" ({i+1}/{len(text_chunks)})"

        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
        title_frame = title_box.text_frame
        title_frame.text = reference_text
        title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        title_frame.paragraphs[0].font.size = Pt(config.title_font_size - 8)
        title_frame.paragraphs[0].font.bold = True
        title_frame.paragraphs[0].font.name = config.font_name
        title_frame.paragraphs[0].font.color.rgb = hex_to_rgb(config.title_color)

        # 본문
        content_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4))
        content_frame = content_box.text_frame
        content_frame.word_wrap = True
        content_frame.text = chunk
        content_frame.paragraphs[0].alignment = PP_ALIGN.LEFT
        content_frame.paragraphs[0].font.size = Pt(config.font_size)
        content_frame.paragraphs[0].font.name = config.font_name
        content_frame.paragraphs[0].font.color.rgb = hex_to_rgb(config.text_color)
        content_frame.paragraphs[0].line_spacing = 1.6

        # 번역본 표시
        translation_box = slide.shapes.add_textbox(Inches(8), Inches(6.5), Inches(1.5), Inches(0.5))
        translation_frame = translation_box.text_frame
        translation_frame.text = scripture.translation
        translation_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
        translation_frame.paragraphs[0].font.size = Pt(14)
        translation_frame.paragraphs[0].font.italic = True
        translation_frame.paragraphs[0].font.name = config.font_name
        translation_frame.paragraphs[0].font.color.rgb = RGBColor(128, 128, 128)

@app.post("/generate-presentation")
async def generate_presentation(request: PresentationRequest):
    """PPT 생성 API"""
    try:
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)

        # 1. 제목 슬라이드
        add_title_slide(prs, request.title, request.date, request.config)

        # 2. 예배 순서 슬라이드
        if request.worship_orders:
            add_worship_order_slide(prs, request.worship_orders, request.config)

        # 3. 성경 본문 슬라이드들
        for scripture in request.scriptures:
            add_scripture_slides(prs, scripture, request.config)

        # 임시 파일로 저장
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pptx')
        prs.save(temp_file.name)
        temp_file.close()

        return FileResponse(
            temp_file.name,
            media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            filename=f"{request.title}_{request.date}.pptx"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def root():
    """메인 페이지 - 웹 인터페이스"""
    try:
        html_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index_v2.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            # API_URL을 현재 호스트로 변경
            html_content = html_content.replace("const API_URL = 'http://localhost:8000';", "const API_URL = window.location.origin;")
            return HTMLResponse(content=html_content)
        else:
            return HTMLResponse(content="<h1>Frontend not found</h1>")
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading frontend: {str(e)}</h1>")

@app.get("/api/info")
async def api_info():
    """API 정보"""
    return {
        "message": "Sermon Slide Generator API",
        "version": "2.0.0",
        "endpoints": {
            "generate": "/generate-presentation (POST)",
            "parse_reference": "/parse-bible-reference (GET)",
            "docs": "/docs"
        },
        "features": [
            "Multi-language support (Korean, English, German)",
            "Bible abbreviation parsing (창, 출, 요, John, Joh, etc.)",
            "Auto-text splitting for long passages",
            "Customizable fonts and colors"
        ]
    }

@app.get("/parse-bible-reference")
async def parse_reference(reference: str, language: str = "korean"):
    """
    성경 참조 파싱 API
    예: /parse-bible-reference?reference=요3:16&language=korean
    """
    try:
        result = parse_bible_reference(reference, language)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
