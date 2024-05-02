import mysql.connector


def get(date, location):
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='capstone'
    )

    # 커서 생성
    cursor = db_connection.cursor()

    # 가져와
    query = "SELECT * FROM weather WHERE date = %s AND name = %s"
    cursor.execute(query, (date, location))

    # 결과 가져오기
    data = cursor.fetchall()

    # 변경 사항 커밋
    db_connection.commit()

    # 연결 닫기
    cursor.close()
    db_connection.close()

    # 튜플에서 마지막 세 개의 값을 추출합니다.
    _, _, _, temperature, precipitation, wind_speed = data[0]

    # 딕셔너리를 생성합니다.
    result = {'기온': temperature, '강수량': precipitation, '풍속': wind_speed}

    return result
