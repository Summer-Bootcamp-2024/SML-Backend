from pydantic import BaseModel

class CreditUpdate(BaseModel):
    credit: int