from pydantic import BaseModel, Field
from typing import Optional

class AgentCarRequest(BaseModel):
    make: str
    model: str
    price: float
    color: str
    userId: str  # agentId
    cityId: str
    kmsDriven: int