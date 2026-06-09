from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "users.json"

app = FastAPI(
    title="HR Automation",
    description="API for retrieving employee details and updating profile information",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserProfile(BaseModel):
    user_id: str = Field(description="Unique user ID")
    name: str
    title: str
    address: str
    time_off_balance: int


class CreateUserRequest(BaseModel):
    name: str = Field(description="Full name of the user.")
    time_off_balance: int = Field(description="Initial time-off balance in days.")
    title: str = Field(description="Job title of the user.")
    address: str = Field(description="Address of the user.")


class TimeOffRequest(BaseModel):
    name: str = Field(description="The name of the user.")
    from_date: date = Field(description="Start date of the time-off request (YYYY-MM-DD).")
    to_date: date = Field(description="End date of the time-off request (YYYY-MM-DD).")


class UpdateTitleRequest(BaseModel):
    name: str = Field(description="The name of the user.")
    new_title: str = Field(description="The updated job title of the user.")


class UpdateAddressRequest(BaseModel):
    name: str = Field(description="The name of the user.")
    new_address: str = Field(description="The updated address of the user.")


DEFAULT_USERS = {
    "장원영": {
        "user_id": "EMP-1001",
        "name": "장원영",
        "title": "AI Engineer",
        "address": "서울특별시 강남구 테헤란로 101",
        "time_off_balance": 15,
    },
    "카리나": {
        "user_id": "EMP-1002",
        "name": "카리나",
        "title": "Data Engineer",
        "address": "서울특별시 서초구 서초대로 202",
        "time_off_balance": 12,
    },
    "안유진": {
        "user_id": "EMP-1003",
        "name": "안유진",
        "title": "HR Specialist",
        "address": "서울특별시 송파구 올림픽로 303",
        "time_off_balance": 18,
    },
    "민지": {
        "user_id": "EMP-1004",
        "name": "민지",
        "title": "Product Manager",
        "address": "서울특별시 마포구 월드컵북로 404",
        "time_off_balance": 10,
    },
    "해린": {
        "user_id": "EMP-1005",
        "name": "해린",
        "title": "Software Engineer",
        "address": "서울특별시 영등포구 국제금융로 505",
        "time_off_balance": 20,
    },
    "지민": {
        "user_id": "EMP-1006",
        "name": "지민",
        "title": "Senior AI Engineer",
        "address": "경기도 성남시 분당구 판교역로 606",
        "time_off_balance": 14,
    },
    "정국": {
        "user_id": "EMP-1007",
        "name": "정국",
        "title": "Platform Engineer",
        "address": "서울특별시 강서구 마곡중앙로 707",
        "time_off_balance": 11,
    },
    "차은우": {
        "user_id": "EMP-1008",
        "name": "차은우",
        "title": "UX Designer",
        "address": "서울특별시 용산구 한강대로 808",
        "time_off_balance": 16,
    },
}


def ensure_data_file() -> None:
    if not DATA_FILE.exists():
        write_users(DEFAULT_USERS)



def read_users() -> dict[str, dict[str, Any]]:
    ensure_data_file()
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)



def write_users(users: dict[str, dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)



def normalize_name(name: str) -> str:
    return unquote(name).strip()



def get_user_or_404(name: str) -> dict[str, Any]:
    users = read_users()
    normalized = normalize_name(name)
    user = users.get(normalized)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{normalized}' not found")
    return user


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "HR Automation API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/user_profile_details/{name}")
def get_user_profile(name: str) -> dict[str, Any]:
    user = get_user_or_404(name)
    return {
        "name": user["name"],
        "title": user["title"],
        "address": user["address"],
        "time_off_balance": user["time_off_balance"],
        "user_id": user["user_id"],
    }


@app.get("/time-off-balance/{name}")
def get_time_off_balance(name: str) -> str:
    user = get_user_or_404(name)
    return f"{user['name']}님의 남은 휴가 일수는 {user['time_off_balance']}일입니다."


@app.post("/request-time-off")
def request_time_off(payload: TimeOffRequest) -> str:
    if payload.to_date < payload.from_date:
        raise HTTPException(status_code=400, detail="to_date must be on or after from_date")

    requested_days = (payload.to_date - payload.from_date).days + 1
    users = read_users()
    name = normalize_name(payload.name)
    user = users.get(name)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{name}' not found")

    if user["time_off_balance"] < requested_days:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Insufficient time off balance. Remaining: {user['time_off_balance']} day(s), "
                f"Requested: {requested_days} day(s)"
            ),
        )

    user["time_off_balance"] -= requested_days
    users[name] = user
    write_users(users)

    return (
        f"{user['name']}님의 휴가가 신청되었습니다. "
        f"기간: {payload.from_date.isoformat()} ~ {payload.to_date.isoformat()}, "
        f"사용 일수: {requested_days}일, 남은 휴가: {user['time_off_balance']}일"
    )


@app.put("/update-title")
def update_title(payload: UpdateTitleRequest) -> str:
    users = read_users()
    name = normalize_name(payload.name)
    user = users.get(name)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{name}' not found")

    old_title = user["title"]
    user["title"] = payload.new_title.strip()
    users[name] = user
    write_users(users)

    return f"{user['name']}님의 직책이 '{old_title}'에서 '{user['title']}'(으)로 변경되었습니다."


@app.put("/update-address")
def update_address(payload: UpdateAddressRequest) -> str:
    users = read_users()
    name = normalize_name(payload.name)
    user = users.get(name)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{name}' not found")

    old_address = user["address"]
    user["address"] = payload.new_address.strip()
    users[name] = user
    write_users(users)

    return f"{user['name']}님의 주소가 '{old_address}'에서 '{user['address']}'(으)로 변경되었습니다."


@app.post("/create-user")
def create_user(payload: CreateUserRequest) -> str:
    users = read_users()
    name = normalize_name(payload.name)

    if name in users:
        raise HTTPException(status_code=409, detail=f"User '{name}' already exists")

    user_id = f"EMP-{str(uuid4().int)[:8]}"
    users[name] = {
        "user_id": user_id,
        "name": name,
        "title": payload.title.strip(),
        "address": payload.address.strip(),
        "time_off_balance": payload.time_off_balance,
    }
    write_users(users)

    return f"사용자 '{name}'가 생성되었습니다. user_id={user_id}"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
