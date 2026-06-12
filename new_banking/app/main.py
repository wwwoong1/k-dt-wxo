from __future__ import annotations

import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from threading import Lock
from typing import Any, Generator, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

APP_TITLE = "GFM Bank Unified Tool APIs"
APP_VERSION = "1.0.0"
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("BANK_DB_PATH", BASE_DIR / "bank.db"))
DB_LOCK = Lock()

TELLER_USERNAME = os.getenv("TELLER_USERNAME", "teller")
TELLER_PASSWORD = os.getenv("TELLER_PASSWORD", "teller123")


app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description="Unified API combining multiple banking services",
)


# -----------------------------
# Utilities
# -----------------------------
def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def q2(value: Decimal | float | int | str) -> float:
    dec = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(dec)


@contextmanager
def get_conn() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def authenticate_teller(username: Optional[str], password: Optional[str]) -> None:
    username = username or TELLER_USERNAME
    password = password or TELLER_PASSWORD
    if username != TELLER_USERNAME or password != TELLER_PASSWORD:
        raise HTTPException(status_code=401, detail="Bad credentials")


def get_account_by_iban(conn: sqlite3.Connection, iban: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM accounts WHERE iban = ?",
        (iban,),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="IBAN not found")
    return row


def get_balances(conn: sqlite3.Connection, account_id: str) -> dict[str, float]:
    row = conn.execute(
        "SELECT COALESCE(SUM(amount_eur), 0) AS current_balance FROM transactions WHERE account_id = ?",
        (account_id,),
    ).fetchone()
    current_balance = q2(row["current_balance"] if row else 0)

    account = conn.execute(
        "SELECT overdraft_limit_eur FROM accounts WHERE account_id = ?",
        (account_id,),
    ).fetchone()
    overdraft_limit = q2(account["overdraft_limit_eur"] if account else 0)
    available_balance = q2(Decimal(str(current_balance)) + Decimal(str(overdraft_limit)))
    return {
        "current_balance_eur": current_balance,
        "overdraft_limit_eur": overdraft_limit,
        "available_balance_eur": available_balance,
    }


def create_transaction(
    conn: sqlite3.Connection,
    *,
    account_id: str,
    amount_eur: float,
    tx_type: str,
    description: str,
    counterparty_iban: Optional[str] = None,
) -> tuple[str, str]:
    transaction_id = str(uuid.uuid4())
    booking_ts = now_iso()
    conn.execute(
        """
        INSERT INTO transactions (
            transaction_id,
            account_id,
            booking_ts,
            amount_eur,
            type,
            description,
            counterparty_iban
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            transaction_id,
            account_id,
            booking_ts,
            q2(amount_eur),
            tx_type,
            description,
            counterparty_iban,
        ),
    )
    return transaction_id, booking_ts


# -----------------------------
# Schemas
# -----------------------------
class IbanTransferRequest(BaseModel):
    source_iban: str = Field(..., examples=["DE89320895326389021994"])
    destination_iban: str = Field(..., examples=["DE89929842579913662103"])
    amount_eur: float = Field(..., gt=0, examples=[100.5])
    username: Optional[str] = Field(default=TELLER_USERNAME)
    password: Optional[str] = Field(default=TELLER_PASSWORD)


class IbanTransferResponse(BaseModel):
    status: str
    source_iban: str
    destination_iban: str
    amount_eur: float
    debit_tx: str
    credit_tx: str
    timestamp: str
    new_balance_eur: float


class BalanceInquiryRequest(BaseModel):
    iban: str = Field(..., examples=["DE89320895326389021994"])
    username: Optional[str] = Field(default=TELLER_USERNAME)
    password: Optional[str] = Field(default=TELLER_PASSWORD)


class RecentTransaction(BaseModel):
    transaction_id: str
    account_id: str
    booking_ts: str
    amount_eur: float
    type: str
    description: Optional[str] = None
    counterparty_iban: Optional[str] = None


class BalanceInquiryResponse(BaseModel):
    iban: str
    account_id: str
    current_balance_eur: float
    overdraft_limit_eur: float
    available_balance_eur: float
    recent_transactions: list[RecentTransaction]


class FeeReversalRequest(BaseModel):
    iban: str = Field(..., examples=["DE89320895326389021994"])
    amount_eur: float = Field(..., gt=0, examples=[50])


class FeeReversalResponse(BaseModel):
    status: str
    iban: str
    customer_name: str
    amount_eur: float
    transaction_id: str
    booking_ts: str
    new_balance_eur: float
    message: str


class ApproveOverdraftRequest(BaseModel):
    iban: str = Field(..., examples=["DE89320895326389021994"])
    overdraft_limit_eur: float = Field(..., ge=0, le=10000, examples=[5000])

    @field_validator("overdraft_limit_eur")
    @classmethod
    def validate_limit(cls, value: float) -> float:
        if value < 0 or value > 10000:
            raise ValueError("Overdraft limit must be between 0 and 10,000 EUR")
        return value


class ApproveOverdraftResponse(BaseModel):
    account_id: str
    iban: str
    customer_name: str
    overdraft_limit_eur: float
    message: str


# -----------------------------
# Database bootstrap
# -----------------------------
def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DB_LOCK:
        with get_conn() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id TEXT PRIMARY KEY,
                    iban TEXT UNIQUE NOT NULL,
                    customer_name TEXT NOT NULL,
                    overdraft_limit_eur REAL NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    account_id TEXT NOT NULL,
                    booking_ts TEXT NOT NULL,
                    amount_eur REAL NOT NULL,
                    type TEXT NOT NULL,
                    description TEXT,
                    counterparty_iban TEXT,
                    FOREIGN KEY(account_id) REFERENCES accounts(account_id)
                );
                """
            )

            count = conn.execute("SELECT COUNT(*) AS cnt FROM accounts").fetchone()["cnt"]
            if count == 0:
                seed_accounts(conn)
                seed_transactions(conn)
            conn.commit()


