from typing import List

from langchain_community.llms.tongyi import Tongyi
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
embeddings = DashScopeEmbeddings(dashscope_api_key="apikey")
text = "苹果手机价格多少钱？"
str_parser = StrOutputParser()
vectorstore = Chroma(
    collection_name="test",
    embedding_function=embeddings,
    persist_directory="./chroma"
)

loader = CSVLoader(
    file_path="./txt.csv",
    encoding="utf-8",
    source_column="实体"
)
document = loader.load()

vectorstore.add_documents(
    documents=document,
    ids = ["id"+ str(i) for i in range(1, len(document) + 1) ]
)

#result = vectorstore.similarity_search(text, k=2)


model = Tongyi(api_key="apikey",model="qwen-max")

def print_prompt(prompt):
    print(f"Prompt: {prompt}")
    return prompt

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据已知的参考资料回答问题,参考资料{content}"),
        ("user", "用户提问{input}"),
    ]
)
#返回一个runnable接口的实例对象，用于入链
retriever = vectorstore.as_retriever(search_kwargs={"k":2})

def format_func(doc: List[Document]) -> str:
    if not doc:
        return "无相关参考资料"
    formatted_str ="["
    for do in doc:
        formatted_str += do.page_content
    formatted_str = formatted_str+"]"
    return formatted_str


chain =({"input":RunnablePassthrough(),"content":retriever |format_func}| prompt|print_prompt| model| str_parser)

res = chain.invoke(text)
print(res)



# chain = prompt | print_prompt | model | str_parser
# res = chain.invoke({"input":text,"content":result})
# print(res)