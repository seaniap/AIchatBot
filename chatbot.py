import openai
import streamlit as st
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 初始化 session_state，確保每次執行時不會丟失對話紀錄
if "messages" not in st.session_state:
    st.session_state.messages = []


# 建立輸入框
user_input = st.text_input("請輸入您的問題：")
# 回答的限制條件
assistant_limit = "使用台灣繁體中文回答下面問題。回答的句子不要超過50字。你覺得需要時會問原因。"

if st.button("送出"):
    if user_input:
        # 將使用者輸入加入歷史記錄
        st.session_state.messages.append({
            "role": "user",
            "content": assistant_limit + user_input
        })

        # 呼叫 OpenAI API，傳送完整的對話歷史
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )

        # 取得 ChatGPT 回應
        bot_response = response.choices[0].message.content

        # 將 ChatGPT 的回應也存入歷史記錄
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # 顯示回應結果
        st.write("ChatGPT 回應：")
        st.write(bot_response)
    else:
        st.warning("請輸入問題後再送出！")

# 顯示對話歷史
st.subheader("💬 聊天紀錄")
for message in st.session_state.messages:
    role = "👤 使用者：" if message["role"] == "user" else "🤖 ChatGPT："
    st.write(f"{role} {message['content']}")