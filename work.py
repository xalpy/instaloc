# -*- coding: utf-8 -*-
"файл для работы с базой"
from models import InstLocations, db_session
from sqlalchemy.exc import OperationalError, IntegrityError

def db_add(location_id, location_name, lttd, lngt, owner_id, post_id,
            caption, picture, comments_count, likes_count):
    'Функция для добавления данных в БД'
    post = InstLocations(location_id, location_name, lttd, lngt, owner_id, post_id,
                         caption, picture, comments_count, likes_count)
    try:
        db_session.add(post) 
        db_session.commit()
    except (OperationalError, IntegrityError): 
        db_session.rollback()
