import csv, os, random

def get_random_image_and_date(gender, length, temp):
    image_folder = "static/img"  # 이미지가 있는 폴더 경로
    images = os.listdir(image_folder)  # 이미지 폴더 내의 모든 파일 목록
    print(images)

    if(gender == '남자'):
        matching_images = [image for image in images if '183_ki' in image or 'dailylooked' in image]
    else:
        matching_images = [image for image in images if 'haveyun.ootd' in image or 'ouneul_look' in image]

    random_images = random.sample(matching_images, 3) # 중복되지 않는 랜덤한 3장의 이미지 선택

    dates_list = []
    with open('length.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for random_image in random_images:
            imgpath = 'img/' + random_image
            date = next((row['date'] for row in reader if row['imgpath'] == imgpath), None)
            dates_list.append(date)
            file.seek(0)  # 파일을 다시 처음으로 돌려줍니다.

    images_list = []
    for random_image in random_images:
        fix_image = random_image.rsplit('_', 1)[0]
        images_list.append(fix_image)

    image_date = [(image, date) for image, date in zip(images_list, dates_list)]
    print(image_date)

    return random_images, image_date

