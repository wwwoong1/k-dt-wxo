# Unified Banking + HR FastAPI Server (JSON-backed)

한 개의 FastAPI 서버에서 **Banking API**와 **HR API**를 함께 운영하는 예제입니다.
이번 버전은 SQLite 대신 **JSON 파일**을 데이터 저장소로 사용하므로, 데모/실습 환경에서 디버깅이 쉽고 데이터 상태를 눈으로 바로 확인할 수 있습니다.

## 포함된 API

### Banking API
- `POST /iban-transfer`
- `POST /balance-inquiry`
- `POST /fee-reversal`
- `POST /approve-overdraft`

### HR API
- `GET /user_profile_details/{name}`
- `GET /time-off-balance/{name}`
- `POST /request-time-off`
- `PUT /update-title`
- `PUT /update-address`
- `POST /create-user`

## 데이터 파일

- `data/hr_users.json`
- `data/bank_data.json`

파일이 없으면 서버 시작 시 자동으로 생성됩니다.
기본적으로 다음 데이터가 들어 있습니다.

### HR 기본 사용자
- 장원영
- 카리나
- 안유진
- 민지
- 해린
- 지민
- 정국
- 차은우

### Banking 기본 계좌
- `DE89320895326389021994` (장원영)
- `DE89929842579913662103` (카리나)
- `DE44500105175407324931` (안유진)
- `DE12500105170648489890` (민지)
- `DE75512108001245126199` (해린)
- `DE02120300000000202051` (지민)
- `DE91100000000123456789` (정국)
- `DE66100205000009876543` (차은우)
- `DE44500105170011112222` (김하늘)
- `DE77500105170033334444` (박서준)

## 실행

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 확인

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- Health: `http://localhost:8000/health`

## 예시 테스트

### HR 조회
```bash
curl "http://localhost:8000/user_profile_details/장원영"
```

### 휴가 잔액 조회
```bash
curl "http://localhost:8000/time-off-balance/카리나"
```

### Banking 잔액 조회
```bash
curl -X POST "http://localhost:8000/balance-inquiry" \
  -H "Content-Type: application/json" \
  -d '{
    "iban": "DE89320895326389021994",
    "username": "teller",
    "password": "teller123"
  }'
```

### Banking 송금
```bash
curl -X POST "http://localhost:8000/iban-transfer" \
  -H "Content-Type: application/json" \
  -d '{
    "source_iban": "DE89320895326389021994",
    "destination_iban": "DE89929842579913662103",
    "amount_eur": 20,
    "username": "teller",
    "password": "teller123"
  }'
```

### 당좌대월 승인
```bash
curl -X POST "http://localhost:8000/approve-overdraft" \
  -H "Content-Type: application/json" \
  -d '{
    "iban": "DE89320895326389021994",
    "overdraft_limit_eur": 4000
  }'
```

### 수수료 환불
```bash
curl -X POST "http://localhost:8000/fee-reversal" \
  -H "Content-Type: application/json" \
  -d '{
    "iban": "DE89320895326389021994",
    "amount_eur": 35
  }'
```

## 운영 메모

- JSON 저장 방식은 **데모, 실습, 단일 서버 저트래픽 환경**에 적합합니다.
- 여러 worker를 두거나 동시 쓰기가 많아지면 SQLite/PostgreSQL 같은 DB가 더 적합합니다.
- 현재 코드는 파일 기반 저장이므로 서버가 파일 쓰기 권한을 가져야 합니다.
