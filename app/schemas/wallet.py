from pydantic import BaseModel, Field, field_validator


class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: float = 0

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    @field_validator("initial_balance")
    @classmethod
    def balance_not_negative(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Initial balance cannot be negative")
        return value
