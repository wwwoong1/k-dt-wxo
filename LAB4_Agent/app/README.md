# HR Automation FastAPI Server

이 서버는 AskHR 데모용 OpenAPI 스펙을 만족하도록 만든 FastAPI 백엔드입니다.

## 포함 기능

- `GET /user_profile_details/{name}`: 사용자 프로필 조회
- `GET /time-off-balance/{name}`: 남은 휴가 일수 조회
- `POST /request-time-off`: 휴가 신청
- `PUT /update-title`: 직책 변경
- `PUT /update-address`: 주소 변경
- `POST /create-user`: 사용자 생성
- `GET /health`: 헬스체크

## 실행 방법

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

브라우저에서 아래로 확인할 수 있습니다.

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health: `http://localhost:8000/health`

## Docker 실행 예시

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

빌드 및 실행:

```bash
docker build -t hr-automation-api .
docker run -p 8000:8000 hr-automation-api
```

## 저장 방식

- 현재는 `users.json` 파일에 데이터를 저장합니다.
- 데모용으로 간단히 구성했으며, 나중에 SQLite/PostgreSQL로 쉽게 교체할 수 있습니다.

## WXO 연결 팁

WXO에서 OpenAPI 툴로 연결할 때는 배포 URL 기준으로 스펙의 `servers.url` 값을 바꾸면 됩니다.
예:

```yaml
servers:
  - url: https://your-api.example.com
    description: Production server
```
