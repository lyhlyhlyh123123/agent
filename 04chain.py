from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,MessagesPlaceholder

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个诗人"),
        MessagesPlaceholder("history"),
        ("human", "根据以上示例生成诗句"),
    ]
)

history_data = [
    ("human", "你来个大气磅礴的诗"),
    ("ai","钟山风雨起苍黄，百万雄师过大江"),
    ("human", "很好再来一个"),
    ("ai","此去泉台招旧部，旌旗十万斩阎罗"),
]

tongyi = Tongyi(api_key="sk-54c5cde195864e09a43673ca5a930b43",model="qwen-max")
chain = chat_template | tongyi

for chunk in chain.stream({"history": history_data}):
    print(chunk, end="", flush=True)

#
# template = """
# 你是一个编程专家，请根据以下信息，生成一个代码，实现以下功能：
# {question}
# """
#
# prompt = PromptTemplate.from_template(template)
# tongyi = Tongyi(api_key="sk-54c5cde195864e09a43673ca5a930b43",model="qwen-max")
# chain = prompt | tongyi
# res = chain.stream({"question": "给我写一个dfs的代码"})
#
# for chunk in res:
#     print(chunk, end="", flush=True)
