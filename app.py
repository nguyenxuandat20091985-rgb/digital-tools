import streamlit as st
import google.generativeai as genai

# Cấu hình trang
st.set_page_config(page_title="Trợ lý AI của anh Đạt", page_icon="🤖")

# Kết nối API từ Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Sử dụng tên model ngắn gọn để tránh lỗi 404
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Lỗi: Không tìm thấy API Key!")
    st.stop()

st.title("🤖 Trợ lý AI - Anh Đạt Digital")
st.write("Em đã sẵn sàng tư vấn Phong Thủy và Decor cho anh Đạt!")

user_input = st.text_input("Anh/Chị cần em tư vấn gì ạ?")

if st.button("Hỏi Trợ lý"):
    if user_input:
        with st.spinner('Đang suy nghĩ...'):
            try:
                # Gửi câu hỏi cho AI
                res = model.generate_content(user_input)
                st.markdown("### Trả lời:")
                st.write(res.text)
            except Exception as e:
                st.error(f"Lỗi: {e}")
    else:
        st.warning("Vui lòng nhập câu hỏi!")
