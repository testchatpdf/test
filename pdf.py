import fitz  # import PyMuPDF
import os    # Để xử lý đường dẫn và kiểm tra file

def extract_text_from_pdf(pdf_path):
    """
    Trích xuất toàn bộ văn bản từ file PDF được chỉ định.
    """
    text = ""
    # Kiểm tra xem file có tồn tại không trước khi cố gắng mở
    if not os.path.exists(pdf_path):
        print(f"Lỗi: Không tìm thấy file tại đường dẫn '{pdf_path}'. Vui lòng kiểm tra lại tên file và đường dẫn.")
        return "" # Trả về chuỗi rỗng nếu không tìm thấy file

    try:
        doc = fitz.open(pdf_path)
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Lỗi khi trích xuất văn bản từ '{pdf_path}': {e}")
    return text

# --- Phần sử dụng ---
# ĐÃ CẬP NHẬT ĐƯỜNG DẪN FILE CỦA BẠN DỰA TRÊN HÌNH ẢNH:
# File của bạn là '1234.pdf' nằm trong thư mục 'C:\Users\dever\Downloads\New folder'
pdf_file_path = r"C:\Users\dever\Downloads\New folder\1234.pdf"

print(f"Đang cố gắng trích xuất văn bản từ: {pdf_file_path}")

# Gọi hàm để trích xuất nội dung
extracted_content = extract_text_from_pdf(pdf_file_path)

if extracted_content:
    print("\n--- Văn bản trích xuất từ PDF ---")
    # In ra 1000 ký tự đầu tiên để kiểm tra, tránh làm tràn console nếu file rất lớn
    print(extracted_content[:1000])

    # Tùy chọn: Lưu toàn bộ văn bản trích xuất ra file .txt
    output_txt_file = "output_text_from_1234_pdf.txt" # Tên file output gợi nhớ hơn
    try:
        with open(output_txt_file, "w", encoding="utf-8") as f:
            f.write(extracted_content)
        print(f"\nToàn bộ văn bản đã được lưu vào file: {output_txt_file}")
    except Exception as e:
        print(f"Lỗi khi lưu văn bản vào file '{output_txt_file}': {e}")
else:
    print("\nKhông thể trích xuất văn bản từ file PDF. Vui lòng kiểm tra lỗi phía trên nếu có.")