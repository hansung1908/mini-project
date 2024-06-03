import csv, os, random

def get_random_image_and_date(gender, length, temp):
    image_folder = "static/img"  # 이미지가 있는 폴더 경로
    images = os.listdir(image_folder)  # 이미지 폴더 내의 모든 파일 목록

    matching_images = []
    if gender == '남자':
        matching_images = [image for image in images if '183_ki' in image or 'dailylooked' in image]
    elif gender == '여자':
        matching_images = [image for image in images if 'haveyun.ootd' in image or 'ouneul_look' in image]

    top_dict = {}
    bot_dict = {}
    with open('length.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            top_dict[row['imgpath']] = row['top']
            bot_dict[row['imgpath']] = row['bot']

    filtered_top_dict = {}
    if length == '반팔':
        filtered_top_dict = {img_path: top for img_path, top in top_dict.items() if top == '반팔'}
    elif length == '긴팔':
        filtered_top_dict = {img_path: top for img_path, top in top_dict.items() if top == '긴팔'}
    elif length == '패딩':
        filtered_top_dict = {img_path: top for img_path, top in top_dict.items() if top == '패딩'}

    filtered_images = []
    for img_path in matching_images:
        if img_path in filtered_top_dict:
            filtered_images.append(img_path)

    filtered_bot_dict = {img_path: bot for img_path, bot in bot_dict.items() if bot == '반바지'}

    if temp < 20:
        for img_path in filtered_images:
            if img_path in filtered_bot_dict:
                filtered_images.remove(img_path)

    random_images = random.sample(filtered_images, 3) # 중복되지 않는 랜덤한 3장의 이미지 선택

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