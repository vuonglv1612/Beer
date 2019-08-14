import json
import requests
import argparse
import time

NUM_OF_PLACE = 50

# LOCATION = '21.013111,105.799972'
KEYWORD = "beer"
RADIUS = 2000  # meters


def api_key(file_path):
    api_key = None
    try:
        with open(file_path, "rt") as api_file:
            api_key = api_file.readline()
            return api_key
    except (FileExistsError, FileNotFoundError) as e:
        print(e)
    finally:
        return api_key


API_KEY = api_key("API_key.txt")


def generate_point(lat, lng, name, address):
    '''
    Trả về một `dict` có dạng một `point` trong GeoJSON
    :param lat: latitude, tức là vĩ độ của điểm
    :param lng: longitude, tức là kinh độ của điểm
    :param name: Tên của địa điểm
    :param address: Địa chỉ của địa điểm
    :rtype: Dictionary
    '''
    point = {
        "type": "Feature",
        "properties": {
            "name": "",
            "address": ""
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                0,
                0
            ]
        }
    }
    point.get('properties').update(name=name)
    point.get('properties').update(address=address)
    point.get('geometry').update(coordinates=[lng, lat])
    return point


def points(page_response):
    '''
    Trả về một generator
    đại diện cho tất cả các `point` trong một page_response.
    :param page_response: một trang của response mà API trả về
    :rtype: Generator
    '''
    for result in page_response.get('results'):
        name = result.get('name')
        address = result.get('vicinity')
        location = result.get('geometry').get('location')
        latitude = location.get('lat')
        longitude = location.get('lng')
        yield generate_point(latitude, longitude, name, address)


def next_page(url, API_key, next_page_token):
    '''
    Trả về một response của page tiếp theo dựa vào `next_page_token`
    :param url: đường dẫn của API khi chưa có parameters
    :param API_key: API key
    :param next_page_token: token được API trả về
    :rtype: Dictionary
    '''
    params = {
        'key': API_key,
        'pagetoken': next_page_token
    }
    response = requests.get(url, params=params)
    return response.json()


def places(location):
    '''
    Trả về một generator đại diện cho các `điểm`
    mà API tìm được xung quanh `location`
    :param location: `str` tọa độ dạng `"latitude,longitude"`
    example: `'21.013111,105.799972'`
    :rtype: Generator
    '''
    # Đường dẫn của API khi chưa có parameters
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': location,
        'radius': RADIUS,
        'keyword': KEYWORD,
        'key': API_KEY
    }
    session = requests.Session()
    # Duyệt trang đầu tiên
    response = session.get(url, params=params).json()
    for point in points(response):
        yield point
    # Nếu thấy `next_page_token` thì xét tiếp các trang sau
    while 'next_page_token' in response:
        time.sleep(10)  # sleep 10s để API cho phép gửi request tiếp
        response = next_page(url, API_KEY, response['next_page_token'])
        for point in points(response):
            yield point


def generate_geoJSON_file(location, file_path):
    '''
    Tạo một file GeoJSON, file này chứa các `point`
    mà API tìm được xung quanh `location`
    :param location: `str` tọa độ dạng `"latitude,longitude"`
    example: `'21.013111,105.799972'`
    :param file_path: Đường dẫn tới file GeoJSON cần tạo
    :rtype: None
    '''
    MAP = {
        "type": "FeatureCollection",
        "features": []
    }
    times = 0
    for place in places(location):
        times += 1
        if times <= NUM_OF_PLACE:
            MAP["features"].append(place)
    with open(file_path, "wt", encoding="utf-8") as geo_file:
        json.dump(MAP, geo_file, ensure_ascii=False, indent=4)


def main():
    '''
    Tìm 50 quán bia trong bán kính 2km gần tọa độ nhập vào,
    xuât file GeoJSON chứa các điểm đại diện cho các quán bia tìm được
    Chạy script bằng lệnh có dạng:
    beer.py `tọa độ` `path của file cần tạo`
    '''
    # Parse args
    paser = argparse.ArgumentParser(description="Tìm 50 quán bia gần tọa độ nhập vào, trong bán kính 2km") # NOQA
    paser.add_argument("location", help="tọa độ(VD: '21.013111,105.799972')",type=str) # NOQA
    paser.add_argument("geoJSON_file_path", help="Đường dẫn của file map(VD: 'beer_hub_nearby_me.geojson')",type=str) # NOQA
    args = paser.parse_args()

    location = args.location
    file_path = args.geoJSON_file_path
    generate_geoJSON_file(location, file_path)
    print("DONE")


if __name__ == "__main__":
    main()
