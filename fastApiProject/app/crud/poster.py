"""
@author: cs
@version: 1.0.0
@file: poster.py
@time: 2024/6/1 21:18
@description: 
"""
# app/crud.py
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.models.artist import Movie
from app.schemas.poster import RequestParams


def get_poster(db: Session, product_id: int):
    return db.query(Movie).filter(Movie.id == product_id).first()


def get_posters(db: Session, params: RequestParams):
    page_size = params.pageInfo.pageSize
    current_page = params.pageInfo.currentPage
    data = db.query(Movie).filter(
        Movie.douban_id == params.doubanId if params.doubanId else True,
        Movie.movie_name == params.movieName if params.movieName else True
    )
    total = data.count()
    data = data.offset((current_page - 1) * page_size).limit(page_size).all()
    return data, total


def update_poster(db: Session, product_id: int, product):
    db_product = get_poster(db, product_id)
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_poster(db: Session, product_id: int):
    db_product = get_poster(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
