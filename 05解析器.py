from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

first_prompt = PromptTemplate.from_template("请生成一个长度为{len}的英文单词,要求输出按照json格式,k是word，v是英文的单词")

second_prompt = PromptTemplate.from_template("帮我解释{word}的意思")


model = Tongyi(api_key="apikey",model="qwen-max")


chain = first_prompt | model | json_parser | second_prompt | model | str_parser


res = chain.stream({"len":"5"})

for chunk in res:
    print(chunk, end="", flush=True)