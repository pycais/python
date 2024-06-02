"""
@author: cs
@version: 1.0.0
@file: artist.py
@time: 2024/5/21 2:03
@description: 影视明星模型
"""

from sqlalchemy import Column, Integer, String, DateTime, func

from app.db.session import Base


class Movie(Base):
    __tablename__ = "movie"
    __table_args = {'comment': '影视演员表'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    douban_id = Column(String(32), comment='豆瓣ID')
    movie_name = Column(String(32), comment='影视名称')
    image_url = Column(String(256), comment='图片URL')
    name_id = Column(Integer, comment='影视名称ID')
    image_type = Column(String(16), comment='图片类型')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='创建时间')


class Artist(Base):
    __tablename__ = "artist"
    __table_args = {'comment': '影视演员表'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    douban_id = Column(String(32), comment='影视名称ID')
    movie_name = Column(String(64), comment='影视名称')
    name = Column(String(16), comment='演员名称')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='创建时间')
