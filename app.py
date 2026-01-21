import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang
st.set_page_config(page_title="Trợ lý AI của anh Đạt", page_icon="🤖")

# 2. Kết nối API
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # DÒNG QUAN TRỌNG: Viết dính liền trên 1 dòng
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Lỗi: Không tìm thấy API Key trong Secrets!")
    st.stop()

# 3. Giao diện
st.title("🤖 Trợ lý AI - Anh Đạt Digital")
st.write("Em đã sẵn sàng tư vấn cho anh Đạt rồi đây!")

user_input = st.text_input("Anh/Chị cần em tư vấn gì ạ?")

if st.button("Hỏi Trợ lý"):
    if user_input:
        with st.spinner('Đợi em một chút nhé...'):
            try:
                # Gửi câu hỏi
                response = model.generate_content(user_input)
                st.markdown("### Trả lời:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi rồi anh ơi: {e}")
