import openai

openai.api_key = 'YOUR_API_KEY'

def summarize_text_gpt3(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{text}\n\nSummarize:",
        temperature=0.3,
        max_tokens=100
    )
    return response.choices[0].text.strip()

text = "여기에 요약하고자 하는 텍스트를 넣으세요."
print("Summary: ", summarize_text_gpt3(text)