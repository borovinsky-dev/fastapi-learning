
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

# Инициализация FastAPI приложения
app = FastAPI(title="Учебный проект FastAPI")

balance = {}


class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str | None = Field(None, max_length=255)

    @field_validator("wallet_name")
    @classmethod
    def wallet_name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Wallet name cannot be empty")
        return v

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v


class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: float = 0

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v

    @field_validator("initial_balance")
    @classmethod
    def balance_not_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Initial balance cannot be negative")
        return v


@app.get("/balance")
def get_balance(
    wallet_name: str | None = None,
) -> dict[str, str | float]:
    if wallet_name is None:
        return {"total_balance": sum(balance.values())}

    if wallet_name not in balance:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found",
        )

    return {"wallet": wallet_name, "balance": balance[wallet_name]}


@app.post("/wallets")
def create_wallet(wallet: CreateWalletRequest) -> dict[str, str | float]:
    if wallet.name in balance:
        raise HTTPException(
            status_code=400,
            detail=f"Wallet {wallet.name} already exists",
        )

    balance[wallet.name] = wallet.initial_balance

    return {
        "message": f"Wallet {wallet.name} created",
        "wallet": wallet.name,
        "balance": balance[wallet.name],
    }


@app.post("/operations/income")
def add_income(operation: OperationRequest) -> dict[str, str | float | None]:
    if operation.wallet_name not in balance:
        raise HTTPException(
            status_code=404,
            detail=f"{operation.wallet_name} not found",
        )

    balance[operation.wallet_name] += operation.amount

    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": balance[operation.wallet_name],
    }


@app.post("/operations/expense")
def add_expense(operation: OperationRequest) -> dict[str, str | float | None]:
    if operation.wallet_name not in balance:
        raise HTTPException(
            status_code=404,
            detail=f"{operation.wallet_name} not found",
        )

    if balance[operation.wallet_name] < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds: {balance[operation.wallet_name]}",
        )

    balance[operation.wallet_name] -= operation.amount

    return {
        "message": "Expense added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": balance[operation.wallet_name],
    }
