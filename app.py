import streamlit as st
import google.generativeai as genai

# Cấu hình trang
st.set_page_config(page_title="Trợ lý AI của anh Đạt", page_icon="🤖")

# CSS đơn giản
st.markdown("""
<style>
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Khởi tạo session
if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.title("🤖 Trợ lý AI - Anh Đạt Digital")
st.write("**Em đã sẵn sàng tư vấn cho anh Đạt rồi đây!**")

# Lấy API Key
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    with st.sidebar:
        st.warning("Chưa có API Key trong Secrets")
        manual_key = st.text_input("Nhập API Key thủ công:", type="password")
        if manual_key:
            api_key = manual_key

if not api_key:
    st.error("Vui lòng cung cấp API Key để sử dụng trợ lý AI")
    st.stop()

# Khởi tạo model
try:
    genai.configure(api_key=api_key)
    
    # THỬ CÁC MODEL KHÁC NHAU
    models_to_try = [
        'gemini-1.5-pro-latest',    # Mới nhất
        'gemini-1.5-flash-latest',  # Flash mới nhất
        'models/gemini-1.5-pro',    # Với prefix models/
        'gemini-pro',               # Model cũ
    ]
    
    model = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # Test với prompt đơn giản
            test_response = model.generate_content("Hi")
            if test_response.text:
                st.success(f"✅ Đã kết nối với: {model_name}")
                break
        except:
            continue
    
    if not model:
        st.error("Không thể kết nối với bất kỳ model nào. Vui lòng thử lại!")
        st.stop()
        
except Exception as e:
    st.error(f"Lỗi kết nối: {str(e)}")
    st.stop()

# Hiển thị lịch sử
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
user_input = st.chat_input("Anh/Chị cần em tư vấn gì ạ?")

if user_input:
    # Hiển thị câu hỏi
    with st.chat_message("user"):
        st.write(user_input)
    
    # Lưu vào history
    st.session_state.history.append({"role": "user", "content": user_input})
    
    # Tạo câu trả lời
    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ..."):
            try:
                response = model.generate_content(user_input)
                answer = response.text if hasattr(response, 'text') else "Không có phản hồi"
                st.write(answer)
                st.session_state.history.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Lỗi: {str(e)}"
                st.error(error_msg)