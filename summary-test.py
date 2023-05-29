from summarizer import Summarizer
import re

# BERT 모델을 사용한 요약기 초기화
model = Summarizer()

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

def summarize_text(text):
    # 전처리된 텍스트를 요약합니다.
    preprocessed_text = preprocess_text(text)
    summary = model(preprocessed_text)
    return summary

text = "안녕하세요 저는 현재 세종대학교 전자정보통신공학과 4학년에 재학중인 유정하라고 합니다. 저는 내년 2월에 졸업할 예정입니다."
print("Summary: ", summarize_text(text))
