import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = os.getenv("ENDPOINT_URL", "https://kms-genai360-openai.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://kms-genai360-aisearch.search.windows.net")
search_key = os.getenv("SEARCH_KEY", "V0fQzvftpy68OdR92eo96UQUmAtMIyEz99zEKFk0QMAzSeCKmwaO")
search_index = os.getenv("SEARCH_INDEX_NAME", "kms-vevtor-embedded")

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default")
      
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",
)
      
completion = client.chat.completions.create(
    model=deployment,
    messages= [
    {
      "role": "user",
      "content": "What are the differences between Azure Machine Learning and Azure AI services?"
    }],
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
            "endpoint": f"{search_endpoint}",
            "index_name": "kms-vevtor-embedded",
            "semantic_configuration": "kms-vevtor-embedded-semantic-configuration",
            "query_type": "semantic",
            "fields_mapping": {},
            "in_scope": True,
            "role_information": "You are an AI assistant that helps people find information.",
            "filter": None,
            "strictness": 3,
            "top_n_documents": 5,
            "authentication": {
              "type": "api_key",
              "key": f"{search_key}"
            },
            "key": f"{search_key}",
            "indexName": f"{search_index}"
          }
        }]
    }
)
print(completion.to_json())