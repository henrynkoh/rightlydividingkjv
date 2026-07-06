# YouTube 연결 설정 (1회만)

## 1. Google Cloud Console에서 credentials 받기

1. https://console.cloud.google.com 접속
2. **새 프로젝트** 생성 (이름: rightlydividing)
3. 왼쪽 메뉴 → **APIs & Services → Library**
4. "YouTube Data API v3" 검색 → **Enable**
5. **APIs & Services → Credentials**
6. **Create Credentials → OAuth 2.0 Client ID**
   - Application type: **Desktop app**
   - Name: rightlydividing
7. **Download JSON** → 파일 이름을 `client_secret.json`으로 변경
8. `client_secret.json`을 이 폴더에 저장:
   `/Users/henryoh/Documents/Claude/Projects/rightlydividing/`

## 2. 패키지 설치

```bash
pip install elevenlabs moviepy pillow google-auth google-auth-oauthlib google-api-python-client pytz
```

## 3. 파이프라인 실행

```bash
cd /Users/henryoh/Documents/Claude/Projects/rightlydividing
python pipeline.py
```

- 처음 실행 시 브라우저가 열리며 Google 계정 로그인 요청
- @ohhenry6524 채널로 로그인
- 이후 자동으로 4개 영상 생성 + 스케줄 업로드

## 업로드 스케줄

| 영상 | 제목 | 업로드 시간 (KST) |
|------|------|-------------------|
| 01 | Rightly Dividing Explained | 07:00 AM |
| 02 | Who is the Bible Written For? | 12:00 PM |
| 03 | Kingdom vs Grace Gospel | 04:00 PM |
| 04 | Why So Many Denominations? | 08:00 PM |

> 영상은 **Private**으로 업로드되며 지정 시간에 자동 공개됩니다.
