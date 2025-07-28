import requests
import json

# Thay bằng API Key của bạn
API_KEY = "sec_9Z9B3PU67Id21XLmCCfQ4G4sTpm49iPN"


# Hàm tải lên PDF và nhận sourceId
def upload_pdf(file_path):
    url = "https://api.chatpdf.com/v1/sources/add-file"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "multipart/form-data"
    }

    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        return response.json()["sourceId"]
    else:
        raise Exception(f"Error uploading PDF: {response.text}")


# Hàm gửi câu hỏi tới ChatPDF
def ask_question(source_id, question):
    url = "https://api.chatpdf.com/v1/chats/message"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "sourceId": source_id,
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["content"]
    else:
        raise Exception(f"Error asking question: {response.text}")


# Hàm chính để chạy chatbot
def main():
    # Đường dẫn tới file PDF
    pdf_path = "path/to/your/pdf/file.pdf"  # Thay bằng đường dẫn tới file PDF của bạn

    try:
        # Tải lên PDF
        source_id = upload_pdf(pdf_path)
        print(f"PDF uploaded successfully. Source ID: {source_id}")

        # Vòng lặp để nhập câu hỏi
        while True:
            question = input("Hỏi về nội dung PDF (hoặc nhập 'quit' để thoát): ")
            if question.lower() == "quit":
                break
            answer = ask_question(source_id, question)
            print(f"Trả lời: {answer}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")


if __name__ == "__main__":
    main()