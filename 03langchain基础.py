from langchain_community.llms.tongyi import Tongyi
from langchain_ollama import OllamaLLM,OllamaEmbeddings

#tongyi = Tongyi(api_key="apikey",model="qwen-max")

# tongyi = OllamaLLM(model="qwen3:4b",apikey = "lyh")
#
# res = tongyi.stream(input="给我写一个dfs的代码")
#
#
# for chunk in res:
#     print(chunk, end="", flush=True)


#向量化
model = OllamaEmbeddings(model="qwen3-embedding")

res = model.embed_documents(["三角形","正方形"])
print(res)
