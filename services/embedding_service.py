import os

from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS


class EmbeddingService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_key):
        self.embeddings = AzureOpenAIEmbeddings(
            api_key=os.environ.get('AZURE_OPENAI_API_KEY'),
            api_version=os.environ.get('OPENAI_API_VERSION'),
            azure_endpoint=os.environ.get('AZURE_OPENAI_BASE'),
            model=os.environ.get('OPENAI_EMBEDDING_MODEL_ID')
        )

    def generate_locations_embeddings(self, texts):
        return FAISS.from_texts(texts, self.embeddings)

    def find_matching_results(self, input_text, vector_store, k=3):
        results = vector_store.similarity_search_with_score(input_text, k=k)
        return results if results else None
