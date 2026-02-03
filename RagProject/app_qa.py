import time
from rag import RagService
import streamlit as st
import config_data as config
st.title("智能客服")
st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"你好有什么可以帮助你的？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("请输入问题：")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    ai_res_list = []
    with st.spinner("正在思考"):
        time.sleep(1)
        result_stream = st.session_state["rag"].chain.stream({"input":prompt},config.session_config)
        def capture(generator,cache_list):
           for chunk in generator:
               cache_list.append(chunk)
               yield  chunk

        st.chat_message("assistant").write_stream(capture(result_stream,ai_res_list))
        st.session_state["message"].append({"role":"assistant","content":"".join(ai_res_list)})
