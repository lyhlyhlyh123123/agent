from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config

class VectorStoreService:
    def __init__(self, embedding):
        self.embedding = embedding

        self.vectorstore = Chroma(
            persist_directory=config.persist_directory,
            embedding_function=self.embedding,
            collection_name=config.collection_name,
        )
    def get_retriever(self):
        return self.vectorstore.as_retriever(search_kwargs={"k":config.similarity_threshold})

if __name__ == "__main__":
    embedding = DashScopeEmbeddings(model="text-embedding-v4",dashscope_api_key="apikey")
    vectorstore = VectorStoreService(embedding)
    retriever = vectorstore.get_retriever()
    result = retriever.invoke("我的体重180斤，给我合适的尺码")
    print(result)