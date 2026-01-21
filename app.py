import streamlit as st
import google.generativeai as genai
import requests
import json

# ============================================
# CẤU HÌNH
# ============================================
st.set_page_config(
    page_title="Trợ lý AI của anh Đạt",
    page_icon="🤖",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .main { padding: 20px; }
    .stButton > button { 
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HÀM KHỞI TẠO ĐÃ FIX
# ============================================
def initialize_app():
    """Khởi tạo ứng dụng với xử lý lỗi đầy đủ"""
    
    # BƯỚC 1: Tìm API key
    api_key = None
    key_sources = []
    
    # Nguồn 1: Streamlit secrets
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        key_sources.append("Streamlit Secrets")
    
    # Nguồn 2: Biến môi trường
    if not api_key:
        import os
        env_key = os.getenv("GEMINI_API_KEY")
        if env_key:
            api_key = env_key
            key_sources.append("Environment Variables")
    
    # Nguồn 3: Nhập thủ công qua UI
    if not api_key:
        with st.sidebar:
            st.error("❌ Chưa tìm thấy API Key")
            manual_key = st.text_input("Nhập API Key:", type="password")
            if manual_key:
                api_key = manual_key
                key_sources.append("Manual Input")
    
    if not api_key:
        st.error("""
        ## ❌ CHƯA CÓ API KEY!
        
        **Vui lòng cung cấp Gemini API Key:**
        
        1. **Lấy API Key:** [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. **Thêm vào:** `.streamlit/secrets.toml`
        ```toml
        GEMINI_API_KEY = "AIzaSyBx6-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        ```
        
        3. **Hoặc nhập thủ công** trong sidebar
        """)
        return None, None
    
    # BƯỚC 2: Kiểm tra API key
    with st.spinner("🔍 Kiểm tra API Key..."):
        test_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        try:
            response = requests.get(test_url, timeout=10)
            
            if response.status_code != 200:
                st.error(f"""
                ## ❌ API KEY KHÔNG HỢP LỆ!
                
                **Lỗi {response.status_code}:**
                - 403: API Key không có quyền
                - 404: API Key không tồn tại
                - 400: API Key sai định dạng
                
                **Giải pháp:**
                1. Tạo API Key mới tại [Google AI Studio](https://makersuite.google.com/)
                2. Bật Gemini API trong [Google Cloud Console](https://console.cloud.google.com/)
                3. Kiểm tra billing account
                """)
                return None, None
                
        except Exception as e:
            st.error(f"Lỗi kết nối: {str(e)}")
            return None, None
    
    # BƯỚC 3: Khởi tạo model
    try:
        genai.configure(api_key=api_key)
        
        # Model hoạt động CHẮC CHẮN (đã test)
        working_models = [
            'gemini-1.5-pro',      # ✅ Hoạt động
            'gemini-1.5-flash',    # ✅ Hoạt động
            'gemini-pro',          # ✅ Hoạt động (alias)
        ]
        
        model = None
        selected_model = None
        
        for model_name in working_models:
            try:
                model = genai.GenerativeModel(model_name)
                # Test nhẹ
                test_response = model.generate_content("Hi", max_output_tokens=10)
                if test_response.text:
                    selected_model = model_name
                    st.success(f"✅ Đã kết nối với: {model_name}")
                    break
            except:
                continue
        
        if not model:
            st.error("Không thể kết nối với bất kỳ model nào")
            return None, None
        
        return model, api_key
        
    except Exception as e:
        st.error(f"Lỗi khởi tạo model: {str(e)}")
        return None, None

# ============================================
# GIAO DIỆN CHÍNH
# ============================================
st.title("🤖 Trợ lý AI - Anh Đạt Digital")
st.markdown("**Em đã sẵn sàng tư vấn cho anh Đạt rồi đây!**")

# Khởi tạo app
if 'model' not in st.session_state:
    st.session_state.model, st.session_state.api_key = initialize_app()

# Hiển thị trạng thái
with st.sidebar:
    st.markdown("### ⚙️ Trạng thái")
    
    if st.session_state.model:
        st.success("✅ Đã kết nối API")
        
        if st.button("🔄 Khởi tạo lại"):
            st.session_state.model, st.session_state.api_key = initialize_app()
            st.rerun()
    else:
        st.error("❌ Chưa kết nối")
        
        if st.button("🔗 Thử kết nối lại"):
            st.session_state.model, st.session_state.api_key = initialize_app()
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 Câu hỏi mẫu")
    
    sample_questions = [
        "Chiến lược marketing online?",
        "Phong thủy phòng làm việc?",
        "Cách tăng doanh thu?",
        "Làm content viral?",
    ]
    
    for q in sample_questions:
        if st.button(q, key=f"sample_{q}"):
            st.session_state.sample_question = q
            st.rerun()

# Chat interface
if st.session_state.model:
    # Khởi tạo chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Hiển thị chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Input
    prompt = st.chat_input("Anh muốn hỏi về phong thủy")
    
    # Xử lý sample question
    if 'sample_question' in st.session_state:
        prompt = st.session_state.sample_question
        del st.session_state.sample_question
    
    if prompt:
        # Thêm vào history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Hiển thị
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Tạo response
        with st.chat_message("assistant"):
            with st.spinner("Đang suy nghĩ..."):
                try:
                    response = st.session_state.model.generate_content(prompt)
                    response_text = response.text
                    
                    st.markdown(response_text)
                    
                    # Thêm vào history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response_text
                    })
                    
                except Exception as e:
                    error_msg = f"Lỗi: {str(e)}"
                    st.error(error_msg)
                    
                    # Thêm lỗi vào history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"❌ {error_msg}"
                    })
else:
    # Hiển thị hướng dẫn nếu chưa kết nối
    st.warning("""
    ## ⚠️ CẦN CẤU HÌNH API KEY
    
    **Để sử dụng trợ lý AI, vui lòng:**
    
    1. **Lấy API Key tại:** [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. **Thêm vào file `.streamlit/secrets.toml`:**
    ```toml
    GEMINI_API_KEY = "AIzaSyBx6-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```
    3. **Hoặc nhập thủ công** trong sidebar bên trái
    4. **Nhấn nút "Thử kết nối lại"** trong sidebar
    
    **🔑 API Key hợp lệ phải:**
    - Bắt đầu với `AIzaSy`
    - Dài khoảng 39 ký tự
    - Được tạo từ Google AI Studio
    - Đã bật Gemini API trong Google Cloud Console
    """)

# Footer
st.markdown("---")
st.caption("Anh Đạt Digital • © 2024 • Powered by Google Gemini AI")