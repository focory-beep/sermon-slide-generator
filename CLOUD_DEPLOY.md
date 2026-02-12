# 🚀 클라우드 무료 배포 가이드

**Python 설치 없이 웹에서 바로 사용하기!**

이 가이드를 따라하시면 5-10분 안에 본인만의 URL로 접속 가능합니다.

예: `https://hamburg-church-slides.onrender.com`

---

## 📋 준비물

1. **GitHub 계정** (없으면 무료 생성: [github.com](https://github.com))
2. **Render 계정** (없으면 무료 생성: [render.com](https://render.com))
3. 이 프로젝트 폴더

---

## 🎯 3단계 배포

### 1️⃣ GitHub에 프로젝트 업로드

#### Option A: GitHub 웹사이트 사용 (추천 - 가장 쉬움)

1. **GitHub 로그인**
   - [github.com](https://github.com)에서 로그인

2. **새 저장소 만들기**
   - 우측 상단 `+` 버튼 → `New repository` 클릭
   - Repository name: `sermon-slide-generator` (또는 원하는 이름)
   - Public 선택
   - `Create repository` 클릭

3. **파일 업로드**
   - `uploading an existing file` 링크 클릭
   - `sermon-slide-generator` 폴더의 **모든 파일과 폴더**를 드래그 앤 드롭
   - 아래쪽 `Commit changes` 클릭

#### Option B: Git 명령어 사용 (터미널 사용)

```bash
# 프로젝트 폴더로 이동
cd sermon-slide-generator

# Git 초기화
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Sermon Slide Generator v2.0"

# GitHub 저장소와 연결 (YOUR_USERNAME을 본인 GitHub 아이디로 변경)
git remote add origin https://github.com/YOUR_USERNAME/sermon-slide-generator.git

# GitHub에 업로드
git branch -M main
git push -u origin main
```

---

### 2️⃣ Render에 배포

1. **Render 로그인**
   - [render.com](https://render.com)에서 로그인
   - GitHub 계정으로 로그인 가능

2. **새 서비스 만들기**
   - Dashboard에서 `New +` 버튼 클릭
   - `Web Service` 선택

3. **GitHub 저장소 연결**
   - `Connect a repository` 에서 본인의 GitHub 계정 연결
   - `sermon-slide-generator` 저장소 선택
   - `Connect` 클릭

4. **배포 설정**
   - **Name**: `hamburg-church-slides` (또는 원하는 이름, URL에 사용됨)
   - **Region**: `Frankfurt (EU Central)` ← 독일에서 가장 가까움!
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: 자동 입력됨 (또는 수동 입력)
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**: 자동 입력됨 (또는 수동 입력)
     ```
     uvicorn backend.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: `Free` 선택 ← 완전 무료!

5. **배포 시작**
   - `Create Web Service` 클릭
   - 배포가 시작됩니다! (3-5분 소요)

6. **배포 완료 확인**
   - 로그에서 `Build successful` 확인
   - 상단에 URL 표시: `https://hamburg-church-slides.onrender.com`

---

### 3️⃣ 접속 및 테스트

1. **URL 열기**
   - Render 대시보드 상단의 URL 클릭
   - 또는 직접 주소 입력

2. **첫 접속**
   - ⏳ 첫 접속 시 30초 정도 기다려야 함 (무료 티어 한계)
   - "서버가 깨어나는 중..." 메시지 표시
   - 이후부터는 빠름!

3. **테스트**
   - 성경 참조: `요3:16` 입력
   - 번역본: `개역개정` 선택
   - 본문 입력 후 **PPT 생성하기** 클릭
   - ✅ PPT 다운로드 확인!

---

## 🎉 완료!

이제 **어디서든** 이 URL로 접속해서 사용할 수 있습니다!

```
https://YOUR-APP-NAME.onrender.com
```

- 집에서 ✓
- 교회에서 ✓
- 카페에서 ✓
- 핸드폰에서도 ✓

---

## 💡 사용 팁

### 1. 북마크 추가
브라우저 북마크에 URL 저장:
```
이름: 예배 슬라이드 생성기
URL: https://hamburg-church-slides.onrender.com
```

### 2. 팀원과 공유
URL을 찬양팀, 봉사자들과 공유:
```
안녕하세요!
예배 PPT 자동 생성 도구입니다:
https://hamburg-church-slides.onrender.com

약어 사용 가능합니다:
- 요3:16 → 요한복음 3:16
- 창1:1 → 창세기 1:1
```

### 3. 홈 화면에 추가 (모바일)
- iPhone: Safari에서 공유 → 홈 화면에 추가
- Android: Chrome에서 메뉴 → 홈 화면에 추가

---

## 🔧 문제 해결

### 배포가 실패해요
**증상**: Build failed
**해결**:
1. GitHub 저장소에 모든 파일이 업로드되었는지 확인
2. 특히 `requirements.txt`, `render.yaml`, `backend/`, `frontend/` 폴더 확인
3. Render 로그 확인해서 어떤 에러인지 확인

### 첫 접속이 너무 느려요
**원인**: 무료 티어는 15분 동안 접속이 없으면 서버가 sleep 모드로 전환
**해결**:
- 첫 접속 시 30초 기다리기
- 자주 사용하시면 sleep 안 됨
- 또는 유료 플랜 ($7/월) 업그레이드

### PPT 다운로드가 안 돼요
**확인 사항**:
1. 본문이 입력되었는지 확인
2. 브라우저 팝업 차단 해제
3. 브라우저 콘솔(F12)에서 에러 확인

### URL을 커스터마이징하고 싶어요
**방법 1**: Render에서 앱 이름 변경
- Dashboard → Settings → Name 변경
- 예: `hamburg-methodist-church`

**방법 2**: 도메인 연결 (선택사항)
- 본인 도메인 구입 (연 $10-15)
- Render에서 Custom Domain 설정

---

## 🔒 보안 및 프라이버시

### 데이터는 어디에 저장되나요?
- **저장 안 됨!** 모든 데이터는 PPT 생성 후 즉시 삭제
- 서버에 히스토리가 남지 않음
- 완전히 프라이빗

### 누가 접근할 수 있나요?
- URL을 아는 사람만 접근 가능
- 검색엔진에 노출 안 됨
- 원하시면 비밀번호 추가 가능 (v3.0 기능)

---

## 📈 무료 티어 제한

Render Free Plan:
- ✅ 무제한 요청
- ✅ 750시간/월 (충분함)
- ⚠️ 15분 비활동 시 sleep (첫 접속 30초 지연)
- ✅ 자동 SSL 인증서 (HTTPS)
- ✅ 무제한 사용자

**충분한 이유:**
- 주 1회 예배 준비 = 월 4-5회 사용
- 한 번 사용 시 5분 미만
- 완전히 무료로 충분!

---

## 🚀 업그레이드 옵션

더 빠른 속도가 필요하시면:
- **Starter Plan**: $7/월
  - Sleep 없음 (항상 빠름)
  - 더 많은 메모리
  - 우선 지원

---

## 🆘 도움 요청

배포 중 문제가 있으시면:
1. GitHub Issues에 질문 올리기
2. 이메일: focory@gmail.com
3. Render 로그 스크린샷 첨부하면 더 빠른 해결!

---

## 🎊 배포 완료 체크리스트

- [ ] GitHub에 코드 업로드 완료
- [ ] Render에 앱 생성 완료
- [ ] 배포 성공 확인 (Build successful)
- [ ] URL 접속 테스트 완료
- [ ] PPT 생성 테스트 완료
- [ ] 북마크 추가 완료
- [ ] 팀원들과 URL 공유 완료

---

**축하합니다! 🎉**

이제 Python 설치 없이 웹에서 바로 사용하실 수 있습니다!

매주 예배 준비가 훨씬 쉬워집니다! 🙏

---

**Made with ❤️ for Hamburg Methodist Church**

🇰🇷 한국어 • 🇬🇧 English • 🇩🇪 Deutsch
