#API KEY 저장을 위한 os 라이브러리 호출
import os
from langchain_openai import OpenAI

global OPENAI_API_KEY

def chatgpt(question):
    #OPENAI API키 저장
    #API KEY 발급 페이지: https://platform.openai.com/docs/guides/gpt/completions-api
    os.environ["OPENAI_API_KEY"] = 'sk-bEG4v-N0uNWGuh7Is6rHiu9TVInF7ECw3dvkU60T7bT3BlbkFJu9g9S3iyqRBkw8J6hOG6K5Sei7AIQZKslb4KLsn_UA'
    llm = OpenAI()
    result = llm.invoke(question)
    return result

def apitest(question):
    global OPENAI_API_KEY

    try:
        print(OPENAI_API_KEY)
        llm = OpenAI()
        result = llm.invoke(question)
        return result
    except KeyError as e:
        # Handle cases where environment variable is not set
        return {"error": f"KeyError: {str(e)} - The API key was not set correctly."}
    
def apikey(key):
    global OPENAI_API_KEY
    print(key)
    try:
        # Set the API key
        OPENAI_API_KEY = key
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        # Initialize the OpenAI object
        llm = OpenAI()
        
        # Invoke the method
        llm.invoke("ready?")
        # Return the result if everything is successful
        return {"result": "승인"}
        
    except KeyError as e:
        # Handle cases where environment variable is not set
        return {"error": f"KeyError: {str(e)} - The API key was not set correctly."}
        
    # except Exception as e:
    #     # Handle any other exceptions
    #     return {"error": f"An error occurred: {str(e)}"}
