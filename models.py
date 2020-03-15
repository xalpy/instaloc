# -*- coding: utf-8 -*-
"Структура таблицы базы данных"
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base



engine = create_engine('sqlite:///insta.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class InstLocations(Base):
    "Класс со структурой таблицы"
    __tablename__ = 'inst_locations'
    location_id = Column(Integer())
    location_name = Column(String())
    lttd = Column(String())
    lngt = Column(String())
    owner_id = Column(String())
    post_id = Column(Integer(), primary_key=True)
    caption = Column(String())
    picture = Column(String())
    comments_count = Column(Integer())
    likes_count = Column(Integer())

    def __init__(self, location_id=None, location_name=None, lttd=None, lngt=None,
                 owner_id=None, post_id=None, caption=None, picture=None,
                 comments_count=None, likes_count=None):
        self.location_id = location_id
        self.location_name = location_name
        self.lttd = lttd
        self.lngt = lngt
        self.owner_id = owner_id
        self.post_id = post_id
        self.caption = caption
        self.picture = picture
        self.comments_count = comments_count
        self.likes_count = likes_count





if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
