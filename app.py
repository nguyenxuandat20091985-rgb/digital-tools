import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json

# ============================================
# CẤU HÌNH TRANG
# ============================================
st.set_page_config(
    page_title="Trợ lý AI của anh Đạt",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    /* Mobile-first design */
    .main {
        padding: 10px;
    }
    
    /* Chat containers */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 0 18px;
        margin: 8px 0 8px auto;
        max-width: 80%;
        text-align: left;
        float: right;
        clear: both;
    }
    
    .bot-message {
        background: #f0f2f6;
        color: #333;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 0;
        margin: 8px auto 8px 0;
        max-width: 80%;
        text-align: left;
        float: left;
        clear: both;
        border: 1px solid #ddd;
    }
    
    /* Clear floats */
    .message-container::after {
        content: "";
        display: table;
        clear: both;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    
    /* Input styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 12px;
    }
    
    /* Quick question buttons */
    .quick-question {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 4px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .quick-question:hover {
        background: #e9ecef;
        border-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# KHỞI TẠO SESSION STATE
# ============================================
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'model_initialized' not in st.session_state:
    st.session_state.model_initialized = False

# ============================================
# HÀM KHỞI TẠO MODEL - FIXED
# ============================================
def initialize_gemini():
    """Khởi tạo model Gemini với xử lý lỗi mới nhất"""
    try:
        # Lấy API key từ nhiều nguồn
        api_key = None
        
        # Ưu tiên 1: Từ secrets
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        # Ưu tiên 2: Từ session state
        elif st.session_state.api_key:
            api_key = st.session_state.api_key
        # Ưu tiên 3: Từ biến môi trường
        else:
            import os
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            return None, "Vui lòng cung cấp API Key"
        
        # Cấu hình Gemini
        genai.configure(api_key=api_key)
        
        # DANH SÁCH MODEL KHẢ DỤNG MỚI NHẤT (Tháng 1/2025)
        available_models = [
            'gemini-1.5-pro',          # Model PRO chính thức
            'gemini-1.5-flash',        # Model FLASH chính thức
            'gemini-1.0-pro',          # Model PRO cũ
            'gemini-pro',              # Tên ngắn gọn
        ]
        
        # Thử từng model
        for model_name in available_models:
            try:
                # Tạo model
                model = genai.GenerativeModel(model_name)
                
                # Test với prompt đơn giản
                test_response = model.generate_content(
                    "Hello",
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=100,
                        temperature=0.1
                    )
                )
                
                # Kiểm tra response hợp lệ
                if test_response and hasattr(test_response, 'text') and test_response.text:
                    st.session_state.model_initialized = True
                    return model, f"✅ Đã kết nối với model: {model_name}"
                    
            except Exception as model_error:
                continue
        
        # Nếu không model nào hoạt động
        return None, "Không thể kết nối với bất kỳ model nào. Vui lòng kiểm tra API key."
        
    except Exception as e:
        return None, f"Lỗi khởi tạo: {str(e)}"

# ============================================
# SIDEBAR - CÀI ĐẶT
# ============================================
with st.sidebar:
    st.title("⚙️ Cài đặt")
    
    # Kiểm tra API Key
    st.subheader("🔑 API Configuration")
    
    # Hiển thị trạng thái hiện tại
    if st.session_state.api_key:
        st.success("✅ Đã có API Key")
        if st.button("🔁 Reset API Key"):
            st.session_state.api_key = ""
            st.session_state.model_initialized = False
            st.rerun()
    else:
        st.warning("⚠️ Chưa có API Key")
    
    # Nhập API Key thủ công
    with st.expander("Nhập API Key thủ công"):
        manual_key = st.text_input(
            "Gemini API Key:",
            type="password",
            placeholder="AIzaSyBx6...",
            help="Lấy API key tại: https://makersuite.google.com/app/apikey"
        )
        
        if manual_key:
            st.session_state.api_key = manual_key
            if st.button("Lưu & Kết nối"):
                with st.spinner("Đang kết nối..."):
                    model, message = initialize_gemini()
                    if model:
                        st.success(message)
                    else:
                        st.error(message)
    
    # Debug info
    with st.expander("📊 Thông tin debug"):
        st.write(f"Model initialized: {st.session_state.model_initialized}")
        st.write(f"Chat history length: {len(st.session_state.chat_history)}")
        
        if st.button("Clear Session"):
            st.session_state.clear()
            st.rerun()
    
    # Quick links
    st.markdown("---")
    st.markdown("### 🔗 Liên kết hữu ích")
    st.markdown("[Google AI Studio](https://makersuite.google.com/)")
    st.markdown("[Gemini API Docs](https://ai.google.dev/)")
    st.markdown("[Streamlit Docs](https://docs.streamlit.io/)")

# ============================================
# HEADER
# ============================================
st.title("🤖 Trợ lý AI - Anh Đạt Digital")
st.markdown("### **Em đã sẵn sàng tư vấn cho anh Đạt rồi đây!**")

# ============================================
# HIỂN THỊ LỊCH SỬ CHAT
# ============================================
chat_container = st.container()

with chat_container:
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 💬 Lịch sử trò chuyện")
        
        for i, chat in enumerate(st.session_state.chat_history):
            if chat["role"] == "user":
                st.markdown(f'<div class="message-container"><div class="user-message"><strong>👤 Bạn:</strong><br>{chat["content"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-container"><div class="bot-message"><strong>🤖 AI:</strong><br>{chat["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.info("💡 **Chào mừng! Hãy bắt đầu trò chuyện với trợ lý AI.**")

# ============================================
# CÂU HỎI NHANH
# ============================================
st.markdown("---")
st.markdown("### 🚀 Câu hỏi nhanh")

col1, col2, col3 = st.columns(3)

quick_questions = [
    ("🎯 Chiến lược Digital Marketing", "Tư vấn cho tôi chiến lược digital marketing hiệu quả"),
    ("🏠 Phong thủy văn phòng", "Phong thủy cho văn phòng làm việc cần lưu ý gì?"),
    ("💰 Tăng doanh thu online", "Làm thế nào để tăng doanh thu bán hàng online?"),
    ("📱 Content viral", "Cách tạo content viral trên mạng xã hội"),
    ("🔍 SEO website", "Chiến lược SEO website hiệu quả nhất hiện nay"),
    ("🎨 Thiết kế website", "Nguyên tắc thiết kế website chuyên nghiệp")
]

for idx, (title, question) in enumerate(quick_questions):
    if idx < 2:
        with col1:
            if st.button(title, key=f"quick_{idx}"):
                st.session_state.quick_question = question
    elif idx < 4:
        with col2:
            if st.button(title, key=f"quick_{idx}"):
                st.session_state.quick_question = question
    else:
        with col3:
            if st.button(title, key=f"quick_{idx}"):
                st.session_state.quick_question = question

# ============================================
# INPUT FORM
# ============================================
st.markdown("---")
st.markdown("### 💭 Đặt câu hỏi của bạn")

# Sử dụng form để tránh reload
with st.form(key="chat_form", clear_on_submit=True):
    # Xử lý quick question
    if 'quick_question' in st.session_state:
        default_question = st.session_state.quick_question
        del st.session_state.quick_question
    else:
        default_question = ""
    
    user_input = st.text_area(
        "**Nhập câu hỏi của bạn:**",
        value=default_question,
        placeholder="Ví dụ: Tôi muốn hỏi về phong thủy cho phòng ngủ...",
        height=100,
        key="question_input"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        submit_button = st.form_submit_button(
            "🚀 **Gửi câu hỏi**",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        clear_button = st.form_submit_button(
            "🗑️ **Xóa lịch sử**",
            use_container_width=True
        )

# ============================================
# XỬ LÝ SUBMIT
# ============================================
if submit_button and user_input:
    # Kiểm tra API và model
    if not st.session_state.model_initialized:
        model, message = initialize_gemini()
        if not model:
            st.error(f"❌ {message}")
            st.stop()
    
    # Thêm câu hỏi vào lịch sử
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    # Tạo prompt cải tiến
    system_prompt = """Bạn là Trợ lý AI chuyên gia của anh Đạt, chuyên tư vấn về:
    1. Digital Marketing & SEO
    2. Phong thủy & Kiến trúc
    3. Kinh doanh online
    4. Công nghệ & Ứng dụng
    
    Hãy trả lời:
    - Chi tiết, thực tế, có ví dụ cụ thể
    - Có số liệu và case study nếu có
    - Đưa ra 3-5 bước hành động
    - Kết thúc bằng lời động viên tích cực
    
    Câu hỏi: """
    
    full_prompt = system_prompt + user_input
    
    # Hiển thị trạng thái xử lý
    with st.spinner("🤔 **Trợ lý AI đang suy nghĩ...**"):
        try:
            # Khởi tạo lại model để đảm bảo kết nối
            genai.configure(api_key=st.session_state.api_key or st.secrets.get("GEMINI_API_KEY", ""))
            
            # SỬ DỤNG MODEL CHÍNH THỨC
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Gửi request
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2000,
                )
            )
            
            # Kiểm tra và xử lý response
            if response and hasattr(response, 'text'):
                answer = response.text
            else:
                answer = "Xin lỗi, tôi không thể tạo câu trả lời lúc này. Vui lòng thử lại."
            
            # Thêm vào lịch sử
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Rerun để hiển thị
            st.rerun()
            
        except Exception as e:
            error_msg = str(e)
            
            # Xử lý lỗi cụ thể
            if "404" in error_msg and "models" in error_msg:
                error_msg = "Lỗi model không tìm thấy. Đang thử model khác..."
                try:
                    # Thử model flash
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(full_prompt)
                    answer = response.text
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    st.rerun()
                    
                except:
                    error_msg = "Không thể kết nối với API Gemini. Vui lòng kiểm lại API Key."
            
            st.error(f"❌ {error_msg}")
            
            # Lưu lỗi vào lịch sử
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"❌ **Lỗi:** {error_msg}\n\nVui lòng:\n1. Kiểm tra API Key\n2. Thử lại sau ít phút\n3. Liên hệ hỗ trợ",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()

# Xử lý clear button
if clear_button:
    st.session_state.chat_history = []
    st.success("✅ Đã xóa lịch sử trò chuyện")
    st.rerun()

# ============================================
# FOOTER & TRẠNG THÁI
# ============================================
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    status = "🟢 Đang hoạt động" if st.session_state.model_initialized else "🟡 Chờ kết nối"
    st.caption(f"**Trạng thái:** {status}")

with col2:
    st.caption(f"**Số tin nhắn:** {len(st.session_state.chat_history)}")

with col3:
    st.caption(f"**Thời gian:** {datetime.now().strftime('%H:%M')}")

# ============================================
# HƯỚNG DẪN SỬ DỤNG
# ============================================
with st.expander("📚 **Hướng dẫn sử dụng chi tiết**"):
    st.markdown("""
    ### 🎯 **Cách sử dụng:**
    1. **Nhập API Key** trong sidebar (nếu chưa có trong Secrets)
    2. **Nhập câu hỏi** vào ô văn bản hoặc **chọn câu hỏi nhanh**
    3. **Nhấn "Gửi câu hỏi"** để nhận tư vấn từ AI
    
    ### 🔑 **Lấy API Key:**
    1. Truy cập [Google AI Studio](https://makersuite.google.com/)
    2. Đăng nhập bằng tài khoản Google
    3. Tạo API Key mới
    4. Copy và dán vào ứng dụng
    
    ### ⚠️ **Lưu ý quan trọng:**
    - API Key cần có quyền truy cập Gemini API
    - Model sử dụng: **gemini-1.5-pro** (mặc định)
    - Giới hạn: ~60 requests/phút (tùy tài khoản)
    - Lịch sử chat được lưu tạm trong phiên
    
    ### 🆘 **Khắc phục lỗi:**
    **Lỗi 404 Model not found:**
    - Cập nhật thư viện: `pip install --upgrade google-generativeai`
    - Kiểm tra API Key có hợp lệ không
    - Thử model khác: gemini-1.5-flash
    
    **Lỗi API Key không hợp lệ:**
    - Tạo API Key mới tại Google AI Studio
    - Đảm bảo đã bật Gemini API trong Google Cloud
    
    ### 📞 **Hỗ trợ:**
    - Email: support@anhdatdigital.com
    - Zalo: 0912 345 678
    - Website: anhdatdigital.com
    """)

# ============================================
# TẢI XUỐNG LỊCH SỬ CHAT
# ============================================
if st.session_state.chat_history:
    st.markdown("---")
    
    # Chuyển đổi lịch sử thành JSON
    chat_json = json.dumps(st.session_state.chat_history, indent=2, ensure_ascii=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Tải lịch sử chat (JSON)",
            data=chat_json,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # Export as text
        chat_text = ""
        for chat in st.session_state.chat_history:
            role = "👤 Bạn" if chat["role"] == "user" else "🤖 AI"
            chat_text += f"{role} ({chat['timestamp']}):\n{chat['content']}\n\n"
        
        st.download_button(
            label="📄 Tải lịch sử chat (TXT)",
            data=chat_text,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )