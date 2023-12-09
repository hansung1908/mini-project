import subprocess
import os
from gensim.summarization.summarizer import summarize
import urllib3
import base64
import json
import tkinter as tk
from tkinter import scrolledtext

def youtube_summary():
    # 재입력시 내용 초기화
    output1.delete(1.0, tk.END)
    output2.delete(1.0, tk.END)

    # 유튜브 url을 통해 영상 추출
    youtube_url = entry.get()
    subprocess.call(["yt-dlp", "-o", "%(title)s.%(ext)s", youtube_url.split("=")[-1]])

    # mp4 파일 중 첫번째 파일만 임의로 선택
    filelist = [file for file in os.listdir(".") if file.endswith((".webm", ".mp4", ".mkv"))]
    if not filelist:
        output1.insert(tk.END, "유효하지 않는 유튜브 url입니다.")
    file = filelist[0]


    # audio 추출
    # -y : 이미 존재하는 파일의 경우, overwriting할 수 있도록 설정
    subprocess.call(["ffmpeg", "-y", "-i", file, "output.mp3"])

    # mp3 -> wav 변경
    # -y : 이미 존재하는 파일의 경우, overwriting할 수 있도록 설정
    # -ar : sampling rate (etri의 경우 16khz지원)
    # -ac : 1 (mono)
    subprocess.call(["ffmpeg", "-y", "-i", "output.mp3", "-ac", "1", "-ar", "16000", "output.wav"])

    # 30초씩 오디오 자르기
    subprocess.call(["ffmpeg", "-i",
                     "output.wav",
                     "-f", "segment", "-segment_time", "30",
                     "-c", "copy", "output%09d.wav"])

    # stt_api url, key
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    accessKey = "9c5e9610-0fce-4eba-acdb-5e060bbf782b"

    # audio 파일을 text로 변환
    def etri_stt(audioFilePath):
        languageCode = "korean"

        file = open(audioFilePath, "rb")
        audioContents = base64.b64encode(file.read()).decode("utf8")
        file.close()

        requestJson = {
            "access_key": accessKey,
            "argument": {
                "language_code": languageCode,
                "audio": audioContents
            }
        }

        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
            body=json.dumps(requestJson)
        )

        print("[responseCode] " + str(response.status))
        print("[responBody]")
        print("===== 결과 확인 ====")
        data = json.loads(response.data.decode("utf-8", errors='ignore'))
        print(data['return_object']['recognized'])

        return data['return_object']['recognized']

    # 전체 텍스트 출력
    filelist = [file for file in os.listdir(".") if file.startswith("output00")]

    text_stacked = ""
    for file in filelist:
        print(file)
        text = etri_stt(file)
        text_stacked += text

    print(text_stacked)
    output1.insert(tk.END, text_stacked)

    # 요약본 출력
    punctuation_text = text_stacked.replace("니다", "니다.") #습니다. 입니다.
    summarize_text = summarize(punctuation_text, word_count=50)

    print()
    print()
    print(summarize_text)
    output2.insert(tk.END, summarize_text)

# 메인 윈도우 생성
root = tk.Tk()
root.title("유튜브 영상 요약하기")

# 라벨 및 엔트리 위젯 추가
label = tk.Label(root, text="URL 입력:")
label.pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# 버튼 추가
button = tk.Button(root, text="텍스트 가져오기", command=youtube_summary)
button.pack(pady=10)

# 출력을 위한 스크롤 텍스트 위젯 추가
# 전체 내용 텍스트
summary_label1 = tk.Label(text="전체 내용")
summary_label1.pack()
output1 = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
output1.pack(padx=10, pady=10)

# 요약본 텍스트
summary_label2 = tk.Label(text="요약본")
summary_label2.pack()
output2 = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)
output2.pack(padx=10, pady=10)

# GUI 실행
root.mainloop()