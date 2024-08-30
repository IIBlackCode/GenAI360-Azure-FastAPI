import os
import openai
from langchain_openai import AzureOpenAI
from langchain_openai import OpenAI
from openai import AzureOpenAI

def gpt4omini(question):
    # 환경 변수 설정
    ENDPOINT = "https://kms-genai360-openai.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-15-preview"
    os.environ["AZURE_OPENAI_API_KEY"] = '6c19fcba60364d87af385b8517e13dff'
    os.environ["OPENAI_BASE"] = ENDPOINT  # 기본 URL
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://kms-genai360-openai.openai.azure.com/"  # 기본 URL
    os.environ["OPENAI_API_VERSION"] = '2024-07-18'  # API 버전

    # openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
    # openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    # openai.api_type = 'azure'
    # openai.api_version = '2024-07-18' # this might change in the future

    deployment_name='REPLACE_WITH_YOUR_DEPLOYMENT_NAME'

    # OpenAI 객체 초기화
    llm = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-07-18",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
    # deployment_name='gpt-4o-mini'  # 사용하는 모델 이름
    deployment_name='kms-genai360-openai'  # 사용하는 모델 이름

    try:
        # response = llm.invoke(question)
        response = llm.completions.create(model=deployment_name, prompt=question, max_tokens=10)
        # response = openai.Completion.create(engine=deployment_name, prompt=question, max_tokens=10)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    print(response)
    return response

# 예시 호출
# result = gpt4omini("What is the capital of France?")
# print(result)
