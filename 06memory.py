import os,json
from typing import Sequence, List

from langchain_community.llms.tongyi import Tongyi
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
f

class FileChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, session_id: str, storage_path: str):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, self.session_id)

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        message_dicts = [message_to_dict(m) for m in all_messages]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(message_dicts, f)

    @property
    def messages(self) -> List[BaseMessage]:
        """读取历史消息，文件不存在时返回空列表"""
        if not os.path.exists(self.file_path):
            return []  # 首次运行，文件还没创建

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                message_dicts = json.load(f)
            return messages_from_dict(message_dicts)
        except (json.JSONDecodeError, FileNotFoundError):
            # 文件损坏或被删除时返回空列表
            return []

    def clear(self) -> None:
        with open(self.file_path, "w") as f:
            json.dump([], f)


def print_prompt(prompt):
    print(f"Prompt: {prompt}")
    return prompt

str_parser = StrOutputParser()
model = Tongyi(api_key="sk-54c5cde195864e09a43673ca5a930b43",model="qwen-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据历史记录回答的问题"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

def get_history(session_id):
    return FileChatMessageHistory(session_id, "./historydata")


base_chain = prompt | model | str_parser

conversation = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)



if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id": "user_1"
        }
    }
    res = conversation.invoke({"input":"小明有一只猫"},session_config)
    print(res)
    res =conversation.invoke({"input":"小明有三只狗"},session_config)
    print(res)
    res =conversation.invoke({"input":"现在小明有几个动物"},session_config)
    print(res)
