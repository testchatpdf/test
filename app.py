import streamlit as st
import requests

API_KEY = "sec_Cc2RpBY3WeEbjtRbBTrlomxufxHq5nfz"
SOURCE_IDS = ["MQrphdpKv99AaOzRZypro"]

def ask_question(source_id, question):
    if not API_KEY:
        return "Lỗi: API Key không được tìm thấy."
    if not question or not question.strip():
        return "Lỗi: Vui lòng nhập câu hỏi."
    url = "https://api.chatpdf.com/v1/chats/message"
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    data = {"sourceId": source_id, "messages": [{"role": "user", "content": question}]}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["content"]
    else:
        return f"Lỗi: {response.status_code} - {response.text}"

st.title("ChatPDF Chatbot")

selected_source = SOURCE_IDS[0]

question = st.text_input("Hỏi về nội dung PDF:")
if question and question.strip():
    with st.spinner("Đang xử lý..."):
        answer = ask_question(selected_source, question)
    if answer:
        st.write(f"Trả lời: {answer}")
    else:
        st.error("Không thể xử lý yêu cầu. Vui lòng kiểm tra lại.")