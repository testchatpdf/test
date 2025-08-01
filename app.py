import streamlit as st
import requests
import os # Import module os để làm việc với đường dẫn file

API_KEY = "sec_Cc2RpBY3WeEbjtRbBTrlomxufxHq5nfz" # Giữ nguyên API Key của bạn cho ChatPDF
SOURCE_IDS = ["cha_34WQKyw6jr8SIIqT6xuEX"] # Giữ nguyên Source ID của bạn

# Hàm gửi câu hỏi tới ChatPDF
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

# Hàm tìm kiếm hình ảnh cục bộ
def get_local_images(query, answer):
    image_paths = []
    # Định nghĩa đường dẫn đến thư mục chứa hình ảnh cục bộ của bạn
    # Đảm bảo thư mục 'static/images' nằm trong cùng cấp với 'app.py'
    image_directory = os.path.join(os.path.dirname(__file__), "static", "images")

    # Kiểm tra xem thư mục có tồn tại không
    if not os.path.isdir(image_directory):
        st.warning(f"Thư mục hình ảnh không tồn tại: {image_directory}")
        return []

    # Đây là phần LOGIC quan trọng để quyết định hình ảnh nào sẽ được hiển thị.
    # Bạn cần tùy chỉnh phần này dựa trên cách bạn muốn chatbot liên kết câu trả lời/câu hỏi với hình ảnh.
    # Dưới đây là một số ví dụ đơn giản:

    # VD 1: Hiển thị hình ảnh nếu từ khóa trong câu hỏi/câu trả lời khớp với tên file
    # (Bạn sẽ cần đặt tên file hình ảnh có ý nghĩa, ví dụ: "quy_trinh_xay_dung.png")
    all_image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Chuyển đổi query và answer thành chữ thường để so sánh không phân biệt chữ hoa chữ thường
    lower_query = query.lower()
    lower_answer = answer.lower()

    for filename in all_image_files:
        # Lấy tên file không có phần mở rộng (ví dụ: "quy_trinh_xay_dung")
        name_without_extension = os.path.splitext(filename)[0].replace("_", " ") # Thay _ bằng khoảng trắng để so sánh dễ hơn

        # Logic 1: Nếu tên file (đã làm sạch) xuất hiện trong câu hỏi hoặc câu trả lời
        if name_without_extension in lower_query or name_without_extension in lower_answer:
            image_paths.append(os.path.join(image_directory, filename))
            # Có thể thêm break ở đây nếu bạn chỉ muốn hiển thị 1 hình ảnh đầu tiên tìm thấy
            # break

        # Logic 2: Bạn có thể tạo một mapping thủ công (ví dụ: một dictionary)
        # mapping_keywords_to_images = {
        #     "quy trình xây dựng": "quy_trinh_xay_dung.png",
        #     "sơ đồ": "so_do_he_thong.jpg",
        #     "báo cáo tài chính": "bao_cao_tai_chinh.png"
        # }
        # for keyword, img_file in mapping_keywords_to_images.items():
        #     if keyword in lower_query or keyword in lower_answer:
        #         if img_file == filename: # Đảm bảo file tồn tại
        #             image_paths.append(os.path.join(image_directory, filename))
        #             break # Lấy hình ảnh đầu tiên khớp

    return image_paths

st.title("ChatPDF Chatbot với Hình ảnh Cục bộ")

# Sử dụng sourceId đầu tiên trong danh sách SOURCE_IDS
selected_source = SOURCE_IDS[0]

question = st.text_input("Hỏi về nội dung PDF:")
if question and question.strip():
    with st.spinner("Đang xử lý..."):
        # Lấy câu trả lời từ ChatPDF
        answer = ask_question(selected_source, question)

        if answer:
            st.write(f"Trả lời: {answer}")

            # Gọi hàm để lấy đường dẫn hình ảnh cục bộ
            # Truyền cả câu hỏi và câu trả lời để có nhiều ngữ cảnh hơn
            local_image_paths = get_local_images(question, answer)

            if local_image_paths:
                st.subheader("Hình ảnh liên quan từ thư mục cục bộ:")
                for img_path in local_image_paths:
                    # Streamlit có thể hiển thị hình ảnh từ đường dẫn file cục bộ
                    st.image(img_path, caption=os.path.basename(img_path), width=800)
            else:
                st.info("Không tìm thấy hình ảnh liên quan trong thư mục cục bộ.")
        else:
            st.error("Không thể xử lý yêu cầu. Vui lòng kiểm tra lại.")