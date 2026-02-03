from typing import List

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda

from file_history_store import FileChatMessageHistory, MessagesPlaceholder
from vector_stores import VectorStoreService
import config_data as config

def get_history(session_id):
    return FileChatMessageHistory(session_id, "./historydata")
def print_prompt(prompt):
    print(f"Prompt: {prompt}")
    return prompt
class RagService(object):
    def __init__(self):
        self.vectorstore  = VectorStoreService(embedding=DashScopeEmbeddings(
            model = config.embedding_model_name,
            dashscope_api_key = config.dashscope_api_key
        ))
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "你需要根据已知的参考资料回答问题,参考资料{context}。\n并且我提供对话历史记录,如下："),
            MessagesPlaceholder(variable_name="history"),
            ("human", "回答用户提问{input}")
        ])
        self.chat_model = ChatTongyi(api_key=config.tongyi_api_key,model=config.chat_model_name)
        self.chain =self.__get_chain()

    def __get_chain(self):
        retriever = self.vectorstore.get_retriever()
        def format_document(docs: List[Document]):
            if not docs:
                return "无相关参考资料"

            formatted_str =""
            for doc in docs:
                formatted_str += f"文档片段:{doc.page_content}\n文档元数据:{doc.metadata}\n\n"
            formatted_str += ""
            return formatted_str
        def format_for_retriever(valve):
            return valve["input"]

        def format_for_prompt_template(valve):
            new_valve={}
            new_valve["input"] = valve["input"]["input"]
            new_valve["context"] = valve["context"]
            new_valve["history"] = valve["input"]["history"]
            return new_valve
        def debug(valve):
            print(valve)
            return valve
        chain = (
                {"input":RunnablePassthrough() ,"context": RunnableLambda(format_for_retriever)|retriever|format_document }
                |RunnableLambda(format_for_prompt_template)|RunnableLambda(debug)|self.prompt_template|self.chat_model|StrOutputParser()
        )
        conversation = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        return conversation

if __name__ == "__main__":
    session_config = {
        "configurable": {
            "session_id": "user_2"
        }
    }
    rag = RagService().chain.invoke({"input":"羽绒服有什么推荐"},session_config)
    print(rag)