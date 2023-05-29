import threading
import keyboard
import speech_recognition as sr
from summarizer import Summarizer
from gtts import gTTS
import os
import playsound
import time
import re

# 음성 인식을 위한 객체 초기화
r = sr.Recognizer()
mic = sr.Microphone()

# BERT 모델을 사용한 요약기 초기화
model = Summarizer()

# 불필요한 말 리스트 정의
unnecessary_words = ["음", "그", "이제", "뭐냐", "어", "막", "허"]

# 종결어미 리스트 정의
endings = ["다", "요", "죠", "네", "의", "을", "를", "에", "와", "과", "로", "으로", "이", "가", "은", "는", "와", "과"]

def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def start_recording():
    sentence_count = 0
    end_blurry_count = 0
    unnecessary_word_count = 0

    filename = 'record.txt'
    if os.path.isfile(filename):
        os.remove(filename)

    speak("안녕하세요. 캡스톤 디자인 하면서 어떠셨는지 말씀해주세요. 2초 후에 말씀하시고, 종료시 s를 누르면 됩니다.")

    stop_recording = threading.Event()

    def check_keyboard_input():
        while True:
            if keyboard.is_pressed('s'):  # 's' 키가 눌리면
                stop_recording.set()  # 녹음 종료 이벤트 설정
                break
            time.sleep(0.1)

    # 키보드 입력 체크를 위한 별도의 스레드 생성 및 시작
    keyboard_thread = threading.Thread(target=check_keyboard_input)
    keyboard_thread.start()

    with mic as source:
        while True:
            if stop_recording.is_set():  # 's' 키가 눌렸는지 확인
                break

            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language='ko-KR')
                print("Transcribed Text: ", text)

                with open(filename, 'a') as f:
                    f.write("말한 내용: " + str(text) + "\n")

                sentence_count += 1
                time.sleep(0.1)

                # 불필요한 단어의 개수를 계산
                for word in unnecessary_words:
                    if word in text:
                        unnecessary_word_count += text.count(word)

                # 변환된 텍스트를 전처리하여 요약합니다.
                summary = model(text)
                print("Summary: ", summary)
                with open(filename, 'a') as f:
                    f.write("Summary: " + summary + "\n")

                # 문장의 종결어미가 명확한지 확인합니다.
                if not any(text.endswith(ending) for ending in endings):
                    print("평가: 문장의 종결이 불분명합니다.")
                    with open(filename, 'a') as f:
                        f.write("평가: 문장의 종결이 불분명합니다.\n")
                    end_blurry_count += 1

            except Exception as e:
                print("Exception: ", str(e))  # 오류 발생 시 출력

    keyboard_thread.join()  # 키보드 체크 스레드가 종료될 때까지 기다림

    stat_result = f"총 {sentence_count}문장 중, {end_blurry_count}문장의 종결이 불분명합니다. 또한, 불필요한 단어가 총 {unnecessary_word_count}번 나왔습니다."
    print(stat_result)
    with open(filename, 'a') as f:
        f.write("\n" + stat_result)

    print("평가 결과 저장 완료.")

start_recording()