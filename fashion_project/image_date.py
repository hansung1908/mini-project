import csv, os, random

def get_random_image_and_date(gender, length, temp):
    # 이미지가 있는 폴더 경로
    image_folder = "static/img"

    # 이미지 폴더 내의 모든 파일 목록
    images = os.listdir(image_folder)

    # 성별에 따라 같은 성별의 인플루언서가 담긴 이미지 목록 생성
    matching_images = []
    if gender == '남자':
        matching_images = [image for image in images if '183_ki' in image or 'dailylooked' in image]
    elif gender == '여자':
        matching_images = [image for image in images if 'haveyun.ootd' in image or 'ouneul_look' in image]

    # length.csv로부터 상의, 하의 목록 가져오기
    top_dict = {}
    bot_dict = {}
    with open('length.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            top_dict[row['imgpath']] = row['top']
            bot_dict[row['imgpath']] = row['bot']

    # 상의 종류에 따라 이미지 목록 생성
    filtered_top_dict = {}
    if length == '반팔':
        filtered_top_dict = {img_path: top for img_path, top in top_dict.items() if top == '반팔'}
    elif length == '긴팔':
        filtered_top_dict = {img_path: top for img_path, top in top_dict.items() if top == '긴팔'}
    elif length == '패딩':
        filtered_top_dict = {img_path: top for img_path, top in top_dict.items() if top == '패딩'}

    # 성별로 분류한 이미지 목록에서 상의 종류로 한차례 더 분류한 이미지 목록 생성
    filtered_images = []
    for img_path in matching_images:
        if img_path in filtered_top_dict:
            filtered_images.append(img_path)

    # 하의가 반바지인 이미지 목록 생성
    filtered_bot_dict = {img_path: bot for img_path, bot in bot_dict.items() if bot == '반바지'}

    # 온도가 20도 미만일때는 이미지 목록에서 반바지 제외
    if temp < 20:
        for img_path in filtered_images:
            if img_path in filtered_bot_dict:
                filtered_images.remove(img_path)

    # 중복되지 않는 랜덤한 3장의 이미지 선택
    random_images = random.sample(filtered_images, 3)

    # CSV 파일을 읽어서 이미지 경로와 날짜를 딕셔너리에 저장
    date_dict = {}
    with open('length.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date_dict[row['imgpath']] = row['date']

    # random_images 리스트에 있는 각 이미지 경로에 해당하는 날짜를 dates_list에 저장
    dates_list = [date_dict.get(random_image) for random_image in random_images]

    images_list = []
    for random_image in random_images:
        fix_image = random_image.rsplit('_', 1)[0]
        images_list.append(fix_image)

    image_date = [(image, date) for image, date in zip(images_list, dates_list)]

    return random_images, image_date