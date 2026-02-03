from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

@tool(description="获取天气信息")
def get_weather():
    return "今天的天气是晴天"

agent = create_agent(
    model=ChatTongyi(model = "qwen3-max",api_key = "sk-54c5cde195864e09a43673ca5a930b43"),
    tools=[get_weather],
    system_prompt ="你是一个聊天助手，可以回答用户的问题"

)
res  = agent.invoke(
    {
        "messages":[
            {"role": "user", "content": "明天深圳的天气如何？"},
        ]
    }
)

print(res)