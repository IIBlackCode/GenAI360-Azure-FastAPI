import os
import requests
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
def run(question):

    endpoint = "https://kms-genai360-openai.openai.azure.com/"  
    deployment = "gpt-4o"  
    search_endpoint = "https://search-mzc-prod-search-01.search.windows.net"  
    search_key = "H2Qt1LsqCThh0sfpkdkfsCcIba4AY8yXinZeOQZyIhAzSeB69pio"  
    search_index = "vector-prefix-1234" 

    try:
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://cognitiveservices.azure.com/.default")
        print(token_provider)
        client = AzureOpenAI(
            azure_endpoint="https://kms-genai360-openai.openai.azure.com/",
            azure_ad_token_provider=token_provider,
            api_version="2024-05-01-preview",
        )
            
        print(client)
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
                        "query_type": "semantic",  
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