from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class EmbeddingManager:
    def __init__(self, embedding_model_name: str):
        self.embedding_model_name = embedding_model_name
        self.embedding = OpenAIEmbeddings(model=self.embedding_model_name)

    def create_embedding(self, chunks: list):
        vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=self.embedding
        )

        return vectorstore

