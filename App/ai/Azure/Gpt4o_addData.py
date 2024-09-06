import os
import requests
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.core.credentials import AzureKeyCredential
def run(question):

    # endpoint = os.getenv("ENDPOINT_URL", "https://kms-genai360-openai.openai.azure.com/")
    # deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
    # search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://kms-genai360-aisearch.search.windows.net")
    # search_key = os.getenv("SEARCH_KEY", "JZkLhXMpQ2M2WBO3gpYLny8GRzOVLAw6zuISkruRbrAzSeCf7rC6")
    # search_index = os.getenv("SEARCH_INDEX_NAME", "kms-vevtor-embedded")

    endpoint = "https://kms-genai360-openai.openai.azure.com/"  
    deployment = "gpt-4o-mini"
    search_endpoint = "https://kms-genai360-aisearch.search.windows.net"  
    search_key = "JZkLhXMpQ2M2WBO3gpYLny8GRzOVLAw6zuISkruRbrAzSeCf7rC6"
    search_index = "kms-vevtor-embedded" 

    print("2024-09-05")

    # credential = AzureKeyCredential(search_key)

    try:
        print(DefaultAzureCredential())
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://cognitiveservices.azure.com/.default")
        
        # Azure Open AI Client
        client = AzureOpenAI(
            azure_endpoint="https://kms-genai360-openai.openai.azure.com/",
            azure_ad_token_provider=token_provider,
            api_version="2024-05-01-preview",
        )
        
        # search_client = SearchClient(search_endpoint, search_index, AzureKeyCredential(search_key))

        completion = client.chat.completions.create(  
            model=deployment,  
            messages=[  
                {  
                    "role": "user",  
                    "content": "What are the differences between Azure Machine Learning and Azure AI services?"  
                }  
            ],  
            max_tokens=800,  
            temperature=0.7,  
            top_p=0.95,  
            frequency_penalty=0,  
            presence_penalty=0,  
            stop=None,  
            stream=False,  
            extra_body={  
                "data_sources": [{  
                    "type": "azure_search",  
                    "parameters": {  
                        "endpoint": search_endpoint,  
                        "index_name": search_index,  
                        "semantic_configuration": "vector-prefix-1234-semantic-configuration",  
                        "query_type": "semantic", # simple:키워드 
                        "fields_mapping": {},  
                        "in_scope": True,  
                        "role_information": "You are an AI assistant that helps people find information.",  
                        "filter": None,  
                        "strictness": 3,  
                        "top_n_documents": 5,  
                        "authentication": {  
                            "type": "api_key",  
                            "key": search_key
                        }  
                    }  
                }]  
            }  
        )
        # Send request
        print(completion.to_json())
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    json_response = response.json()
    content = json_response['choices'][0]['message']['content']
    return content