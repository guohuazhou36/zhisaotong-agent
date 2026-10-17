import os
import time


def _apply_streamlit_secrets() -> None:
    """把 Streamlit Cloud Secrets 写入环境变量，供 ChatTongyi / 工具读取。"""
    try:
        from streamlit import secrets
    except Exception:
        return

    try:
        # 兼容 dict / AttrDict；本地无 secrets.toml 时可能抛错，忽略即可
        for key in ("DASHSCOPE_API_KEY", "GAODE_API_KEY"):
            try:
                value = secrets[key]
            except Exception:
                continue
            if value is None:
                continue
            text = str(value).strip()
            if text:
                os.environ[key] = text
    except Exception:
        return


_apply_streamlit_secrets()

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

if not (os.getenv("DASHSCOPE_API_KEY") or "").strip():
    st.error(
        "未检测到 DASHSCOPE_API_KEY。请在 Streamlit Cloud → Manage app → Settings → Secrets 中配置：\n\n"
        'DASHSCOPE_API_KEY = "你的密钥"\n'
        'GAODE_API_KEY = "你的高德密钥"'
    )
    st.stop()

from agent.react_agent import ReactAgent

# 标题
st.title("智扫通机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):

            for chunk in generator:
                cache_list.append(chunk)

                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})
        st.rerun()
