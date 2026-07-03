from pydantic import BaseModel, ConfigDict
from datetime import datetime


class InvestigationCreate(BaseModel):
    title: str
    brain_dump: str

class InvestigationResponse(BaseModel):
    id: int
    title: str
    brain_dump: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Wrapping allows me room to add fields later without breaking response shape.
class InvestigationList(BaseModel):
    investigations: list[InvestigationResponse]
    