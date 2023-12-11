import easyocr
import cv2
import matplotlib.pyplot as plt
import difflib

THRESHOLD = 0.5

correct_words = ['서울', '경기', '충남', '충북', '전북', '전남', '경북', '경남', '제주', '부산', '대구', '인천', '대전']

reader = easyocr.Reader(['ko', 'en'])

def read(img_path):
    img = cv2.imread(img_path)

    result = reader.readtext(img_path)

    r = []

    for bbox, text, conf in result:
        if conf > THRESHOLD:
            r.append(text)
            cv2.rectangle(img, pt1=(int(bbox[0][0]), int(bbox[0][1])), pt2=(int(bbox[2][0]), int(bbox[2][1])), color=(0, 255, 0), thickness=3)

    if len(r[0]) > 4:
        r[0] = r[0].lstrip('0')
        r[0] = r[0].rstrip('0')
    print(r)

    plt.figure(figsize=(8, 8))
    plt.imshow(img[:, :, ::-1])
    plt.axis('off')
    plt.show()

read('picture/5.jpg')
