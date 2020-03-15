# -*- coding: utf-8 -*-
"""
программа собирает данные по постам и местоположению где были сделанны фотографии
"""
from argparse import ArgumentParser
from multiprocessing import Pool
import urllib.parse
from json import JSONDecodeError

from requests import get as reqget
from work import db_add


def get_req(url: str) -> dict:
    "Функция для запросов"
    req = reqget(url)
    try:
        json = req.json()
        return json
    except JSONDecodeError:
        print(req)
    


def get_info(json: dict) -> None:
    "сортировка данных для дальнейшего добавления в БД"
    location = json['graphql']['location']
    loc_id = location['id']
    loc_name = location['name']
    lat = location['lat']
    lng = location['lng']
    loc_post = location['edge_location_to_media']['edges']
    for item in loc_post:
        node = item['node']
        owner_id = node['owner']['id']
        post_id = node['id']
        try:
            caption = node['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            caption = ''
        picture = node['display_url']
        comments_count = node['edge_media_to_comment']['count']
        likes_count = node['edge_liked_by']['count']
        db_add(loc_id, loc_name, lat, lng, owner_id, post_id, caption,
               picture, comments_count, likes_count)




def get_jsons(places_list: list) -> list:
    "Получение json'ов с постами в локациях"
    json_list = []
    for item in places_list:
        url = f'https://www.instagram.com/explore/locations/{item}/?__a=1'
        json = get_req(url)
        json_list.append(json)
    return json_list




def get_place_id(place: str) -> list:
    "Функция для сбора айди локаций"
    url = f'https://www.instagram.com/web/search/topsearch/?context=blended&query={place}'
    json = get_req(url)
    places = json['places']
    places_list = [i['place']['location']['pk'] for i in places]
    return places_list


def main():
    'Главная функция для запуска'
    parser = ArgumentParser()
    parser.add_argument("--place", help='название места, в формате: "Москва+сити", "Россия+москва"',
                        type=str, nargs='+')
    
    args = parser.parse_args()
    place = args.place
    if isinstance(place, list):
        place = '+'.join(place)

    place = place.replace(' ', '+')
    place = urllib.parse.quote_plus(place)
    places_list = get_place_id(place)
    json_list = get_jsons(places_list)

    if len(json_list) >= 8:
        workers = 8
    else:
        workers = len(json_list)

    with Pool(workers) as p:
        p.map(get_info, json_list)




if __name__ == '__main__':
    main()
