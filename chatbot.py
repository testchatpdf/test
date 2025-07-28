import requests

# Sử dụng API Key trực tiếp (thay bằng API Key thực tế của bạn)
API_KEY = "sec_9Z9B3PU67Id21XLmCCfQ4G4sTpm49iPN"

# Hàm gửi câu hỏi tới ChatPDF với sourceId cố định
def ask_question(source_id, question):
    if not API_KEY:
        raise Exception("API Key không được tìm thấy.")
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
        raise Exception(f"Error asking question: {response.status_code} - {response.text}")

# Hàm chính để chạy chatbot
def main():
    # Sử dụng sourceId cố định đã có
    source_id = "src_IAt3Zah3IeHjCiOrqFa4j"

    try:
        print(f"Using existing Source ID: {source_id}")

        # Vòng lặp để nhập câu hỏi
        while True:
            question = input("Hỏi về nội dung PDF (hoặc nhập 'quit' để thoát): ")
            if question.lower() == "quit":
                break
            answer = ask_question(source_id, question)
            print(f"Trả lời: {answer}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {str(e)}")

if __name__ == "__main__":