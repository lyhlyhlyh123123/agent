import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="sk-54c5cde195864e09a43673ca5a930b43",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "给我写一个dfs的代码"},
    ],
    stream=True
)
for chunk in completion:
    print(chunk.choices[0].delta.content, end="", flush=True)