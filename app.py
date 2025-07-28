import streamlit as st
import requests

# Thay bằng API Key của bạn
API_KEY = "sec_9Z9B3PU67Id21XLmCCfQ4G4sTpm49iPN"
# Sử dụng sourceId bạn cung cấp
SOURCE_IDS = ["CT73v2j5ywDHUtzNKMtyM"]  # Chỉ cần sourceId này, thêm thêm nếu có nhiều PDF

def ask_question(source_id, question):
    url = "https://api.chatpdf.com/v1/chats/message"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "sourceId": source_id,
        "messages": [{"role": "user", "content": question}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["content"]
    else:
        return f"Error: {response.text}"

# Giao diện Streamlit
st.title("ChatPDF Chatbot")

# Vì chỉ có một sourceId, không cần chọn
selected_source = SOURCE_IDS[0]

question = st.text_input("Hỏi về nội dung PDF:")
if question:
    with st.spinner("Đang xử lý..."):
        answer = ask_question(selected_source, question)
    st.write(f"Trả lời: {answer}")