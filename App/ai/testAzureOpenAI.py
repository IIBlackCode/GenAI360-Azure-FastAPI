import openai

# Azure OpenAI API 버전 설정
api_version = "2024-07-18"

# API Key를 환경 변수에서 가져옵니다.
api_key = 'd800d93e9142483e8bf232565ca15147'  # 실제 API 키로 교체

# OpenAI 클라이언트 초기화
client = openai.AzureOpenAI(
    api_key="d800d93e9142483e8bf232565ca15147",
    api_version="2024-07-18",
    azure_endpoint="https://kms-genai360-openai.openai.azure.com",
    azure_deployment="kms-genai360-openai"  # 실제 배포 이름으로 교체
)

# 채팅 생성 요청
try:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # 모델 이름
        messages=[
            {
                "role": "user",
                "content": "How do I output all files in a directory using Python?",
            },
        ],
    )
    print(completion.choices[0].message['content'])
except Exception as e:
    print(f"An error occurred: {e}")

# 배포 클라이언트 초기화
deployment_client = openai.AzureOpenAI(
    api_key='d800d93e9142483e8bf232565ca15147',
    api_version=api_version,
    azure_endpoint="https://kms-genai360-openai.openai.azure.com/",
    azure_deployment="kms-genai360-openai"  # 실제 배포 이름으로 교체
)

# 채팅 생성 요청
try:
    completion = deployment_client.chat.completions.create(
        model="gpt-4o-mini",  # 모델 이름
        messages=[
            {
                "role": "user",
                "content": "How do I output all files in a directory using Python?",
            },
        ],
    )
    print(completion.choices[0].message['content'])
except Exception as e:
    print(f"An error occurred: {e}")
