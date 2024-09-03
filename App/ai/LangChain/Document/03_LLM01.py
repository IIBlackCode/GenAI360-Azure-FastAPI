#API KEY 저장을 위한 os 라이브러리 호출
import os

#OPENAI API키 저장
#API KEY 발급 페이지: https://platform.openai.com/docs/guides/gpt/completions-api
os.environ["OPENAI_API_KEY"] = 'sk-bEG4v-N0uNWGuh7Is6rHiu9TVInF7ECw3dvkU60T7bT3BlbkFJu9g9S3iyqRBkw8J6hOG6K5Sei7AIQZKslb4KLsn_UA'

# (1) API를 통해 GPT-3, ChatGPT와 대화해보기
# 1.   항목 추가
# 2.   항목 추가

from langchain_openai import OpenAI
def llm01():
    llm = OpenAI()
    result = llm.invoke('왜 파이썬이 가장 인기있는 프로그래밍 언어야?')
    print(result)

def llm02():
    llm = OpenAI()
    llm = OpenAI(model_name = 'gpt-3.5-turbo-instruct', max_tokens = -1)
    result = llm.invoke('왜 파이썬이 가장 인기있는 프로그래밍 언어야?')
    print(result)

from langchain_openai import ChatOpenAI
def llm03():
    chatgpt = ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens = 512)
    answer = chatgpt.invoke("왜 파이썬이 가장 인기있는 프로그래밍 언어야?")
    print(answer.content)

from langchain_openai import OpenAI
def llm05():
    llm = OpenAI()
    llm = OpenAI(model_name = 'gpt-3.5-turbo-instruct', max_tokens = -1)
    result = llm.invoke('왜 파이썬이 가장 인기있는 프로그래밍 언어야?')
    print(result)

from langchain_openai import ChatOpenAI
def llm06():
    chatgpt = ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens = 512)
    answer = chatgpt.invoke("왜 파이썬이 가장 인기있는 프로그래밍 언어야?")
    print(answer.content)

# (2) 매개변수 조절해보기
# 1. Temperature의 의미 
def llm04():
    # temperature : 답변의 일관성을 조절하는 변수(0~2)
    # 0 : 답변이 일관적(신뢰성이 중요할때)
    # 2 : 답변이 랜덤함(창의성이 중요할때)
    chatgpt_temp0_1 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature = 0, max_tokens = 512)
    chatgpt_temp0_2 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature = 0, max_tokens = 512)
    chatgpt_temp1_1 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature = 1, max_tokens = 512)
    chatgpt_temp1_2 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature = 1, max_tokens = 512)

    model_list = [chatgpt_temp0_1, chatgpt_temp0_2, chatgpt_temp1_1, chatgpt_temp1_2]

    for i in model_list:
        answer = i.invoke("왜 파이썬이 가장 인기있는 프로그래밍 언어야?", max_tokens = 128)
        print("-"*100)
        print(">>>",answer.content)

    for chunk in chatgpt.stream("왜 파이썬이 가장 인기있는 프로그래밍 언어야?"):
        print(chunk.content, end="", flush=True)

# 2. ChatGPT처럼 실시간 응답 출력이 가능하도록 해보기
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
def llm07():
    chatgpt = ChatOpenAI(model_name="gpt-3.5-turbo", streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature = 1)
    answer = chatgpt.predict("왜 파이썬이 가장 인기있는 프로그래밍 언어야?")
    for chunk in chatgpt.stream("왜 파이썬이 가장 인기있는 프로그래밍 언어야?"):
        print(chunk.content, end="", flush=True)

# ChatGPT에게 역할 부여하기

# ChatGPT API는 기본 OpenAI LLM들과 다른 Input 형식을 갖고 있습니다.
# ChatGPT는 대화에 특화된 LLM인만큼, 아래와 같은 2가지 독특한 매개변수를 지닙니다.
# (1) SystemMessage: ChatGPT에게 역할을 부여하여, 대화의 맥락을 설정하는 메세지
# (2) HumanMessage: 사용자가 ChatGPT에게 대화 또는 요청을 위해 보내는 메세지
# 위 두가지 형식을 적절히 활용하면, LLM을 더욱 효과적으로 사용할 수 있습니다.
def llm08():
    # from langchain.chat_models import ChatOpenAI # 구버전 
    # langchain.chat_models > langchain_openai
    from langchain_openai import ChatOpenAI
    from langchain.schema import AIMessage, HumanMessage, SystemMessage

    chatgpt = ChatOpenAI(model_name="gpt-3.5-turbo", temperature = 1)

    messages = [
        SystemMessage(
            content="your a helpful assistant that translates English to korean"
        ),
        HumanMessage(
            content="how to use langchain."
        ),
    ]
    response_langchain = chatgpt.invoke(messages)
    response_langchain.content

def llm09():
    # from langchain.chat_models import ChatOpenAI
    from langchain_openai import ChatOpenAI
    from langchain.schema import AIMessage, HumanMessage, SystemMessage

    chatgpt = ChatOpenAI(model_name="gpt-3.5-turbo", temperature = 1)

    messages = [
        SystemMessage(
            content="너는 20년차 시니어 개발자야. 사용자의 질문에 매우 건방지게 대답해줘."
        ),
        HumanMessage(
            content="파이썬의 장점에 대해서 설명해줘."
        ),
    ]
    response_langchain = chatgpt.invoke(messages)
    response_langchain.content

# (3) LLM 응답 캐싱하여 같은 질문에 더 빠르게 응답받기
def llm10():
    from langchain.globals import set_llm_cache
    from langchain_openai import OpenAI

    # To make the caching really obvious, lets use a slower model.
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct", n=2, best_of=2)

    %%time
    from langchain.cache import InMemoryCache

    set_llm_cache(InMemoryCache())

    # The first time, it is not yet in cache, so it should take longer
    llm.predict("Tell me a joke")
