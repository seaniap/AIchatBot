import openai
import streamlit as st
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# # 設定 OpenAI API Key
# openai.api_key = "您的 OpenAI API 金鑰"
# 建立 Streamlit UI
st.title("單輪對話GPT聊天機器人")
# 建立輸入框，讓使用者輸入問題
user_input = st.text_input("請輸入您的問題：")
# 回答的限制條件
assistant_limit = "你會問原因。使用台灣繁體中文回答下面問題。回答的句子不要超過50字"
if st.button("送出"):
    if user_input:
        # 呼叫 OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": assistant_limit + user_input}]
        )
        # 顯示回應結果
        st.write("ChatGPT 回應：")
        st.write(response.choices[0].message.content)
    else:
        st.warning("請輸入問題後再送出！")