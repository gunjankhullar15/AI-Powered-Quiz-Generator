from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.model import Weightage
from app.schemas.schema import WeightageResponse
from app.database.database import get_db

router = APIRouter(prefix="/weightages")

@router.get("/get-weightages", response_model=list[WeightageResponse])
async def get_weightages(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    
    result = await db.execute(select(Weightage))
    weightages = result.scalars().all()
    
    if not weightages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No weightages found")
    
    return weightages