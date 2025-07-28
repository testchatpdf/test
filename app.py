import streamlit as st
import requests

API_KEY = "sec_9Z9B3PU67Id21XLmCCfQ4G4sTpm49iPN"


def upload_pdf(file):
    url = "https://api.chatpdf.com/v1/sources/add-file"
    headers = {"x-api-key": API_KEY}
    response = requests.post(url, headers=headers, files={"file": file})
    return response.json()["sourceId"] if response.status_code == 200 else None


def ask_question(source_id, question):
    url = "https://api.chatpdf.com/v1/chats/message"
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    data = {"sourceId": source_id, "messages": [{"role": "user", "content": question}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()["content"] if response.status_code == 200 else "Lỗi"


# Giao diện Streamlit
st.title("ChatPDF Chatbot")
uploaded_file = st.file_uploader("Tải lên file PDF", type="pdf")

if uploaded_file:
    source_id = upload_pdf(uploaded_file)
    st.write(f"PDF uploaded. Source ID: {source_id}")

    question = st.text_input("Hỏi về nội dung PDF:")
    if question:
        answer = ask_question(source_id, question)
        st.write(f"Trả lời: {answer}")