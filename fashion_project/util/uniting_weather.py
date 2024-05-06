import pandas as pd
from sqlalchemy import create_engine

# MySQL 연결 설정
try:
    # MySQL 연결 설정
    engine = create_engine('mysql+mysqlconnector://root:1234@localhost/capstone')

    # MySQL에서 날씨 데이터 가져오기
    query = "SELECT * FROM weather"
    weather_data = pd.read_sql_query(query, engine)

    # 데이터를 정상적으로 가져왔을 때만 이후의 작업 수행

    # 첫 번째 CSV 파일: 이미지 이름과 날짜
    image_date_df = pd.read_csv('../img.csv')

    # 두 DataFrame을 날짜를 기준으로 결합합니다.
    merged_df = pd.merge(image_date_df, weather_data, left_on='date', right_on='date', how='inner')

    # 'id' 및 'name' 열을 제거합니다.
    merged_df.drop(['id', 'name'], axis=1, inplace=True)

    # 결합된 DataFrame에서 NaN 값을 0으로 바꿉니다.
    merged_df.fillna(0, inplace=True)

    # 결과를 CSV 파일로 저장합니다.
    merged_df.to_csv('merged_file.csv', index=False)

except mysql.connector.Error as err:
    # MySQL 연결 오류 발생 시 오류 메시지 출력
    print("MySQL 연결 오류: {}".format(err))

finally:
    # 연결 종료
    if 'db_connection' in locals() and db_connection.is_connected():
        db_connection.close()
