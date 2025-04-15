from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from bson import ObjectId

class AgentModel(BaseModel):
    agentId: str = Field(alias="_id")
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role_id: str  # This should match the ObjectId of the agent role

    @validator("agentId", pre=True, always=True)
    def convert_object_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator("role_id", pre=True, always=True)
    def convert_role_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
