import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

plt.style.use('dark_background')

# 이미지 읽어오기
img_ori = cv2.imread('license_picture\ROK_Construction_Equipment_Registration_Plate_for_Private_Fork_Lift_Truck_-_Jeonnam.jpg')

# 높이, 너비, 채널
height, width, channel = img_ori.shape

plt.figure(figsize=(12, 10))
plt.imshow(img_ori,cmap='gray')
print(height, width, channel)   #1

# 흑백이미지 변환
gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
plt.figure(figsize=(12,10))
plt.imshow(gray, cmap='gray')   #2

# 가우시안 블러 : 노이즈 감소
img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)

# 쓰레시홀딩 : 계단 함수(흑색, 백색으로 나눔)
img_blur_thresh = cv2.adaptiveThreshold(
    img_blurred,
    maxValue=255.0,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY_INV,
    blockSize=19,
    C=9
)

img_thresh = cv2.adaptiveThreshold(
    gray,
    maxValue=255.0,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY_INV,
    blockSize=19,
    C=9
)

plt.figure(figsize=(20,20))
plt.subplot(1,2,1)
plt.title('Threshold only')
plt.imshow(img_thresh, cmap='gray')    #3
plt.subplot(1,2,2)
plt.title('Blur and Threshold')
plt.imshow(img_blur_thresh, cmap='gray')    #4


# 컨투어(윤곽선) 찾기
contours, _ = cv2.findContours(
    img_blur_thresh,
    mode=cv2.RETR_LIST,
    method=cv2.CHAIN_APPROX_SIMPLE
)

temp_result = np.zeros((height, width, channel), dtype=np.uint8)

# 컨투어 그리기, contourIdx가 -1이면 윤곽선 모두 그리기
cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255,255,255))

plt.figure(figsize=(12, 10))
plt.imshow(temp_result) #4

# 데이터 비교
temp_result = np.zeros((height, width, channel), dtype=np.uint8)

contours_dict = []

for contour in contours:
    # 컨투어의 사각형 범위 찾기
    x, y, w, h = cv2.boundingRect(contour)
    # 컨투어 사각형 그리기
    cv2.rectangle(temp_result, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255), thickness=2)

    # 컨투어 정보 저장
    contours_dict.append({
        'contour': contour,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'cx': x + (w / 2), # 중심 좌표
        'cy': y + (h / 2)
    })

plt.figure(figsize=(12, 10))
plt.imshow(temp_result, cmap='gray')

# 번호판 내용 컨투어 추리기
MIN_AREA = 80
MIN_WIDTH, MIN_HEIGHT = 2, 8
MIN_RATIO, MAX_RATIO = 0.25, 1.0 # 비율

possible_contours = []

cnt = 0
for d in contours_dict:
    area = d['w'] * d['h'] # 넓이
    ratio = d['w'] / d['h'] # 비율

    # 기준에 해당하는 컨투어 저장
    if area > MIN_AREA \
            and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
            and MIN_RATIO < ratio < MAX_RATIO:
        d['idx'] = cnt # 인덱스 연산을 위해 저장
        cnt += 1
        possible_contours.append(d)

temp_result = np.zeros((height, width, channel), dtype=np.uint8)

for d in possible_contours:
    cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(255, 255, 255),
                  thickness=2)

plt.figure(figsize=(12, 10))
plt.imshow(temp_result, cmap='gray')

# 위치의 배열을 보고 번호판 찾기
MAX_DIAG_MULTIPLYER = 5 # 컨투어 중심간의 길이가 첫 컨투어의 대각선 길이의 5배 이내
MAX_ANGLE_DIFF = 12 # 두 컨투어를 연결했을 댸 최대 각도
MAX_AREA_DIFF = 0.5 # 두 컨투어의 최대 면적 차이
MAX_WIDTH_DIFF = 0.8 # 두 컨투어의 최대 너비 차이
MAX_HEIGHT_DIFF = 0.2 # 두 컨투어의 최대 높이 차이
MIN_N_MATCHED = 3 # 위 조건에 만족하는 컨투어가 서로 붙어 있어야 하는 최소 갯수

