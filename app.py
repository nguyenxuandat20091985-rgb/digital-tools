import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Trợ lý AI của anh Đạt", page_icon="🤖")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Em đã cập nhật dòng này để hết lỗi 404 cho anh
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.error("Anh Đạt ơi, hãy kiểm tra mục Secrets nhé!")
    st.stop()

st.title("🤖 Trợ lý AI - Anh Đạt Digital")
st.write("Chào mừng anh/chị! Em là trợ lý thông minh của cửa hàng anh Đạt.")

user_input = st.text_input("Anh/Chị cần tư vấn gì về sản phẩm số không ạ?")

if st.button("Hỏi Trợ lý"):
    if user_input:
        with st.spinner('Đang suy nghĩ...'):
            try:
                response = model.generate_content(user_input)
                st.markdown("### Trả lời:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi rồi anh ơi: {e}")
    else:
        st.warning("Anh/Chị nhập câu hỏi trước nhé!")
