import json
import pandas as pd
import numpy as np
import tensorflow as tf


def ai(avgTemp, sumRain):
    # 모델 불러오기
    model = tf.keras.models.load_model('demo/model_demo.h5')

    # 변수
    print(avgTemp, sumRain)
    # avgTemp = 10.4
    minTemp = 3.8
    maxTemp = 15.2
    # sumRain = 5.4

    df = pd.DataFrame(columns=['avgTemp', 'minTemp', 'maxTemp', 'sumRain'])
    df.loc[0] = [avgTemp, minTemp, maxTemp, sumRain]

    # 예측
    pred = model.predict(df)
    max_index = np.argmax(pred[0])

    # 클래스 불러오기
    cat_json = json.load(open('demo/category_demo.json', 'r'))
    convert_cat_dict = {v: k for k, v in cat_json.items()}

    result_tag = convert_cat_dict[max_index]

    # 결과 보여주기
    print(f'스타일: {result_tag}')
    print(f'확률: {pred[0][max_index] * 100:.4f}%')

    return result_tag
