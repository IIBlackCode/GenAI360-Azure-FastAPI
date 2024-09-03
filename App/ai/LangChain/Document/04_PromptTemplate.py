# !pip install -q openai langchain langchain-openai
# LangChain의 구조
## Prompt란 무엇인가?
# - "프롬프트"는 모델에 대한 입력을 의미. 이 입력은 하드 코딩되는 경우는 거의 없지만 여러 구성 요소로 구성되는 경우가 많음
# - "프롬프트 템플릿"은 이 입력의 구성을 담당. LangChain은 프롬프트를 쉽게 구성하고 작업할 수 있도록 여러 클래스와 함수를 제공

# pip install langchain
# pip install openai
# pip install langchain-openai

#API KEY 저장을 위한 os 라이브러리 호출
import os
#기본 LLM 로드를 위한 라이브러리 호출
from langchain.llms import OpenAI
#채팅 LLM 로드를 위한 라이브러리 호출
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI

# OPENAI API키 저장
os.environ["OPENAI_API_KEY"] = 'sk-bEG4v-N0uNWGuh7Is6rHiu9TVInF7ECw3dvkU60T7bT3BlbkFJu9g9S3iyqRBkw8J6hOG6K5Sei7AIQZKslb4KLsn_UA'

# Davinch-003 모델 설정하기(레거시모델 최신화 2024.09.02)
# text-davinci-003 > gpt-3.5-turbo-instruct
davinch3 = OpenAI(
    model_name="gpt-3.5-turbo-instruct",
    max_tokens = 1000
)

# (1)프롬프트 템플릿 맛보기
"""
프롬프트 템플릿은 크게 2가지가 존재합니다.
    1. Prompt Template : 일반적인 프롬프트 템플릿 생성시 활용
    2. Chat Prompt Template : 채팅 LLM에 프롬프트를 전달하는데 활용할 수 있는 특화 프롬프트 템플릿
"""

from langchain.prompts import PromptTemplate, ChatPromptTemplate
def promptTemplate01():

    #프롬프트 템플릿을 통해 매개변수 삽입 가능한 문자열로 변환
    string_prompt = PromptTemplate.from_template("tell me a joke about {subject}")

    #매개변수 삽입한 결과를 string_prompt_value에 할당
    string_prompt_value = string_prompt.format_prompt(subject="soccer")

    #채팅LLM이 아닌 LLM과 대화할 때 필요한 프롬프트 = string prompt
    string_prompt_value

    #to_string() 함수를 통해 prompt template으로 생성한 문장 raw_text 반환 가능
    print(string_prompt_value.to_string())

    chat_prompt = ChatPromptTemplate.from_template("tell me a joke about {subject}")
    chat_prompt_value = chat_prompt.format_prompt(subject="soccer")
    chat_prompt_value

    chat_prompt_value.to_string()

# (2) 프롬프트 템플릿 활용해보기
# 반복적인 프롬프트를 삽입해야하는 경우, Prompt Template를 통해 간편하게 LLM을 활용할 수 있습니다.
# - GPT-3와 프롬프트 템플릿을 활용하여 대화해보기
def promptTemplate02():
    template = """
    너는 요리사야. 내가 가진 재료들을 갖고 만들 수 있는 요리를 추천하고, 그 요리의 레시피를 제시해줘.
    내가 가진 재료는 아래와 같아.

    <재료>
    {재료}

    """
    prompt_template = PromptTemplate(
        input_variables = ['재료'],
        template = template
    )
    print(prompt_template.format(재료 = '양파, 계란, 사과, 빵'))

    # -  ChatGPT와 프롬프트 템플릿을 활용하여 대화해보기
    from langchain.prompts import (
        ChatPromptTemplate,
        PromptTemplate,
        SystemMessagePromptTemplate,
        AIMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )
    from langchain.schema import (
        AIMessage,
        HumanMessage,
        SystemMessage
    )

    # ChatGPT 모델을 로드합니다.
    chatgpt = ChatOpenAI(temperature=0)

    #ChatGPT에게 역할을 부여합니다.(위에서 정의한 Template 사용)
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    #사용자가 입력할 매개변수 template을 선언합니다.
    human_template = "{재료}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    #ChatPromptTemplate에 system message와 human message 템플릿을 삽입합니다.
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    #ChatGPT API에 ChatPromptTemplate을 입력할 때, human message의 매개변수인 '재료'를 할당하여 전달합니다.
    #이와 같은 방식을 통해 ChatGPT는 ChatPromptTemplate의 구성요소인 system message와 human message를 전달받아, 대답 생성에 활용합니다.
    answer = chatgpt(chat_prompt.format_prompt(재료="양파, 계란, 사과, 빵").to_messages())
    print(answer.content)