def seed_accounts(conn: sqlite3.Connection) -> None:
    accounts = [
        ("ACC-1001", "DE89320895326389021994", "John Example", 0.0),
        ("ACC-1002", "DE89929842579913662103", "Mia Example", 0.0),
        ("ACC-1003", "DE44500105175407324931", "GFM Savings Customer", 500.0),
    ]
    conn.executemany(
        "INSERT INTO accounts (account_id, iban, customer_name, overdraft_limit_eur) VALUES (?, ?, ?, ?)",
        accounts,
    )


def seed_transactions(conn: sqlite3.Connection) -> None:
    seed_data = [
        ("ACC-1001", "2026-04-10T09:00:00+00:00", 4800.0, "DEPOSIT", "Initial balance", None),
        ("ACC-1001", "2026-04-11T10:30:00+00:00", -50.0, "WITHDRAWAL", "ATM Withdrawal", None),
        ("ACC-1001", "2026-04-12T08:15:00+00:00", 200.0, "DEPOSIT", "Direct Deposit", None),
        ("ACC-1001", "2026-04-13T18:20:00+00:00", -30.0, "PURCHASE", "Grocery Store", None),
        ("ACC-1001", "2026-04-14T09:10:00+00:00", 80.0, "DEPOSIT", "Refund", None),
        ("ACC-1002", "2026-04-10T09:00:00+00:00", 2500.0, "DEPOSIT", "Initial balance", None),
        ("ACC-1003", "2026-04-10T09:00:00+00:00", 1200.0, "DEPOSIT", "Initial balance", None),
    ]
    for account_id, booking_ts, amount_eur, tx_type, description, counterparty_iban in seed_data:
        conn.execute(
            """
            INSERT INTO transactions (
                transaction_id, account_id, booking_ts, amount_eur, type, description, counterparty_iban
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (str(uuid.uuid4()), account_id, booking_ts, q2(amount_eur), tx_type, description, counterparty_iban),
        )


@app.on_event("startup")
def startup_event() -> None:
    init_db()


# -----------------------------
# Health / utility
# -----------------------------
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": now_iso()}


# -----------------------------
# API endpoints
# -----------------------------
@app.post("/balance-inquiry", response_model=BalanceInquiryResponse)
def balance_inquiry(payload: BalanceInquiryRequest) -> BalanceInquiryResponse:
    authenticate_teller(payload.username, payload.password)

    with DB_LOCK:
        with get_conn() as conn:
            account = get_account_by_iban(conn, payload.iban)
            balances = get_balances(conn, account["account_id"])
            tx_rows = conn.execute(
                """
                SELECT transaction_id, account_id, booking_ts, amount_eur, type, description, counterparty_iban
                FROM transactions
                WHERE account_id = ?
                ORDER BY booking_ts DESC
                LIMIT 10
                """,
                (account["account_id"],),
            ).fetchall()

    recent_transactions = [
        RecentTransaction(
            transaction_id=row["transaction_id"],
            account_id=row["account_id"],
            booking_ts=row["booking_ts"],
            amount_eur=q2(row["amount_eur"]),
            type=row["type"],
            description=row["description"],
            counterparty_iban=row["counterparty_iban"],
        )
        for row in tx_rows
    ]

    return BalanceInquiryResponse(
        iban=account["iban"],
        account_id=account["account_id"],
        current_balance_eur=balances["current_balance_eur"],
        overdraft_limit_eur=balances["overdraft_limit_eur"],
        available_balance_eur=balances["available_balance_eur"],
        recent_transactions=recent_transactions,
    )


@app.post("/iban-transfer", response_model=IbanTransferResponse)
def iban_transfer(payload: IbanTransferRequest) -> IbanTransferResponse:
    authenticate_teller(payload.username, payload.password)

    if payload.source_iban == payload.destination_iban:
        raise HTTPException(status_code=400, detail="Source and destination IBAN must be different")

    with DB_LOCK:
        with get_conn() as conn:
            source = conn.execute("SELECT * FROM accounts WHERE iban = ?", (payload.source_iban,)).fetchone()
            destination = conn.execute("SELECT * FROM accounts WHERE iban = ?", (payload.destination_iban,)).fetchone()
            if source is None or destination is None:
                raise HTTPException(status_code=404, detail="Source or destination IBAN not found")

            source_balances = get_balances(conn, source["account_id"])
            amount = q2(payload.amount_eur)
            if Decimal(str(source_balances["available_balance_eur"])) < Decimal(str(amount)):
                raise HTTPException(
                    status_code=403,
                    detail=(
                        f"Insufficient funds. Balance {source_balances['current_balance_eur']}, "
                        f"overdraft {source_balances['overdraft_limit_eur']}"
                    ),
                )

            debit_tx, booking_ts = create_transaction(
                conn,
                account_id=source["account_id"],
                amount_eur=-amount,
                tx_type="TRANSFER_OUT",
                description=f"Transfer to {payload.destination_iban}",
                counterparty_iban=payload.destination_iban,
            )
            credit_tx, _ = create_transaction(
                conn,
                account_id=destination["account_id"],
                amount_eur=amount,
                tx_type="TRANSFER_IN",
                description=f"Transfer from {payload.source_iban}",
                counterparty_iban=payload.source_iban,
            )
            conn.commit()

            new_source_balances = get_balances(conn, source["account_id"])

    return IbanTransferResponse(
        status="success",
        source_iban=payload.source_iban,
        destination_iban=payload.destination_iban,
        amount_eur=amount,
        debit_tx=debit_tx,
        credit_tx=credit_tx,
        timestamp=booking_ts,
        new_balance_eur=new_source_balances["current_balance_eur"],
    )


@app.post("/fee-reversal", response_model=FeeReversalResponse)
def fee_reversal(payload: FeeReversalRequest) -> FeeReversalResponse:
    if payload.amount_eur <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    with DB_LOCK:
        with get_conn() as conn:
            account = get_account_by_iban(conn, payload.iban)
            tx_id, booking_ts = create_transaction(
                conn,
                account_id=account["account_id"],
                amount_eur=payload.amount_eur,
                tx_type="FEE_REVERSAL",
                description="Fee reversal",
            )
            conn.commit()
            balances = get_balances(conn, account["account_id"])

    amount = q2(payload.amount_eur)
    return FeeReversalResponse(
        status="success",
        iban=account["iban"],
        customer_name=account["customer_name"],
        amount_eur=amount,
        transaction_id=tx_id,
        booking_ts=booking_ts,
        new_balance_eur=balances["current_balance_eur"],
        message=f"Fee reversal of {amount:.2f} EUR processed successfully.",
    )


@app.post("/approve-overdraft", response_model=ApproveOverdraftResponse)
def approve_overdraft(payload: ApproveOverdraftRequest) -> ApproveOverdraftResponse:
    if payload.overdraft_limit_eur < 0 or payload.overdraft_limit_eur > 10000:
        raise HTTPException(status_code=400, detail="Overdraft limit must be between 0 and 10,000 EUR")

    with DB_LOCK:
        with get_conn() as conn:
            account = get_account_by_iban(conn, payload.iban)
            conn.execute(
                "UPDATE accounts SET overdraft_limit_eur = ? WHERE account_id = ?",
                (q2(payload.overdraft_limit_eur), account["account_id"]),
            )
            conn.commit()
            updated = conn.execute(
                "SELECT * FROM accounts WHERE account_id = ?",
                (account["account_id"],),
            ).fetchone()

    limit = q2(payload.overdraft_limit_eur)
    return ApproveOverdraftResponse(
        account_id=updated["account_id"],
        iban=updated["iban"],
        customer_name=updated["customer_name"],
        overdraft_limit_eur=limit,
        message=f"Overdraft limit updated to {limit:.2f} EUR.",
    )
