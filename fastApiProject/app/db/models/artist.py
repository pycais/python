"""
@author: cs
@version: 1.0.0
@file: artist.py
@time: 2024/5/21 2:03
@description: 影视明星模型
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from app.db.session import Base


class ArtistName(Base):
    __tablename__ = "artist_name"
    __table_args = {'comment': '影视演员表'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_id = Column(String(32), uniquet=True, index=True, comment='演员ID')
    zh_name = Column(String(128), comment='中文名字')
    en_name = Column(String(128), comment='英文名字')
    create_time = Column(DateTime, server_default=datetime.now(), comment='创建时间')