# 재귀 함수
def find_chars(contour_list):
    # 최종 인덱스 값을 저장
    matched_result_idx = []

    for d1 in contour_list:
        matched_contours_idx = []
        for d2 in contour_list:
            if d1['idx'] == d2['idx']:
                continue
            
            # 두 컨투어 사이의 거리를 구하기 위한 중심점을 기준으로 한 가로, 세로 길이
            dx = abs(d1['cx'] - d2['cx'])
            dy = abs(d1['cy'] - d2['cy'])

            diagonal_length1 = np.sqrt(d1['w'] ** 2 + d1['h'] ** 2)

            # 두 컨투어 사이의 거리 측정
            distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))

            # 두 컨투어 사아의 각도 측정
            if dx == 0: # 컨투어의 x 좌표가 차이가 없으면 90도로 지정하여 예외 처리
                angle_diff = 90
            else:
                angle_diff = np.degrees(np.arctan(dy / dx))
            
            # 면적, 너비, 높이 비율 측정
            area_diff = abs(d1['w'] * d1['h'] - d2['w'] * d2['h']) / (d1['w'] * d1['h'])
            width_diff = abs(d1['w'] - d2['w']) / d1['w']
            height_diff = abs(d1['h'] - d2['h']) / d1['h']

            # 해당 기준에 맞는 컨투어 인덱스를 저장
            if distance < diagonal_length1 * MAX_DIAG_MULTIPLYER \
                    and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
                    and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                matched_contours_idx.append(d2['idx'])

        # 첫 컨투어의 인덱스도 저장
        matched_contours_idx.append(d1['idx'])

        # 연속된 컨투어 수가 기준보다 낮으면 제외
        if len(matched_contours_idx) < MIN_N_MATCHED:
            continue
        
        # 최종 후보군 저장
        matched_result_idx.append(matched_contours_idx)

        # 최종 후보군에서 탈락한 컨투어 저장
        unmatched_contour_idx = []
        for d4 in contour_list:
            if d4['idx'] not in matched_contours_idx:
                unmatched_contour_idx.append(d4['idx'])

        unmatched_contour = np.take(possible_contours, unmatched_contour_idx)

        # 재귀 함수를 통해 다시 비교
        recursive_contour_list = find_chars(unmatched_contour)

        # 최종 결과물을 저장
        for idx in recursive_contour_list:
            matched_result_idx.append(idx)

        break
    
    return matched_result_idx

# 함수 호출을 통해 번호판일거 같은 최종 결과물 저장
result_idx = find_chars(possible_contours)

matched_result = []
for idx_list in result_idx:
    matched_result.append(np.take(possible_contours, idx_list))

temp_result = np.zeros((height, width, channel), dtype=np.uint8)

for r in matched_result:
    for d in r:
        cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(255, 255, 255),
                      thickness=2)

plt.figure(figsize=(12, 10))
plt.imshow(temp_result, cmap='gray')

#번호판 이미지 정렬
PLATE_WIDTH_PADDING = 1.3  # 1.3
PLATE_HEIGHT_PADDING = 1.5  # 1.5
MIN_PLATE_RATIO = 3
MAX_PLATE_RATIO = 10

plate_imgs = []
plate_infos = []

