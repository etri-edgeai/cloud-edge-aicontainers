# 현재위치 좌표 얻기
import requests, json
from geopy.geocoders import Nominatim


## 위치 좌표 얻어주는 사이트 활용
def current_location():
    here_req = requests.get("http://www.geoplugin.net/json.gp")

    if (here_req.status_code != 200):
        print("현재좌표를 불러올 수 없음")
    else:
        location = json.loads(here_req.text)
        crd = {"lat": str(location["geoplugin_latitude"]), "lng": str(location["geoplugin_longitude"])}

    return crd

# crd = current_location()
# print(crd)



## 지오코딩. 한글 주소를 위 경도로 변환
def geocoding(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}

    return crd

crd = geocoding("여수시 중앙동 246-1")
print(crd['lat'])
print(crd['lng'])
