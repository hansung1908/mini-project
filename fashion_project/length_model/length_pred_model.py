import pandas as pd
import numpy as np
import tensorflow as tf

def play(avg_temp):
    # 모델 불러오기
    model = tf.keras.models.load_model('length_model/length_pretrain_model.h5')

    # 모델 요약 정보 출력
    print("모델 요약 정보:")
    model.summary()

    # 변수
    print(avg_temp)
    min_temp = avg_temp - 10
    max_temp = avg_temp + 10

    df = pd.DataFrame(columns=['avgTemp', 'min_temp', 'max_temp'])
    df.loc[0] = [avg_temp, min_temp, max_temp]

    # 예측
    pred = model.predict(df)
    max_index = np.argmax(pred[0])

    length_dict = {0: '반팔', 1: '긴팔', 2: '패딩'}
    result_tag = length_dict[max_index]

    # 결과 보여주기
    print(f'스타일: {result_tag}')
    print(f'확률: {pred[0][max_index] * 100:.4f}%')

    return result_tag