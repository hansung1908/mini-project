import easyocr
import cv2
import matplotlib.pyplot as plt
import difflib

THRESHOLD = 0.5

reader = easyocr.Reader(['ko'])

def read(img_path):
    img = cv2.imread(img_path)

    result = reader.readtext(img_path)

    r = []

    # 인식된 내용 표시
    for bbox, text, conf in result:
        if conf > THRESHOLD:
            r.append(text)
            cv2.rectangle(img, pt1=(int(bbox[0][0]), int(bbox[0][1])), pt2=(int(bbox[2][0]), int(bbox[2][1])), color=(0, 255, 0), thickness=3)

    # 인식시 번호판 고정을 위해 박아둔 너트(0)도 함께 인식할 경우 그 부분만 삭제
    if len(r[0]) > 4:
        r[0] = r[0].lstrip('0')
        r[0] = r[0].rstrip('0')

    # 아래 번호 인식시 한글과 숫자 크기로 인한 분할 인식할 경우 두 인식값을 병합
    if len(r) > 2:
        r[1] = r[1] + r[2]
        r.pop(2)

    # '북'이나 '울'이 글씨체로 '묵', '목', '물'로 인식할 경우 올바르게 변경
    korean_part = ''.join(char for char in r[0] if char.isalpha())  # 한글만 추출
    number_part = ''.join(char for char in r[0] if char.isdigit())  # 숫자만 추출
    if korean_part == '서물' or korean_part == '서몰':
        korean_part = '서울'
        r[0] = korean_part + number_part
    elif korean_part == '전묵' or korean_part == '전목':
        korean_part = '전북'
        r[0] = korean_part + number_part
    elif korean_part == '경묵' or korean_part == '경목':
        korean_part = '경북'
        r[0] = korean_part + number_part
    elif korean_part == '충묵' or korean_part == '충목':
        korean_part = '충북'
        r[0] = korean_part + number_part

    print(r)

    plt.figure(figsize=(8, 8))
    plt.imshow(img[:, :, ::-1])
    plt.axis('off')
    plt.show()

read('picture/5.jpg')
