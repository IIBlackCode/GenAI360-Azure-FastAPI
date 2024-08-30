#API KEY 저장을 위한 os 라이브러리 호출
import os
from langchain_openai import OpenAI


def chatgpt(question):
    #OPENAI API키 저장
    #API KEY 발급 페이지: https://platform.openai.com/docs/guides/gpt/completions-api
    os.environ["OPENAI_API_KEY"] = 'sk-bEG4v-N0uNWGuh7Is6rHiu9TVInF7ECw3dvkU60T7bT3BlbkFJu9g9S3iyqRBkw8J6hOG6K5Sei7AIQZKslb4KLsn_UA'
    llm = OpenAI()
    result = llm.invoke(question)
    return result

# def test2(question):
#     llm = OpenAI()
#     result = llm.invoke(question)
#     return result