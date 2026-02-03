from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from agent.rag.vector_store import VectorStoreService
from agent.utils.logger_handler import logger
from agent.utils.config_handler import prompt_conf
from langchain_core.runnables import RunnableLambda
from agent.model.factory import chat_model
from agent.utils.path_tool import get_abs_path
from agent.utils.prompt_loader import load_rag_prompt
def print_prompt(prompt):
    print(f"RAGPrompt: {prompt.to_string()}")
    return prompt

class RagSummarizeService:
    # 类变量缓存，所有实例共用
    _PROMPT_TEXT: str = None

    def __init__(self, vector_store: VectorStoreService):
        self.vector_store = vector_store
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template |RunnableLambda(print_prompt)| self.model | StrOutputParser()
        return chain

    def retrieve_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        # key: input, for user query
        # key: context, 参考资料
        input_dict = {}
        context_docs = self.retrieve_docs(query)
        print(f"[RAG_DEBUG] 检索到 {len(context_docs)} 条文档")
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】：参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"
        input_dict["input"] = query
        input_dict["context"] = context

        return self.chain.invoke(input_dict)


# for testing
if __name__ == '__main__':
    vs = VectorStoreService()
    rag = RagSummarizeService(vs)

    print(rag.rag_summarize("地毯环境扫地机器人使用建议？"))
