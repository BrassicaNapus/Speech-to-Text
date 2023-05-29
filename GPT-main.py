import openai
import speech_recognition as sr
import re

# 음성 인식을 위한 객체 초기화
r = sr.Recognizer()
mic = sr.Microphone()

# OpenAI GPT-3 API 키 설정
openai.api_key = 'YOUR_API_KEY'

# 불필요한 말 리스트 정의
unnecessary_words = ["음", "그", "이제", "뭐냐", "어", "막", "진짜"]

# 불필요한 말 카운트 변수 초기화
unnecessary_words_count = 0


def preprocess_text(text):
    # 불필요한 말 카운트를 위해 전처리된 텍스트를 반환합니다.
    global unnecessary_words_count
    for word in unnecessary_words:
        count = text.count(word)
        unnecessary_words_count += count

    # 불용어 제거
    text = re.sub(r'\b\w{1,2}\b', '', text)  # 단어 길이가 1 또는 2인 단어를 제거합니다.
    text = ' '.join([word for word in text.split() if word.lower() not in unnecessary_words])

    return text


def summarize_text_gpt3(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{text}\n\nSummarize:",
        temperature=0.3,
        max_tokens=100
    )
    return response.choices[0].text.strip()


def start_recording():
    global unnecessary_words_count
    with mic as source:
        print("Recording started...")
        audio = r.listen(source, timeout=5, phrase_time_limit=30)  # 무음 시간 5초, 한 번에 녹음 가능한 시간은 30초로 설정합니다.
        try:
            text = r.recognize_google(audio, language='ko-KR')  # 녹음된 음성을 텍스트로 변환합니다.
            print("Original Transcribed Text: ", text)

            # 변환된 텍스트를 전처리하여 요약합니다.
            preprocessed_text = preprocess_text(text)
            summary = summarize_text_gpt3(preprocessed_text)
            print("Summary: ", summary)

            # 불필요한 말 카운트 출력
            print("Unnecessary Words Count: ", unnecessary_words_count)
        except Exception as e:
            print("Exception: ", str(e))  # 오류 발생 시 출력


# 프로그램이 실행되면 즉시 녹음을 시작합니다.
start_recording()
