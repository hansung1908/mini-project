import requests, json
import xmltodict
import openpyxl
import mysql.connector
import os
import pandas as pd

api_key = "1%2FCFOLYKPhbqr5KCMfu2IA4Zl25N6B7KedYBRbxuh3AbeigZpcJtFG3pdO9DUDgohN8Qe2L%2BdHjidB1dwABAaQ%3D%3D"

# 서울, 부산, 대구, 인천, 광주, 대전, 울산, 경기(수원), 충북(청주), 충남(천안), 전북(전주), 전남(목포), 경북(영천), 경남(창원), 제주, 강원(춘천)순으로 좌표값
locations = [108, 159, 143, 112, 156, 133, 152, 119, 131, 232, 146, 165, 281, 155, 184, 101]

# 호출시 최대 출력 갯수 (1000 이상은 안됨)
numOfRows = 999

# 시작 날짜
startDts = [20150101, 20170101, 20190101, 20210101, 20230101]

# 끝 날짜
endDts = [20161231, 20181231, 20201231, 20221231, 20240430]

for location in locations:
    for startDt, endDt in zip(startDts, endDts):
        url = f'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList?serviceKey={api_key}&numOfRows={numOfRows}&pageNo=1&dataCd=ASOS&dateCd=DAY&startDt={startDt}&endDt={endDt}&stnIds={location}'
        print(url)

        content = requests.get(url).content
        dict = xmltodict.parse(content)

        # 딕셔너리를 JSON 파일로 저장
        with open('data.json', 'w', encoding='utf-8') as json_file:
            json.dump(dict['response']['body']['items']['item'], json_file, ensure_ascii=False, indent=4)

        # MySQL 연결 설정
        db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='capstone'
        )

        # 커서 생성
        cursor = db_connection.cursor()

        # JSON 파일 읽기
        with open('data.json', 'r', encoding='UTF8') as file:
            data = json.load(file)

        # 테이블 있으면 삭제후 재설정
        # sql = "DROP TABLE IF EXISTS weather"
        # cursor.execute(sql)
        # sql2 = "CREATE TABLE weather (\
        #     id INT AUTO_INCREMENT PRIMARY KEY,\
        #     name VARCHAR(255),\
        #     date VARCHAR(255),\
        #     avgTemp DOUBLE,\
        #     minTemp DOUBLE,\
        #     maxTemp DOUBLE,\
        #     sumRain DOUBLE\
        # );"
        # cursor.execute(sql2)

        # 데이터베이스에 데이터 삽입
        for record in data:
            query = "INSERT INTO weather(name, date, avgTemp, sumRain, avgWind) VALUES (%s, %s, %s, %s, %s)"
            values = (record['stnNm'], record['tm'], record['avgTa'], record['sumRn'], record['avgWs'])
            cursor.execute(query, values)

        # null 값을 0으로 치환
        null_change_query = "UPDATE weather SET sumRain = COALESCE(sumRain, 0)"
        cursor.execute(null_change_query)

        name_change_query = ("UPDATE weather SET name = CASE WHEN name = '청주' THEN '충북' WHEN name = '수원' THEN '경기' "
                             "WHEN name = '천안' THEN '충남' WHEN name = '전주' THEN '전북' WHEN name = '목포' THEN '전남' WHEN "
                             "name = '영천' THEN '경북' WHEN name = '창원' THEN '경남' WHEN name = '춘천' THEN '강원' ELSE name "
                             "END")
        cursor.execute(name_change_query)

        # 변경 사항 커밋
        db_connection.commit()

        # 연결 닫기
        cursor.close()
        db_connection.close()

        # 파일 삭제
        file_path = "data.json"

        try:
            os.remove(file_path)
            print(f"{file_path} has been successfully deleted.")
        except FileNotFoundError:
            print(f"{file_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
