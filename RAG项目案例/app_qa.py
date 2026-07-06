# streamlit run RAG项目案例\app_qa.py

import time
from rag import RagService
import streamlit as st
import config_data as config

# 标题区域
col1, col2 = st.columns([0.8, 0.2], vertical_alignment="center")
with col1:
    st.title("🤖智能客服助手")
with col2:
    if st.button("🗑️清空记录", use_container_width=True):
        st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你？"}]
        st.rerun()

st.divider()  # 分隔符

# 初始化会话状态
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# 渲染聊天记录
for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 关键：st.chat_input() 独立放在最外层，固定在页面底部
prompt = st.chat_input()

# 处理用户输入
if prompt:
    # 输出用户提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    with st.spinner("AI思考中..."):
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)
        res_stream = st.chat_message("assistant").write_stream(res_stream)
        st.session_state["message"].append({"role": "assistant", "content": res_stream})

# 侧边栏信息
with st.sidebar:
    st.header("ℹ️ 帮助信息")
    st.info("""
    - 支持基于知识库的智能问答
    - 聊天记录仅保存在本地会话中
    - 点击清空按钮可重置所有对话
    """)
    st.divider()
    st.subheader("📊 会话统计")
    st.write(f"总消息数：{len(st.session_state['message'])}")
    user_messages = len([m for m in st.session_state['message'] if m["role"] == "user"])
    st.write(f"你的提问：{user_messages} 条")
    st.write(f"AI回答：{len(st.session_state['message']) - user_messages} 条")