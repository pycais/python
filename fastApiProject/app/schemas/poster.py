"""
@author: cs
@version: 1.0.0
@file: poster.py
@time: 2024/6/1 21:20
@description: 
"""
from datetime import datetime
from typing import Union, List

from pydantic import BaseModel

from app.schemas.base_response import SuccessResponse


class PosterBase(BaseModel):
    douban_id: str
    movie_name: str
    image_url: str
    name_id: Union[int, None]
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True


class ShowPoster(SuccessResponse):
    data: Union[List[PosterBase], None]
    total: int


class PosterCreate(PosterBase):
    pass


class PosterUpdate(PosterBase):
    pass


class Poster(PosterBase):
    id: int

    class Config:
        orm_mode = True


class PageInfo(BaseModel):
    pageSize: int
    currentPage: int


class RequestParams(BaseModel):
    doubanId: str
    movieName: str
    imageType: Union[List[str]]
    pageInfo: PageInfo
