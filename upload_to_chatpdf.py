import requests
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()
CHATPDF_API_KEY = os.getenv("CHATPDF_API_KEY")

def upload_pdf_to_chatpdf(file_path):
    """
    Tải file PDF lên ChatPDF API và trả về sourceId.
    """
    if not CHATPDF_API_KEY:
        print("Lỗi: CHATPDF_API_KEY không được tìm thấy. Vui lòng kiểm tra file .env.")
        return None

    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file tại đường dẫn '{file_path}'. Vui lòng kiểm tra lại.")
        return None

    url = "https://api.chatpdf.com/v1/sources/add-file" # Đây là endpoint để tải file lên
    headers = {
        "x-api-key": CHATPDF_API_KEY,
    }

    try:
        with open(file_path, "rb") as f: # Mở file ở chế độ nhị phân (binary)
            files = {"file": f} # Dữ liệu file để gửi đi
            response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            source_id = response.json()["sourceId"]
            print(f"File '{file_path}' đã được tải lên ChatPDF thành công!")
            print(f"********** SOURCE ID MỚI CỦA BẠN LÀ: {source_id} **********")
            return source_id
        else:
            print(f"Lỗi khi tải file lên ChatPDF: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn khi tải file lên: {e}")
        return None

# --- ĐÂY LÀ PHẦN BẠN CẦN CHỈNH SỬA DUY NHẤT TRONG FILE NÀY ---
# Thay đổi 'C:\Users\dever\Downloads\New folder\1234.pdf' bằng ĐƯỜNG DẪN CHÍNH XÁC đến file PDF của bạn.
# Dựa trên hình ảnh bạn gửi, đường dẫn của file là 'C:\Users\dever\Downloads\New folder\1234.pdf'.
your_pdf_file_path = r"C:\Users\dever\Downloads\New folder\1234.pdf"

if __name__ == "__main__":
    print(f"Đang chuẩn bị tải file: {your_pdf_file_path}")
    new_source_id = upload_pdf_to_chatpdf(your_pdf_file_path)
    if new_source_id:
        print("\n-----------------------------------------------------------")
        print(f"Vui lòng ghi lại SOURCE ID này: {new_source_id}")
        print("Bạn sẽ cần ID này để dán vào file app.py và chatbot.py ở Bước 3.")
        print("-----------------------------------------------------------")
    else:
        print("\nKhông thể lấy được Source ID mới. Vui lòng kiểm tra lỗi phía trên và API Key của bạn.")