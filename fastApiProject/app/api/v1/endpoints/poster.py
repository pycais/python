"""
@author: cs
@version: 1.0.0
@file: poster.py
@time: 2024/6/1 21:18
@description: 
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dedps import get_db
from app.crud.poster import get_posters
from app.schemas.poster import ShowPoster, RequestParams

router = APIRouter()


@router.post("/data-list", response_model=ShowPoster)
def read_movies(params: RequestParams, db: Session = Depends(get_db)):
    movies, total = get_posters(db, params)
    return {'data': movies, 'total': total}