# (3) Few-shot 예제를 통한 프롬프트 템플릿
"""
Few-shot이란, 딥러닝 모델이 결과물을 출력할 때 예시 결과물을 제시함으로써 원하는 결과물로 유도하는 방법론입니다.
LLM 역시, Few-shot 예제를 제공하면 예제와 유사한 형태의 결과물을 출력합니다.
내가 원하는 결과물의 형태가 특수하거나, 구조화된 답변을 원할 경우, 결과물의 예시를 수 개 제시함으로써 결과물의 품질을 향상시킬 수 있습니다.
"""

from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
def promptTemplate03():
    examples = [
    {
        "question": "아이유로 삼행시 만들어줘",
        "answer":
        """
        아: 아이유는
        이: 이런 강의를 들을 이
        유: 유가 없다.
        """
    },
    {
        "question": "김민수로 삼행시 만들어줘",
        "answer":
        """
        김: 김치는 맛있다
        민: 민달팽이도 좋아하는 김치!
        수: 수억을 줘도 김치는 내꺼!
        """
    }
    ]

    example_prompt = PromptTemplate(input_variables=["question", "answer"], template="Question: {question}\n{answer}")
    print(example_prompt.format(**examples[0]))

    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix="Question: {input}",
        input_variables=["input"]
    )
    print(prompt.format(input="호날두로 삼행시 만들어줘"))

    # prompt Template 미적용
    print(davinch3.predict("호날두로 삼행시 만들어줘"))
    # prompt Template 적용
    print(davinch3(prompt.format(input="호날두로 삼행시 만들어줘")))

# (4) Example Selector를 이용한 동적 Few-shot 러닝
"""
Few-shot 예제를 동적으로 입력하고 싶은 경우, Example Selector를 활용할 수 있습니다.
LLM이 여러 작업을 수행하도록 만들되 내가 원하는 범위의 대답을 출력하도록 하려면 
사용자의 입력에 동적으로 반응해야 합니다.이와 동시에, 예제를 모두 학습시키는 것이 아니라 
적절한 예시만 포함하도록 함으로써 입력 prompt의 길이를 제한하고, 
이를 통해 오류가 발생하지 않도록 조절할 수 있습니다.
"""
def promptTemplate04():
    from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
    from langchain.vectorstores import Chroma
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.prompts import FewShotPromptTemplate, PromptTemplate

    example_prompt = PromptTemplate(
        input_variables=["input", "output"],
        template="Input: {input}\nOutput: {output}",
    )

    # These are a lot of examples of a pretend task of creating antonyms.
    examples = [
        {"input": "행복", "output": "슬픔"},
        {"input": "흥미", "output": "지루"},
        {"input": "불안", "output": "안정"},
        {"input": "긴 기차", "output": "짧은 기차"},
        {"input": "큰 공", "output": "작은 공"},
    ]

    # !pip install chromadb
    # !pip install tiktoken

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        # This is the list of examples available to select from.
        examples,
        # This is the embedding class used to produce embeddings which are used to measure semantic similarity.
        OpenAIEmbeddings(),
        # This is the VectorStore class that is used to store the embeddings and do a similarity search over.
        Chroma,
        # This is the number of examples to produce.
        k=1
    )
    similar_prompt = FewShotPromptTemplate(
        # We provide an ExampleSelector instead of examples.
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix="주어진 입력에 대해 반대의 의미를 가진 단어를 출력해줘",
        suffix="Input: {단어}\nOutput:",
        input_variables=["단어"],
    )

    # Input is a feeling, so should select the happy/sad example
    print(similar_prompt.format(단어="무서운"))
    # Input is a feeling, so should select the happy/sad example
    print(similar_prompt.format(단어="큰 비행기"))
    query = "큰 비행기"
    print(davinch3(similar_prompt.format(단어=query)))

# (5) Output Parser를 활용한 출력값 조정
"""
LLM의 답변을 내가 원하는 형태로 고정하고 싶다면 OutputParser 함수를 활용할 수 있습니다.
리스트, JSON 형태 등 다양한 형식의 답변을 고정하여 출력할 수 있습니다.
"""
def promptTemplate05():
    from langchain.output_parsers import CommaSeparatedListOutputParser
    from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI

    output_parser = CommaSeparatedListOutputParser()
    format_instructions = output_parser.get_format_instructions()
    format_instructions
    prompt = PromptTemplate(
        template="{주제} 5개를 추천해줘.\n{format_instructions}",
        input_variables=["주제"],
        partial_variables={"format_instructions": format_instructions}
    )
    model = OpenAI(temperature=0)
    _input = prompt.format(주제="영화")
    output = model(_input)
    output
    output_parser.parse(output)