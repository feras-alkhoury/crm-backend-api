from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    company: str | None = None


class CustomerResponse(CustomerCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
