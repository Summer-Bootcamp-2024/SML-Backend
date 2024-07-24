from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.backend.schemas.search.search_schema import SearchFilters
from Backend.backend.database import get_db
from Backend.backend.crud.search_crud import search_users_by_filters

router = APIRouter()

@router.get("")
async def search(user_id: int, search: str, filter_by: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    filters = SearchFilters(user_id=user_id, search=search, filter_by=filter_by)
    try:
        results = await search_users_by_filters(filters, db)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
