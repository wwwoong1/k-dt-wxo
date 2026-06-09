# GFM Bank Unified Tool APIs - FastAPI Server

이 프로젝트는 업로드한 OpenAPI 스펙에 맞춰 만든 FastAPI 기반 샘플 서버입니다.

## 포함된 엔드포인트
- `POST /iban-transfer`
- `POST /balance-inquiry`
- `POST /fee-reversal`
- `POST /approve-overdraft`
- `GET /health`

## 특징
- FastAPI 기반
- SQLite 로컬 DB 사용
- 서버 시작 시 샘플 계좌/거래 데이터 자동 생성
- `balance-inquiry`, `iban-transfer`는 요청 바디의 `username/password`로 간단 인증
- Swagger UI 자동 제공: `/docs`
- OpenAPI 스키마 자동 제공: `/openapi.json`

## 실행 방법
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 환경변수
```bash
export TELLER_USERNAME=teller
export TELLER_PASSWORD=teller123
export BANK_DB_PATH=./bank.db
```

## 테스트 예시
### 1. 잔액 조회
```bash
curl -X POST http://127.0.0.1:8000/balance-inquiry \
  -H "Content-Type: application/json" \
  -d '{
    "iban": "DE89320895326389021994",
    "username": "teller",
    "password": "teller123"
  }'
```

### 2. 송금
```bash
curl -X POST http://127.0.0.1:8000/iban-transfer \
  -H "Content-Type: application/json" \
  -d '{
    "source_iban": "DE89320895326389021994",
    "destination_iban": "DE89929842579913662103",
    "amount_eur": 20,
    "username": "teller",
    "password": "teller123"
  }'
```

### 3. 수수료 환불
```bash
curl -X POST http://127.0.0.1:8000/fee-reversal \
  -H "Content-Type: application/json" \
  -d '{
    "iban": "DE89320895326389021994",
    "amount_eur": 50
  }'
```

### 4. 당좌대월 승인
```bash
curl -X POST http://127.0.0.1:8000/approve-overdraft \
  -H "Content-Type: application/json" \
  -d '{
    "iban": "DE89320895326389021994",
    "overdraft_limit_eur": 4000
  }'
```

## WXO Tool 연결 팁
OpenAPI 파일의 `servers.url` 값을 실제 배포한 FastAPI 서버 주소로 바꾸면 됩니다.
예:
```yaml
servers:
  - url: https://your-domain.example.com
    description: FastAPI Endpoint
```

## 샘플 계좌
- `DE89320895326389021994`
- `DE89929842579913662103`
- `DE44500105175407324931`
