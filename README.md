# Seoul PM10 AI Assistant

서울시의 일별 미세먼지(PM10) 데이터를 분석하고,
사용자가 자연어로 데이터에 대해 질문할 수 있는 AI 웹 서비스입니다.

Firestore에 저장된 시계열 데이터를 FastAPI에서 분석하여
평균, 최대, 최소, 최근 추세 등의 요약 정보를 생성하고,
해당 정보를 GPT의 시스템 프롬프트에 주입하여
실제 데이터 기반의 맞춤형 답변을 제공합니다.


## 주요 기능

### 1. 데이터 기반 AI 채팅
- 서울 PM10 데이터 요약 정보를 기반으로 AI 답변 생성
- 이전 대화 내용을 활용한 멀티턴 대화
- AI 응답 대기 중 로딩 표시

### 2. 데이터 관리
- 미세먼지 데이터 추가
- 데이터 목록 조회
- 데이터 수정
- 데이터 삭제

### 3. 데이터 분석
- 데이터 기간
- 데이터 개수
- 평균 PM10
- 최대 / 최소 PM10
- 최근 7일 평균
- 직전 7일 평균
- 최근 변화율
- 증가 / 감소 / 유지 추세 분석

### 4. 대화 기록
- 대화 자동 저장
- 이전 대화 목록 조회
- 특정 대화 불러오기
- 대화 이어가기
- 대화 삭제


## 사용 데이터

서울시 일별 평균 대기오염도 데이터를 사용했습니다.

2025년 서울 25개 자치구의 PM10 데이터를 날짜별로 평균하여
365개의 일별 시계열 데이터로 가공했습니다.

데이터 형식:

```json
{
  "date": "2025-01-01",
  "value": 40.76,
  "memo": "서울 25개 자치구 PM10 일평균"
}
```


## 데이터 분석 방식

Firestore에 저장된 데이터를 기반으로 다음 정보를 계산합니다.

- 전체 평균
- 최대값 및 발생 날짜
- 최소값 및 발생 날짜
- 최근 7일 평균
- 직전 7일 평균
- 변화율

최근 추세는 최근 7일과 직전 7일의 평균 변화율을 비교하여 판단합니다.

- +5% 초과: 증가
- -5% 미만: 감소
- -5% ~ +5%: 유지

※ ±5% 기준은 공식 미세먼지 등급 기준이 아니라
서비스 내부의 추세 분석을 위해 설정한 기준입니다.


## AI 컨텍스트 주입

AI가 Firestore 데이터에 직접 접근하는 것이 아니라,
FastAPI에서 데이터 요약 정보를 생성한 뒤
이를 시스템 프롬프트에 포함하여 GPT에 전달합니다.

```text
Firestore
→ FastAPI 데이터 분석
→ Summary 생성
→ System Prompt에 주입
→ GPT API 호출
→ 데이터 기반 답변
```


## 기술 스택

### Frontend
- HTML
- CSS
- JavaScript
- Fetch API
- Vercel

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic
- Render

### Database
- Firebase Firestore

### AI
- OpenAI-compatible Chat Completions API
- GPT-5 Mini
- Codyssey API Gateway


## 배포 URL

### Frontend
https://codysseym1-2-frontend-mu.vercel.app

### Backend API
https://dust-ai-assistant-api.onrender.com

### Swagger UI
https://dust-ai-assistant-api.onrender.com/docs


## 프로젝트 구조

```text
dust-ai-assistant/
├── backend/
│   ├── config/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── config.js
│   └── build.js
│
├── data/
│   └── seoul_pm10_2025.csv
│
├── preprocess.py
├── import_data.py
├── requirements.txt
└── README.md
```


## 로컬 실행 방법

### 1. 저장소 Clone

```bash
git clone <repository-url>
cd codyssey_M1-2
```

### 2. Python 가상환경 생성

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성합니다.

```env
FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://copa.codyssey.kr/v1
ALLOWED_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
```

### 5. FastAPI 실행

```bash
uvicorn backend.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### 6. Frontend 실행

`frontend/index.html`을 VS Code Live Server 등으로 실행합니다.


## 배포 환경 변수

### Render

```text
OPENAI_API_KEY
OPENAI_BASE_URL
FIREBASE_SERVICE_ACCOUNT_JSON
ALLOWED_ORIGINS
PYTHON_VERSION
```

### Vercel

```text
API_BASE_URL
```


## API

### Data

```text
POST   /api/data
GET    /api/data
PUT    /api/data/{id}
DELETE /api/data/{id}
GET    /api/data/summary
```

### Chat

```text
POST /api/chat
```

### Conversations

```text
POST   /api/conversations
GET    /api/conversations
GET    /api/conversations/{id}
DELETE /api/conversations/{id}
```


## 배포 환경 주의사항

Render 무료 인스턴스를 사용하기 때문에 일정 시간 요청이 없으면
서버가 비활성화될 수 있습니다.

따라서 첫 요청 시 서버가 다시 시작되면서 응답이 평소보다 늦어질 수 있습니다.