import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang
st.set_page_config(page_title="Trợ lý AI của anh Đạt", page_icon="🤖")

# 2. Kết nối API
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # EM ĐÃ SỬA DÒNG NÀY (Bỏ chữ models/ đi)
 model = genai.GenerativeModel('gemini-1.5-flash')

    st.error("Lỗi: Không tìm thấy API Key trong Secrets!")
    st.stop()

# 3. Giao diện
st.title("🤖 Trợ lý AI - Anh Đạt Digital")
st.write("Em đã sẵn sàng tư vấn Phong Thủy và Decor cho anh rồi đây!")

user_input = st.text_input("Anh/Chị cần em tư vấn gì ạ?")

if st.button("Hỏi Trợ lý"):
    if user_input:
        with st.spinner('Đợi em một chút nhé...'):
            try:
                # Gửi câu hỏi cho AI
                prompt = f"Bạn là chuyên gia Phong Thủy. Hãy trả lời thân thiện: {user_input}"
                response = model.generate_content(prompt)
                
                st.markdown("### Trả lời:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi: {e}")