for i, matched_chars in enumerate(matched_result):
    # x방향을 기준으로 정령
    sorted_chars = sorted(matched_chars, key=lambda x: x['cx'])

    # 정렬된 기준 x, y 저장
    plate_cx = (sorted_chars[0]['cx'] + sorted_chars[-1]['cx']) / 2
    plate_cy = (sorted_chars[0]['cy'] + sorted_chars[-1]['cy']) / 2

    # 정렬된 기준 너비 저장
    plate_width = (sorted_chars[-1]['x'] + sorted_chars[-1]['w'] - sorted_chars[0]['x']) * PLATE_WIDTH_PADDING

    sum_height = 0
    for d in sorted_chars:
        sum_height += d['h']

    # 정렬된 기준 높이 저장
    plate_height = int(sum_height / len(sorted_chars) * PLATE_HEIGHT_PADDING)

    # 기울어진 번호판의 각도 구하기
    # 삼각형의 높이
    triangle_height = sorted_chars[-1]['cy'] - sorted_chars[0]['cy']
    # 삼각형의 빗변
    triangle_hypotenus = np.linalg.norm(
        np.array([sorted_chars[0]['cx'], sorted_chars[0]['cy']]) -
        np.array([sorted_chars[-1]['cx'], sorted_chars[-1]['cy']])
    )

    angle = np.degrees(np.arcsin(triangle_height / triangle_hypotenus))

    # 로테이션 매트릭스 구하기
    rotation_matrix = cv2.getRotationMatrix2D(center=(plate_cx, plate_cy), angle=angle, scale=1.0)

    # 구한 매트릭스를 통해 이미지를 똑바로 정렬
    img_rotated = cv2.warpAffine(img_thresh, M=rotation_matrix, dsize=(width, height))

    # 구한 이미지를 자르기
    img_cropped = cv2.getRectSubPix(
        img_rotated,
        patchSize=(int(plate_width), int(plate_height)),
        center=(int(plate_cx), int(plate_cy))
    )

    if img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO or img_cropped.shape[1] / img_cropped.shape[
        0] < MIN_PLATE_RATIO > MAX_PLATE_RATIO:
        continue

    plate_imgs.append(img_cropped)
    plate_infos.append({
        'x': int(plate_cx - plate_width / 2),
        'y': int(plate_cy - plate_height / 2),
        'w': int(plate_width),
        'h': int(plate_height)
    })

    plt.subplot(len(matched_result), 1, i + 1)
    plt.imshow(img_cropped, cmap='gray')

# 이미지에서 컨투어 찾기
longest_idx, longest_text = -1, 0
plate_chars = []

for i, plate_img in enumerate(plate_imgs):
    plate_img = cv2.resize(plate_img, dsize=(0, 0), fx=1.6, fy=1.6)
    _, plate_img = cv2.threshold(plate_img, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 컨투어 한번 더 찾기
    contours, _ = cv2.findContours(plate_img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)

    plate_min_x, plate_min_y = plate_img.shape[1], plate_img.shape[0]
    plate_max_x, plate_max_y = 0, 0

    # 기준에 맞는지 한번 더 체크
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        area = w * h
        ratio = w / h

        if area > MIN_AREA \
                and w > MIN_WIDTH and h > MIN_HEIGHT \
                and MIN_RATIO < ratio < MAX_RATIO:
            if x < plate_min_x:
                plate_min_x = x
            if y < plate_min_y:
                plate_min_y = y
            if x + w > plate_max_x:
                plate_max_x = x + w
            if y + h > plate_max_y:
                plate_max_y = y + h

    # pytesseract 사용해서 글자 인식
    img_result = plate_img[plate_min_y:plate_max_y, plate_min_x:plate_max_x]

    # 이미지 전처리, 검정색 여백을 주어 인식을 더 원활하게 함
    img_result = cv2.GaussianBlur(img_result, ksize=(3, 3), sigmaX=0)
    _, img_result = cv2.threshold(img_result, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_result = cv2.copyMakeBorder(img_result, top=10, bottom=10, left=10, right=10, borderType=cv2.BORDER_CONSTANT,
                                    value=(0, 0, 0))

    # 파이테서렉트를 이용해 한글 인식
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    chars = pytesseract.image_to_string(img_result, lang='kor', config='--psm 7 --oem 0')

    # 한글과 숫자만 걸러냄
    result_chars = ''
    has_digit = False
    for c in chars:
        if ord('가') <= ord(c) <= ord('힣') or c.isdigit():
            if c.isdigit():
                has_digit = True
            result_chars += c

    print(result_chars)
    plate_chars.append(result_chars)

    # 구한 애들 중 가장 문자열이 긴 번호판을 저장
    if has_digit and len(result_chars) > longest_text:
        longest_text = len(result_chars)
        longest_idx = i

    plt.subplot(len(plate_imgs), 1, i + 1)
    plt.imshow(img_result, cmap='gray')

# 결과 출력
info = plate_infos[longest_idx]
chars = plate_chars[longest_idx]

print(chars)

img_out = img_ori.copy()

cv2.rectangle(img_out, pt1=(info['x'], info['y']), pt2=(info['x']+info['w'], info['y']+info['h']), color=(255,0,0), thickness=2)

# cv2.imwrite(chars + '.jpg', img_out)

plt.figure(figsize=(12, 10))
plt.imshow(img_out)

plt.show()