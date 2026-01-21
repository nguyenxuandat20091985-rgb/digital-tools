import streamlit as st
import google.generativeai as genai
import requests
import time

# ============================================
# CẤU HÌNH TRANG
# ============================================
st.set_page_config(
    page_title="Trợ lý AI của anh Đạt",
    page_icon="🤖",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: bold;
    }
    
    .api-success { color: green; font-weight: bold; }
    .api-error { color: red; font-weight: bold; }
    
    .api-test-box {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HÀM KIỂM TRA API KEY
# ============================================
def test_gemini_api_key(api_key):
    """Kiểm tra API key có hợp lệ không"""
    try:
        # Test trực tiếp với Google API
        test_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            available_models = [model['name'] for model in models]
            return True, "✅ API Key hợp lệ", available_models
        elif response.status_code == 403:
            return False, "❌ API Key không có quyền truy cập", []
        elif response.status_code == 404:
            return False, "❌ API Key không tồn tại", []
        else:
            return False, f"❌ Lỗi {response.status_code}: {response.text[:100]}", []
            
    except requests.exceptions.RequestException as e:
        return False, f"❌ Lỗi kết nối: {str(e)}", []
    except Exception as e:
        return False, f"❌ Lỗi không xác định: {str(e)}", []

# ============================================
# HÀM LẤY DANH SÁCH MODEL
# ============================================
def get_available_models(api_key):
    """Lấy danh sách model có sẵn"""
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
        
        return available_models
    except Exception as e:
        st.error(f"Không thể lấy danh sách model: {str(e)}")
        return []

# ============================================
# HÀM KHỞI TẠO MODEL
# ============================================
def initialize_gemini_model(api_key):
    """Khởi tạo Gemini model với API key"""
    try:
        # Cấu hình API
        genai.configure(api_key=api_key)
        
        # Danh sách model ưu tiên (theo thứ tự thử)
        priority_models = [
            'models/gemini-1.5-pro',      # Format đầy đủ
            'models/gemini-1.5-flash',    # Format đầy đủ
            'gemini-1.5-pro',             # Format ngắn
            'gemini-1.5-flash',           # Format ngắn
            'models/gemini-pro',          # Model cũ
            'gemini-pro',                 # Model cũ ngắn
        ]
        
        # Thử từng model
        for model_name in priority_models:
            try:
                st.info(f"🔍 Đang thử model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                # Test với prompt đơn giản
                response = model.generate_content(
                    "Hello",
                    generation_config={
                        "max_output_tokens": 10,
                        "temperature": 0.1
                    }
                )
                
                if response and hasattr(response, 'text'):
                    st.success(f"✅ Đã kết nối thành công với: {model_name}")
                    return model, model_name
                    
            except Exception as model_error:
                continue
        
        return None, "Không thể kết nối với bất kỳ model nào"
        
    except Exception as e:
        return None, f"Lỗi khởi tạo: {str(e)}"

# ============================================
# GIAO DIỆN CHÍNH
# ============================================
st.title("🔧 **Cấu hình Gemini API**")
st.markdown("### Bước 1: Kiểm tra và cấu hình API Key")

# Khởi tạo session state
if 'api_key_valid' not in st.session_state:
    st.session_state.api_key_valid = False
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'model' not in st.session_state:
    st.session_state.model = None

# ============================================
# PHẦN 1: NHẬP VÀ KIỂM TRA API KEY
# ============================================
with st.expander("🔑 **Nhập API Key của bạn**", expanded=True):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        api_key_input = st.text_input(
            "Gemini API Key:",
            value=st.session_state.api_key,
            type="password",
            placeholder="Nhập API Key bắt đầu với AIzaSy...",
            help="Lấy API key tại: https://makersuite.google.com/app/apikey"
        )
    
    with col2:
        if st.button("🧪 **Kiểm tra API Key**", use_container_width=True):
            if api_key_input:
                with st.spinner("Đang kiểm tra API Key..."):
                    time.sleep(1)
                    
                    # Kiểm tra API key
                    is_valid, message, models = test_gemini_api_key(api_key_input)
                    
                    if is_valid:
                        st.session_state.api_key = api_key_input
                        st.session_state.api_key_valid = True
                        st.success(message)
                        
                        # Hiển thị model có sẵn
                        if models:
                            st.markdown("**📋 Model có sẵn:**")
                            for m in models[:5]:  # Hiển thị 5 model đầu
                                st.code(m)
                    else:
                        st.error(message)
                        st.session_state.api_key_valid = False
            else:
                st.warning("Vui lòng nhập API Key")

# ============================================
# PHẦN 2: HƯỚNG DẪN LẤY API KEY
# ============================================
with st.expander("📖 **Hướng dẫn lấy API Key**"):
    st.markdown("""
    ### **Các bước lấy Gemini API Key:**
    
    1. **Truy cập:** [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. **Đăng nhập** bằng tài khoản Google
    3. **Tạo API Key mới:**
       - Click "Create API Key"
       - Chọn "Create API key in new project"
       - Copy API Key (bắt đầu với `AIzaSy...`)
    
    4. **Kích hoạt Gemini API trong Google Cloud (QUAN TRỌNG):**
       - Truy cập: [Google Cloud Console](https://console.cloud.google.com/)
       - Chọn dự án của bạn
       - Tìm "Gemini API"
       - Click "ENABLE"
    
    ### **🔍 Kiểm tra API Key:**
    - API Key hợp lệ: `AIzaSyBx6-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
    - Độ dài: ~39 ký tự
    - Bắt đầu với: `AIzaSy`
    
    ### **⚠️ Lỗi thường gặp:**
    - **API Key không tồn tại:** Tạo API Key mới
    - **Chưa kích hoạt Gemini API:** Enable API trong Google Cloud
    - **Hết hạn API Key:** Tạo lại API Key
    """)

# ============================================
# PHẦN 3: KHỞI TẠO MODEL
# ============================================
if st.session_state.api_key_valid:
    st.markdown("---")
    st.markdown("### **Bước 2: Khởi tạo Model**")
    
    if st.button("🚀 **Khởi tạo Gemini Model**", type="primary"):
        with st.spinner("Đang khởi tạo model..."):
            model, message = initialize_gemini_model(st.session_state.api_key)
            
            if model:
                st.session_state.model = model
                st.success(f"✅ {message}")
                
                # Test chat đơn giản
                st.markdown("### **Bước 3: Test chat đơn giản**")
                test_prompt = "Xin chào, bạn có thể giới thiệu về mình không?"
                
                with st.spinner("Đang test chat..."):
                    try:
                        response = model.generate_content(test_prompt)
                        st.markdown("**🤖 Trả lời test:**")
                        st.info(response.text)
                        
                        # Lưu vào secrets để dùng sau
                        st.markdown("### **✅ Cấu hình thành công!**")
                        st.markdown("""
                        **Bạn đã sẵn sàng sử dụng Gemini API:**
                        1. API Key: ✅ Hợp lệ
                        2. Model: ✅ Đã kết nối
                        3. Chat: ✅ Hoạt động
                        
                        **Để sử dụng trong ứng dụng khác, thêm vào `.streamlit/secrets.toml`:**
                        ```toml
                        GEMINI_API_KEY = "YOUR_API_KEY_HERE"
                        ```
                        """)
                        
                    except Exception as e:
                        st.error(f"Lỗi khi test chat: {str(e)}")
            else:
                st.error(f"❌ {message}")

# ============================================
# PHẦN 4: TEST TRỰC TIẾP VỚI API
# ============================================
st.markdown("---")
st.markdown("### **🛠️ Test API trực tiếp**")

test_key = st.text_input("Test API Key (hoặc dùng key ở trên):", 
                         value=st.session_state.api_key if st.session_state.api_key else "",
                         type="password")

if st.button("🔍 **Test API trực tiếp**"):
    if test_key:
        with st.spinner("Đang test kết nối API..."):
            # Test với requests trực tiếp
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models?key={test_key}"
                response = requests.get(url, timeout=10)
                
                st.markdown("**📊 Kết quả kiểm tra:**")
                
                if response.status_code == 200:
                    st.success("✅ Kết nối API thành công!")
                    
                    # Parse response
                    data = response.json()
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Status Code", response.status_code)
                        st.metric("Số model", len(data.get('models', [])))
                    
                    with col2:
                        st.metric("API Key hợp lệ", "✅ Có")
                        st.metric("Có thể generate", "✅ Có")
                    
                    # Hiển thị vài model
                    st.markdown("**📋 Một số model có sẵn:**")
                    models = data.get('models', [])
                    for i, model in enumerate(models[:3]):
                        st.code(f"{model.get('name', 'Unknown')} - {model.get('displayName', 'No name')}")
                    
                else:
                    st.error(f"❌ Lỗi {response.status_code}")
                    st.text(f"Response: {response.text[:200]}")
                    
            except Exception as e:
                st.error(f"❌ Lỗi kết nối: {str(e)}")
    else:
        st.warning("Vui lòng nhập API Key để test")

# ============================================
# PHẦN 5: TRỢ LÝ CHAT ĐƠN GIẢN
# ============================================
if st.session_state.model:
    st.markdown("---")
    st.markdown("## 💬 **Trợ lý Chat Demo**")
    
    # Chat interface đơn giản
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    # Hiển thị chat history
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f"**👤 Bạn:** {msg['content']}")
        else:
            st.markdown(f"**🤖 AI:** {msg['content']}")
    
    # Input chat
    user_input = st.text_input("Nhập câu hỏi của bạn:", key="chat_input")
    
    if st.button("Gửi câu hỏi") and user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        with st.spinner("AI đang suy nghĩ..."):
            try:
                response = st.session_state.model.generate_content(user_input)
                ai_response = response.text if hasattr(response, 'text') else "Không có phản hồi"
                st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi: {str(e)}")

# ============================================
# PHẦN 6: XỬ LÝ LỖI PHỔ BIẾN
# ============================================
with st.expander("🔧 **Khắc phục lỗi phổ biến**"):
    st.markdown("""
    ### **❌ Lỗi "Không thể kết nối với bất kỳ model nào"**
    
    **Nguyên nhân và giải pháp:**
    
    1. **API Key không hợp lệ:**
       - Kiểm tra lại API Key
       - Tạo API Key mới tại [Google AI Studio](https://makersuite.google.com/app/apikey)
    
    2. **Chưa kích hoạt Gemini API trong Google Cloud:**
       - Truy cập [Google Cloud Console](https://console.cloud.google.com/)
       - Tìm "Gemini API"
       - Click **ENABLE**
    
    3. **API Key hết hạn hoặc bị thu hồi:**
       - Tạo API Key mới
       - Kiểm tra trong [Google Cloud API Dashboard](https://console.cloud.google.com/apis/dashboard)
    
    4. **Tài khoản chưa được cấp quyền:**
       - Đảm bảo tài khoản có quyền truy cập Gemini API
       - Kiểm tra billing account
    
    5. **Quota hết:**
       - Kiểm tra quota tại [Google Cloud Quotas](https://console.cloud.google.com/iam-admin/quotas)
       - Nâng cấp tài khoản nếu cần
    
    ### **🛠️ Cách test nhanh:**
    
    **Command Line Test:**
    ```bash
    curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_API_KEY"
    ```
    
    **Nếu thành công:** Sẽ thấy danh sách model
    **Nếu lỗi:** Kiểm tra API Key và quyền truy cập
    
    ### **📞 Hỗ trợ:**
    - [Google AI Support](https://developers.google.com/studio/support)
    - [Gemini API Documentation](https://ai.google.dev/docs)
    - [Google Cloud Support](https://cloud.google.com/support)
    """)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.caption("🔧 **Gemini API Configuration Tool** • Anh Đạt Digital • © 2024")