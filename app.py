#import openai
import openai
import streamlit as st
import time
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 設定 API Key
try:
    # 嘗試從 Streamlit Secrets 讀取
    #openai.api_key = st.secrets["openai"]["api_key"]
    openai.api_key = st.secrets["openai"]["api_key"]
except Exception as e:
    # 如果沒有 Secrets，則從環境變數讀取
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        st.error("請設定 OpenAI API Key！")
        st.info("在 Streamlit Cloud 上，請在專案設定中的 Secrets 加入：\n```toml\n[openai]\napi_key = \"你的-OpenAI-API-Key\"\n```")
        st.stop()

# 初始化 session_state
# 使用 session_state 來保存對話歷史和當前回應
# 這樣在 Streamlit 重新渲染時不會丟失資料
if "messages" not in st.session_state:
    st.session_state.messages = []  # 儲存所有對話歷史
if "current_response" not in st.session_state:
    st.session_state.current_response = ""  # 儲存當前正在串流的回應

def stream_response(messages):
    """使用 yield 處理串流回應"""
    try:
        stream = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        st.error(f"API 呼叫錯誤：{str(e)}")
        yield "抱歉，發生錯誤，請稍後再試。"

# 建立使用者輸入介面
user_input = st.text_input("請輸入您的問題：")

# 設定 AI 助手的回答限制條件
assistant_limit = (
    "使用台灣繁體中文回答下面問題。"
    "回答的句子不要超過50字。你覺得需要時會問原因。"
)

if st.button("送出"):
    if user_input:
        # 將使用者輸入加入歷史記錄
        st.session_state.messages.append({
            "role": "user",
            "content": assistant_limit + user_input
        })

        # 建立一個空的回應容器
        response_container = st.empty()
        st.session_state.current_response = ""

        # 使用 yield 處理串流回應
        for text_chunk in stream_response(st.session_state.messages):
            st.session_state.current_response += text_chunk
            response_container.write(st.session_state.current_response + " ▌")
            time.sleep(0.01)

        # 將完整的回應存入歷史記錄
        st.session_state.messages.append({
            "role": "assistant",
            "content": st.session_state.current_response
        })
    else:
        st.warning("請輸入問題後再送出！")

# 顯示完整的對話歷史
st.subheader("💬 聊天紀錄")
for message in st.session_state.messages:
    role = "👤 使用者：" if message["role"] == "user" else "🤖 ChatGPT："
    st.write(f"{role} {message['content']}")