from openai import OpenAI

#本地部署
client = OpenAI(api_key="sk-54c5cde195864e09a43673ca5a930b43", base_url="http://localhost:11434/v1")

response = client.chat.completions.create(
    model="qwen3:4b",
    # messages=[
    #     {"role": "system", "content": "你是一个编程专家,并且回答很简介"},
    #     {"role": "assistant", "content": "好的我是一个编程专家，下面将回答你的问题"},
    #     {"role": "user", "content": "给我写一个dfs的代码"}
    # ]
    # 历史消息
    messages=[
            {"role": "system", "content": "你是一个通用助手,并且回答很简介"},
            {"role": "user", "content": "小明的狗7岁了"},
            {"role": "assistant", "content": "好的了解"},
            {"role": "user", "content": "小红的狗4岁了"},
            {"role": "assistant", "content": "好的了解"},
            {"role": "user", "content": "小黄的狗5岁了"},
            {"role": "assistant", "content": "好的了解"},
            {"role": "user", "content": "小红的狗几岁了？"},
        ]
    , stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)

#print(completion.choices[0].message.content)

