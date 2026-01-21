import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang
st.set_page_config(page_title="Trợ lý AI của anh Đạt", page_icon="🤖")

# 2. Kết nối API từ Secrets (Lấy chìa khóa từ mục Secrets)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # SỬA LỖI 404: Chỉ để gemini-1.5-flash, bỏ chữ models/
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Anh Đạt ơi, chưa có mã API trong mục Secrets!")
    st.stop()

# 3. Giao diện ứng dụng
st.title("🤖 Trợ lý AI - Anh Đạt Digital")
st.write("Em đã sẵn sàng tư vấn Phong Thủy và Decor cho anh Đạt!")

user_input = st.text_input("Anh/Chị cần em tư vấn gì hôm nay ạ?")

if st.button("Hỏi Trợ lý"):
    if user_input:
        with st.spinner('Đang suy nghĩ...'):
            try:
                # Gửi câu hỏi cho AI và nhận câu trả lời
                response = model.generate_content(user_input)
                st.markdown("### Trả lời:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi rồi anh ơi: {e}")
    else:
        st.warning("Anh/Chị nhập câu hỏi trước nhé!")
