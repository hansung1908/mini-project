import json
import pandas as pd
import numpy as np
import tensorflow as tf

def play(avg_temp, sum_rain):
    # 모델 불러오기
    model = tf.keras.models.load_model('style_model/style_pretrain_model.h5')

    # 모델 요약 정보 출력
    print("모델 요약 정보:")
    model.summary()

    # 변수
    print(avg_temp, sum_rain)
    min_temp = avg_temp - 10
    max_temp = avg_temp + 10

    df = pd.DataFrame(columns=['avgTemp', 'min_temp', 'max_temp', 'sum_rain'])
    df.loc[0] = [avg_temp, min_temp, max_temp, sum_rain]

    # 예측
    pred = model.predict(df)
    max_index = np.argmax(pred[0])

    # 클래스 불러오기
    cat_json = json.load(open('style_model/style_category.json', 'r'))
    convert_cat_dict = {v: k for k, v in cat_json.items()}
    print(convert_cat_dict)

    result_tag = convert_cat_dict[max_index]

    # 결과 보여주기
    print(f'스타일: {result_tag}')
    print(f'확률: {pred[0][max_index] * 100:.4f}%')

    return result_tag
