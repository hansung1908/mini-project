# request : 날씨 데이터를 url을 통해 가져오기 위해 사용
import requests
# xmltodict : xml 데이터를 딕셔너리로 바꿔주기 위해 사용
import xmltodict
# datetime : 현재 시간
import datetime
# certifi : url 접속시 ssl 인증 오류 방지를 위해 사용
import certifi

# 현재 시간을 가져와 저장
tmp = datetime.datetime.now()
# url에 삽입하기 위해 형태 변경
now_date, now_time = str(tmp).replace("-", "").split()  # ex) 20231022

# 날씨 데이터 불러올 때 바로 불러오질 못해 -1시간씩 뒤로 미룬 시간의 날씨 설정
now_time = (now_time[0:2])
if now_time == "0000":
    now_date = int(now_date) - 1
    now_time = "2300"
elif int(now_time[0:2]) < 11:
    now_time = "0" + str(int(now_time[0:2]) - 1) + "00"  # ex) 0600
elif int(now_time[0:2]) < 24:
    now_time = str(int(now_time[0:2]) - 1) + "00"  # ex) 0600

# 서울, 부산, 대구, 인천, 광주, 대전, 울산, 경기, 충북, 충남, 전북, 전남, 경북, 경남, 제주, 강원순으로 좌표값
xy_list = [(60, 127), (98, 76), (89, 90), (55, 124), (58, 74), (67, 100), (102, 84),
           (60, 120), (69, 107), (68, 100), (63, 89), (51, 67), (89, 91), (91, 77), (52, 38), (73, 134)]

# 공공데이터 포털에서 단기예보api를 사용하기 위한 api키
api_key = "1%2FCFOLYKPhbqr5KCMfu2IA4Zl25N6B7KedYBRbxuh3AbeigZpcJtFG3pdO9DUDgohN8Qe2L%2BdHjidB1dwABAaQ%3D%3D"

# 각 지역 이름
locations = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "경기", "충북", "충남", "전북", "전남", "경북", "경남", "제주", "강원"]

# 각 지역의 온도, 강수량, 풍속
temperature = []
precipitation = []
wind_speed = []

# 지역 수 만큼 각 좌표에 해당하는 온도, 강수량, 풍속 정보를 각 리스트에 담아줌
for i in range(0, len(xy_list)):
    # 해당 url에 api키, 시간대, 좌표 정보를 넣어줘 데이터를 띄움
    url = ('http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey={'
           '}&numOfRows=10&pageNo=1&base_date={}&base_time={}&nx={}&ny={}') \
        .format(api_key, now_date, now_time, xy_list[i][0], xy_list[i][1])

    # 해당 url에 띄워진 데이터를 크롤링해서 가져옴
    # 이때 ssl 인증서 오류가 발생할 수 있으므로 verify=certifi.where() 옵션을 통해 인증서를 찾아서 직접 인증
    content = requests.get(url, verify=certifi.where()).content
    # 가져온 데이터를 딕셔너리 형태로 변경
    dict = xmltodict.parse(content)

    # 각 데이터에서 필요한 부분만 가져와 각 리스트에 추가
    temperature.append(dict['response']['body']['items']['item'][3]['obsrValue'])  # 기온
    precipitation.append(dict['response']['body']['items']['item'][2]['obsrValue'])  # 강수량
    wind_speed.append(dict['response']['body']['items']['item'][7]['obsrValue'])  # 풍속

# 지역 데이터와 날씨 데이터를 딕셔너리로 정리
weather_data = {}
for i in range(len(locations)):
    weather_data[locations[i]] = {
        "기온": float(temperature[i]),
        "강수량": precipitation[i],
        "풍속": wind_speed[i]
    }