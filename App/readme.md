# GenAI360 Azure향 개발지원 위한 FastAPI
## 파일 구성
```shell
App/
├── main.py
├── routers/
│   ├── __init__.py
│   ├── user.py
│   ├── item.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── item.py
├── templates/
│   ├── base.html
│   ├── index.html
└── static/
    ├── css/
    ├── js/
```

## FastAPI Project 구성 과정
1. fastAPI 설치
```shell
pip install fastapi
```
2. Svelte 설치하기
```shell
# 설치 명령어
npm create vite@latest frontend -- --template svelte

# frontend디렉토리 이동 후 Svelte 서버 실행
npm run dev
```

3. uvicorn 설치하기
```shell
# 설치 명령어
pip install "uvicorn[standard]"

# App디렉토리 이동 후 FastAPi 서버 실행
uvicorn main:app --reload
```

4. 화면구동을 위한 Jinja템플릿엔진 설치
```shell
pip install jinja2
```

5. LLM 실습을 위한 라이브러리 설치
```shell
pip install langchain
pip install openai
pip install langchain-openai
```

6. Azure
```shell
pip install azure
pip install azure-ai-openai
pip install azure-storage-blob 
# pip install python-dotenv
pip install azure-identity 

```

7. 파일업로드
```shell
pip install python-multipart
```

8. 

## FastAPI 실행
```shell
# Dev
uvicorn main:app --reload
```

* 추가사항(Azure OpenAI)
- 모델을 선택하는 기능 추가
    - GPT4o                 : 높은 지능이 필요한 경우 선택
    - GPT4oMini             : 개발진행
    - AI Search(Vector DB)  : 연동 및 개발, 질문 대비를 위한 세부옵션 스터디
    - FastAPI with Azure blob Storage 연동 및 개발

- Embedding model
    - small
    - large

# FastAPI 배포
## 1. python 설치
```shell
sudo apt-get update
sudo apt-get install python3.12
sudo apt-get install python3-venv

# python 버전 확인
python3 --version
Python 3.8.10
```

```shell
```

```shell
```

```shell
```

```shell
```