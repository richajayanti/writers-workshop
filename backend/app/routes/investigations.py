from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Investigation
from app.schemas import InvestigationCreate, InvestigationResponse, InvestigationList

router = APIRouter(prefix="/investigations")


# Query all investigations, return InvestigationList
@router.get("", response_model=InvestigationList)
def list_investigations(db: Session = Depends(get_db)):
    investigations = db.query(Investigation).all()
    return InvestigationList(investigations=investigations)

# Create an investigation from InvestigationCreate, return InvestigationResponse                                                                                                                                                                                                                        
@router.post("", response_model=InvestigationResponse)
def create_investigation(payload: InvestigationCreate, db: Session = Depends(get_db)):
    investigation = Investigation(title=payload.title, brain_dump=payload.brain_dump)
    db.add(investigation)
    db.commit()
    db.refresh(investigation)
    return investigation

# Get an investigation by ID, return InvestigationResponse
@router.get("/{id}", response_model=InvestigationResponse)
def get_investigation(id: int, db: Session = Depends(get_db)):
    investigation = db.query(Investigation).filter(Investigation.id == id).first()
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return investigation