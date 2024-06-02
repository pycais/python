from typing import Union, List, Optional, Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = []


class SuccessResponse(BaseResponse):
    code: int = 0
    message: str = 'success'
    data: List[None] = []


class PosterBase(BaseModel):
    douban_id: str
    movie_name: str
    image_url: str
    name_id: str
    create_time: str
    update_time: str


class ShowPoster(SuccessResponse):
    data: Union[PosterBase, None, List]
    total: int


class Qq(BaseModel):
    dd: List[str]


if __name__ == '__main__':
    q = Qq(dd=[])
    print(q)
