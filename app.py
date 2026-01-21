import streamlit as st
import google.generativeai as genai

# Cấu hình trang
st.set_page_config(page_title="Trợ lý AI của anh Đạt", page_icon="🤖")

# Kết nối với Gemini qua Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Anh Đạt ơi, hãy kiểm tra lại mục Secrets trên Streamlit nhé!")
    st.stop()

st.title("🤖 Trợ lý AI - Anh Đạt Digital")
st.write("Chào mừng anh/chị! Em là trợ lý thông minh chuyên tư vấn Phong Thủy và Decor.")

user_input = st.text_input("Anh/Chị cần em tư vấn gì hôm nay ạ?")

if st.button("Hỏi Trợ lý"):
    if user_input:
        with st.spinner('Em đang suy nghĩ...'):
            try:
                # Huấn luyện AI đóng vai chuyên gia
                prompt = f"Bạn là chuyên gia Phong Thủy và Decor của Anh Đạt Digital. Hãy trả lời thật ngọt ngào, chuyên nghiệp và gọi khách là Anh/Chị: {user_input}"
                response = model.generate_content(prompt)
                
                st.markdown("### Trả lời từ Trợ lý:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi rồi anh ơi: {e}")
    else:
        st.warning("Anh/Chị nhập câu hỏi vào ô trên nhé!")
