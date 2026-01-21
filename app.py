import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime

# 1. Cấu hình trang
st.set_page_config(
    page_title="Trợ lý AI của anh Đạt",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .main {
            padding: 10px;
        }
        .stButton > button {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border-radius: 12px;
            margin: 8px 0;
        }
        .chat-message {
            padding: 12px 16px;
            border-radius: 18px;
            margin: 8px 0;
            max-width: 85%;
            word-wrap: break-word;
        }
    }
    
    /* Chat message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .bot-message {
        background: #f0f2f6;
        color: #333;
        margin-right: auto;
        border: 1px solid #e0e0e0;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Khởi tạo session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'model_initialized' not in st.session_state:
    st.session_state.model_initialized = False
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# 3. Kết nối API - FIXED VERSION
def initialize_gemini_model():
    """Khởi tạo model Gemini với xử lý lỗi"""
    try:
        # Kiểm tra và lấy API key
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        else:
            # Fallback: cho phép nhập thủ công
            if not st.session_state.api_key:
                return None
            api_key = st.session_state.api_key
        
        # Cấu hình Gemini
        genai.configure(api_key=api_key)
        
        # QUAN TRỌNG: Sử dụng đúng model name
        # Thử các model khả dụng
        available_models = [
            'gemini-1.5-pro-latest',    # Model mới nhất
            'gemini-1.5-flash-latest',  # Model flash mới nhất
            'gemini-pro',               # Model cũ
            'models/gemini-pro'         # Format đầy đủ
        ]
        
        model = None
        for model_name in available_models:
            try:
                model = genai.GenerativeModel(model_name)
                # Test với prompt nhỏ
                response = model.generate_content("Hello")
                if response.text:
                    st.success(f"✅ Đã kết nối với model: {model_name}")
                    st.session_state.model_initialized = True
                    return model
            except Exception as e:
                continue
        
        # Nếu không model nào hoạt động
        st.error("Không thể kết nối với bất kỳ model nào. Vui lòng kiểm tra API key.")
        return None
        
    except Exception as e:
        st.error(f"Lỗi khởi tạo model: {str(e)}")
        return None

# 4. Giao diện chính
st.title("🤖 Trợ lý AI - Anh Đạt Digital")
st.markdown("**Em đã sẵn sàng tư vấn cho anh Đạt rồi đây!**")

# Sidebar cho cài đặt
with st.sidebar:
    st.header("⚙️ Cài đặt")
    
    # Kiểm tra API key
    if "GEMINI_API_KEY" not in st.secrets:
        st.warning("⚠️ Chưa cấu hình API Key trong Secrets")
        api_key_input = st.text_input(
            "Nhập Gemini API Key:",
            type="password",
            help="Lấy API key tại: https://makersuite.google.com/app/apikey"
        )
        
        if api_key_input:
            st.session_state.api_key = api_key_input
            if st.button("Kết nối API"):
                with st.spinner("Đang kết nối..."):
                    initialize_gemini_model()
    
    # Model selection
    st.markdown("---")
    st.subheader("🎯 Tùy chọn Model")
    
    model_options = {
        "gemini-1.5-pro-latest": "Pro (Tốt nhất)",
        "gemini-1.5-flash-latest": "Flash (Nhanh)",
        "gemini-pro": "Pro cũ",
    }
    
    selected_model = st.selectbox(
        "Chọn model:",
        list(model_options.keys()),
        format_func=lambda x: model_options[x]
    )
    
    if st.button("Khởi tạo lại Model"):
        st.session_state.model_initialized = False
        st.rerun()
    
    st.markdown("---")
    st.subheader("💾 Lịch sử chat")
    if st.button("Xóa lịch sử"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Hiển thị số tin nhắn
    st.info(f"Số tin nhắn: {len(st.session_state.chat_history)}")

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    # Hiển thị chat history
    chat_container = st.container(height=400, border=True)
    
    with chat_container:
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f"""
                <div style="text-align: right; margin: 10px 0;">
                    <div class="chat-message user-message">
                        <strong>Anh Đạt:</strong><br>
                        {chat["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="text-align: left; margin: 10px 0;">
                    <div class="chat-message bot-message">
                        <strong>🤖 Trợ lý AI:</strong><br>
                        {chat["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

with col2:
    # Quick actions
    st.markdown("### 💡 Câu hỏi nhanh")
    
    quick_questions = [
        "Cách tăng traffic website?",
        "Chiến lược marketing?",
        "Tối ưu SEO?",
        "Content viral?",
        "Quảng cáo Facebook hiệu quả?"
    ]
    
    for question in quick_questions:
        if st.button(question, key=f"quick_{question}"):
            st.session_state.user_input = question

# Input area
st.markdown("---")

# Sử dụng form để tránh reload trang
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "**Anh/Chị cần em tư vấn gì ạ?**",
        placeholder="Ví dụ: Anh muốn tư vấn về chiến lược digital marketing...",
        height=100,
        key="user_input_field"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        submit_button = st.form_submit_button(
            "🚀 **Hỏi Trợ lý**",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        voice_input = st.form_submit_button(
            "🎤 Nhập bằng giọng nói",
            use_container_width=True
        )
    
    with col3:
        clear_button = st.form_submit_button(
            "🧹 Xóa",
            use_container_width=True
        )
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()

# 5. Xử lý khi submit
if submit_button and user_input:
    # Kiểm tra model
    if not st.session_state.model_initialized:
        with st.spinner("🔄 Đang khởi tạo model..."):
            model = initialize_gemini_model()
            if not model:
                st.error("Không thể khởi tạo model. Vui lòng kiểm tra API key!")
                st.stop()
    else:
        try:
            # Sử dụng model đã khởi tạo
            genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", st.session_state.api_key))
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
        except:
            model = initialize_gemini_model()
    
    # Thêm câu hỏi vào lịch sử
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    # Hiển thị typing indicator
    with st.spinner('🤔 **Em đang suy nghĩ...**'):
        try:
            # Tạo prompt cải tiến
            system_prompt = """Bạn là trợ lý AI chuyên gia Digital Marketing của anh Đạt. 
            Hãy trả lời chi tiết, thực tế và có tính ứng dụng cao.
            Nếu là câu hỏi về marketing/digital, hãy đưa ra chiến lược cụ thể.
            Luôn kết thúc với gợi ý hành động tiếp theo."""
            
            full_prompt = f"{system_prompt}\n\nCâu hỏi: {user_input}"
            
            # Gửi request tới Gemini
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2000,
                }
            )
            
            # Kiểm tra response
            if hasattr(response, 'text') and response.text:
                answer = response.text
            else:
                answer = "Xin lỗi, em không thể tạo câu trả lời lúc này. Anh vui lòng thử lại nhé!"
            
            # Thêm câu trả lời vào lịch sử
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Tự động scroll xuống
            st.rerun()
            
        except Exception as e:
            error_msg = f"Lỗi rồi anh ơi: {str(e)}"
            st.error(error_msg)
            
            # Log lỗi vào lịch sử
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"❌ {error_msg}\n\nVui lòng kiểm tra API key hoặc thử lại sau.",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()

# 6. Hiển thị trạng thái hệ thống
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption(f"🕒 {datetime.now().strftime('%H:%M:%S')}")

with col2:
    status = "✅ Đang hoạt động" if st.session_state.model_initialized else "⚠️ Chờ kết nối"
    st.caption(f"Trạng thái: {status}")

with col3:
    st.caption(f"Tin nhắn: {len(st.session_state.chat_history)}")

# 7. Hướng dẫn sử dụng
with st.expander("📖 Hướng dẫn sử dụng"):
    st.markdown("""
    ### Cách sử dụng:
    1. **Nhập câu hỏi** vào ô văn bản
    2. **Nhấn "Hỏi Trợ lý"** hoặc phím Enter
    3. **Chọn câu hỏi nhanh** bên phải để tiết kiệm thời gian
    
    ### Lĩnh vực tư vấn:
    - Digital Marketing
    - SEO & Content
    - Social Media
    - Quảng cáo Facebook/Google
    - Chiến lược kinh doanh online
    - Phát triển website
    
    ### Lưu ý:
    - API Key cần được cấu hình trong Secrets (hoặc nhập thủ công)
    - Model tự động chọn phiên bản ổn định nhất
    - Lịch sử chat được lưu trong session
    """)

# 8. Debug information (chỉ hiển thị trong development)
if st.secrets.get("DEBUG", False):
    with st.expander("🔧 Debug Info"):
        st.write("Session state:", st.session_state)
        st.write("Model initialized:", st.session_state.model_initialized)