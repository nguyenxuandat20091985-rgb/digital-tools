import streamlit as st
import requests
import json
import time
from PIL import Image
import io
import base64
from datetime import datetime
import uuid

# Page configuration
st.set_page_config(
    page_title="AI Decor & Phong Thủy",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-first design
st.markdown("""
<style>
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .main {
            padding: 0;
        }
        .stButton > button {
            width: 100%;
            padding: 20px;
            font-size: 18px;
            border-radius: 15px;
            margin: 10px 0;
        }
        .card {
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .warning-card {
            background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
            color: white;
        }
        .suggestion-card {
            background: linear-gradient(135deg, #ffd93d, #ffed4e);
            color: #333;
        }
        .success-card {
            background: linear-gradient(135deg, #6bce75, #4cd964);
            color: white;
        }
        .payment-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 5px solid #007bff;
        }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(50,50,93,.1);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Camera input styling */
    .stCameraInput > div {
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'activation_code' not in st.session_state:
    st.session_state.activation_code = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Phong Thủy rules database
FENG_SHUI_RULES = {
    "bed": [
        {
            "rule": "Đầu giường không nên hướng ra cửa chính",
            "severity": "warning",
            "description": "Theo phong thủy, đầu giường hướng ra cửa sẽ gây mất ngủ và thiếu an toàn"
        },
        {
            "rule": "Giường nên có điểm tựa vững chắc phía sau",
            "severity": "suggestion",
            "description": "Nên đặt giường sát tường để có điểm tựa, tăng cảm giác an toàn"
        },
        {
            "rule": "Không đặt giường dưới xà nhà",
            "severity": "warning",
            "description": "Xà nhà tạo áp lực lên người nằm, gây đau đầu và mệt mỏi"
        }
    ],
    "mirror": [
        {
            "rule": "Gương không nên đối diện giường",
            "severity": "warning",
            "description": "Gương đối diện giường gây mất ngủ và ảnh hưởng đến sức khỏe"
        },
        {
            "rule": "Gương không nên đối diện cửa chính",
            "severity": "warning",
            "description": "Gương đối diện cửa đẩy năng lượng tốt ra ngoài"
        },
        {
            "rule": "Gương nên đặt ở vị trí giúp mở rộng không gian",
            "severity": "suggestion",
            "description": "Gương nên đặt đối diện cửa sổ hoặc nơi có ánh sáng tốt"
        }
    ],
    "door": [
        {
            "rule": "Cửa chính không nên đối diện cửa sau",
            "severity": "warning",
            "description": "Năng lượng tốt sẽ đi thẳng ra ngoài mà không lưu lại trong nhà"
        },
        {
            "rule": "Cửa nên mở ra vào thoải mái, không vướng vật cản",
            "severity": "suggestion",
            "description": "Đảm bảo không gian mở cửa đủ rộng để năng lượng lưu thông"
        }
    ],
    "window": [
        {
            "rule": "Cửa sổ nên đón được ánh sáng tự nhiên",
            "severity": "success",
            "description": "Ánh sáng tự nhiên mang lại năng lượng dương cho không gian"
        },
        {
            "rule": "Cửa sổ không nên có vật cản lớn bên ngoài",
            "severity": "warning",
            "description": "Vật cản làm cản trở năng lượng và tầm nhìn"
        }
    ],
    "kitchen": [
        {
            "rule": "Bếp không nên đối diện nhà vệ sinh",
            "severity": "warning",
            "description": "Năng lượng xung khắc giữa hỏa (bếp) và thủy (nhà vệ sinh)"
        },
        {
            "rule": "Bếp nên được giữ sạch sẽ và ngăn nắp",
            "severity": "suggestion",
            "description": "Bếp sạch sẽ thu hút năng lượng tích cực cho sức khỏe"
        }
    ],
    "desk": [
        {
            "rule": "Bàn làm việc nên quay lưng vào tường",
            "severity": "success",
            "description": "Tạo thế tựa lưng vững chắc, tăng tập trung và may mắn"
        },
        {
            "rule": "Bàn làm việc nên có tầm nhìn tốt ra cửa",
            "severity": "suggestion",
            "description": "Giúp chủ nhân nắm bắt cơ hội và kiểm soát không gian"
        }
    ]
}

# Decor rules database
DECOR_RULES = {
    "color_balance": [
        {
            "rule": "Sử dụng quá nhiều màu sắc nóng",
            "severity": "warning",
            "description": "Nên cân bằng với màu lạnh để tạo cảm giác hài hòa"
        },
        {
            "rule": "Tỷ lệ màu sắc hợp lý (60-30-10)",
            "severity": "success",
            "description": "60% màu chủ đạo, 30% màu phụ, 10% điểm nhấn"
        }
    ],
    "furniture_proportion": [
        {
            "rule": "Đồ nội thất quá lớn so với phòng",
            "severity": "warning",
            "description": "Tạo cảm giác chật chội, nên chọn đồ phù hợp với diện tích"
        },
        {
            "rule": "Bố cục cân đối và có điểm nhấn",
            "severity": "success",
            "description": "Tạo sự hài hòa và thu hút ánh nhìn"
        }
    ],
    "lighting": [
        {
            "rule": "Ánh sáng tự nhiên đầy đủ",
            "severity": "success",
            "description": "Tận dụng tối đa ánh sáng tự nhiên"
        },
        {
            "rule": "Kết hợp nhiều lớp ánh sáng",
            "severity": "suggestion",
            "description": "Ánh sáng tổng thể, ánh sáng nhiệm vụ và ánh sáng trang trí"
        }
    ]
]

def check_payment_activation(activation_code, user_name):
    """Mock function to check activation code"""
    # In production, this would connect to a database
    valid_codes = ["FENG2024", "DECORAI", "PHONGTHUY", "ACTIVE123"]
    
    if activation_code in valid_codes:
        st.session_state.authenticated = True
        st.session_state.user_name = user_name
        return True
    return False

def analyze_image_with_ai(image, api_choice="gemini"):
    """Analyze image using AI Vision API"""
    
    # Mock analysis for demo purposes
    # In production, replace with actual API calls
    
    detected_objects = [
        {"name": "bed", "confidence": 0.95, "position": "center"},
        {"name": "window", "confidence": 0.88, "position": "right"},
        {"name": "door", "confidence": 0.92, "position": "left"},
        {"name": "desk", "confidence": 0.75, "position": "corner"}
    ]
    
    decor_analysis = {
        "color_balance": "Có thể cân bằng thêm màu sắc",
        "furniture_proportion": "Tỷ lệ hợp lý",
        "lighting": "Cần bổ sung ánh sáng trang trí"
    }
    
    return detected_objects, decor_analysis

def get_recommendations(detected_objects, decor_analysis):
    """Generate recommendations based on analysis"""
    recommendations = []
    
    # Check Feng Shui rules
    for obj in detected_objects:
        obj_name = obj["name"]
        if obj_name in FENG_SHUI_RULES:
            for rule in FENG_SHUI_RULES[obj_name]:
                recommendations.append({
                    "category": "Phong Thủy",
                    "object": obj_name,
                    "rule": rule["rule"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "suggestion": f"Kiểm tra {obj_name}: {rule['description']}"
                })
    
    # Check Decor rules
    for category, analysis in decor_analysis.items():
        if category in DECOR_RULES:
            for rule in DECOR_RULES[category]:
                recommendations.append({
                    "category": "Decor",
                    "object": category,
                    "rule": rule["rule"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "suggestion": f"{rule['description']}"
                })
    
    return recommendations

def display_recommendation_card(recommendation):
    """Display a recommendation card with appropriate styling"""
    severity_colors = {
        "warning": "warning-card",
        "suggestion": "suggestion-card",
        "success": "success-card"
    }
    
    severity_icons = {
        "warning": "⚠️",
        "suggestion": "💡",
        "success": "✅"
    }
    
    with st.container():
        st.markdown(f"""
        <div class="card {severity_colors.get(recommendation['severity'], '')}">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <h4 style="margin: 0;">{severity_icons.get(recommendation['severity'], '')} {recommendation['category']}: {recommendation['object'].title()}</h4>
            </div>
            <p><strong>Quy tắc:</strong> {recommendation['rule']}</p>
            <p><strong>Phân tích:</strong> {recommendation['description']}</p>
            <p><strong>Gợi ý:</strong> {recommendation['suggestion']}</p>
        </div>
        """, unsafe_allow_html=True)

def landing_page():
    """Display landing/payment page"""
    st.title("🏠 AI Decor & Phong Thủy")
    st.markdown("### Chào mừng đến với trợ lý AI thông minh cho không gian sống của bạn!")
    
    st.markdown("""
    <div class="payment-info">
    <h4>🌟 Tính năng cao cấp:</h4>
    <ul>
        <li>Phân tích phong thủy chuyên sâu</li>
        <li>Gợi ý decor theo xu hướng</li>
        <li>Nhận diện đồ vật thông minh</li>
        <li>Đánh giá chi tiết không gian</li>
        <li>Hỗ trợ đa ngôn ngữ</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Payment Information
    st.markdown("### 💳 Thanh toán để kích hoạt")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **Thông tin chuyển khoản:**
        - Ngân hàng: BIDV
        - Số tài khoản: 4430269669
        - Chủ tài khoản: NGUYỄN XUÂN ĐẠT
        """)
    
    with col2:
        st.warning("""
        **Lưu ý quan trọng:**
        - Phí kích hoạt: 50,000 VNĐ
        - Thời hạn: 30 ngày
        - Hỗ trợ 24/7
        """)
    
    # User input
    st.markdown("### 🔑 Kích hoạt tài khoản")
    
    user_name = st.text_input("Tên của bạn:", placeholder="Nhập họ tên của bạn")
    payment_content = st.text_input(
        "Nội dung chuyển khoản:",
        value=f"KICHHOAT {user_name}" if user_name else "KICHHOAT",
        disabled=True
    )
    
    activation_code = st.text_input(
        "Mã kích hoạt:",
        placeholder="Nhập mã kích hoạt sau khi thanh toán",
        type="password"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        activate_button = st.button(
            "🎯 KÍCH HOẠT NGAY",
            use_container_width=True,
            type="primary"
        )
    
    if activate_button:
        if not user_name:
            st.error("Vui lòng nhập tên của bạn!")
        elif not activation_code:
            st.error("Vui lòng nhập mã kích hoạt!")
        else:
            with st.spinner("Đang xác thực mã kích hoạt..."):
                time.sleep(2)  # Simulate API call
                if check_payment_activation(activation_code, user_name):
                    st.success("✅ Kích hoạt thành công! Chuyển hướng đến ứng dụng...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Mã kích hoạt không hợp lệ. Vui lòng kiểm tra lại!")
    
    # Demo section
    st.markdown("---")
    st.markdown("### 🎮 Trải nghiệm bản demo")
    demo_button = st.button("🚀 DÙNG THỬ BẢN DEMO", use_container_width=True)
    
    if demo_button:
        st.session_state.authenticated = True
        st.session_state.user_name = "Người dùng Demo"
        st.rerun()

def main_app():
    """Main application after authentication"""
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title(f"🏠 Chào {st.session_state.user_name}!")
        st.markdown(f"**Phiên làm việc:** {st.session_state.session_id}")
    
    # Main features
    tab1, tab2, tab3 = st.tabs(["📸 Chụp ảnh", "📤 Tải ảnh lên", "ℹ️ Hướng dẫn"])
    
    with tab1:
        st.markdown("### 📷 Chụp ảnh phòng của bạn")
        st.info("Đảm bảo ánh sáng đủ và chụp toàn cảnh phòng")
        
        captured_image = st.camera_input(
            "Chụp ảnh không gian",
            key="camera_input",
            help="Chụp ảnh phòng để phân tích"
        )
        
        if captured_image:
            process_image(captured_image)
    
    with tab2:
        st.markdown("### 📂 Tải ảnh từ thiết bị")
        uploaded_image = st.file_uploader(
            "Chọn ảnh từ thiết bị",
            type=['jpg', 'jpeg', 'png'],
            help="Tải lên ảnh phòng của bạn"
        )
        
        if uploaded_image:
            process_image(uploaded_image)
    
    with tab3:
        st.markdown("### 📝 Hướng dẫn sử dụng")
        st.markdown("""
        <div class="card">
            <h4>🎯 Cách sử dụng hiệu quả:</h4>
            <ol>
                <li><strong>Chụp/Tải ảnh:</strong> Chụp toàn cảnh phòng với ánh sáng tốt</li>
                <li><strong>Phân tích AI:</strong> Hệ thống sẽ tự động nhận diện đồ vật</li>
                <li><strong>Đánh giá:</strong> Xem kết quả phân tích phong thủy và decor</li>
                <li><strong>Cải thiện:</strong> Áp dụng các gợi ý để tối ưu không gian</li>
            </ol>
            
            <h4>🏆 Nguyên tắc phong thủy cơ bản:</h4>
            <ul>
                <li>⚡ <strong>Luồng khí:</strong> Đảm bảo không khí lưu thông tự do</li>
                <li>🌈 <strong>Ánh sáng:</strong> Tận dụng tối đa ánh sáng tự nhiên</li>
                <li>🎯 <strong>Bố cục:</strong> Sắp xếp đồ đạc hợp lý, tránh lộn xộn</li>
                <li>🎨 <strong>Màu sắc:</strong> Cân bằng ngũ hành trong trang trí</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def process_image(image_file):
    """Process uploaded/captured image"""
    with st.spinner("🔄 Đang phân tích hình ảnh..."):
        progress_bar = st.progress(0)
        
        # Simulate processing steps
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
        
        # Convert image
        image = Image.open(image_file)
        
        # Display image
        st.markdown("### 📸 Hình ảnh đã chụp")
        st.image(image, use_container_width=True, caption="Hình ảnh phòng của bạn")
        
        # Analyze with AI
        detected_objects, decor_analysis = analyze_image_with_ai(image)
        
        # Get recommendations
        recommendations = get_recommendations(detected_objects, decor_analysis)
        st.session_state.analysis_results = recommendations
        
        progress_bar.empty()
        st.success("✅ Phân tích hoàn tất!")
    
    # Display results
    st.markdown("### 📊 Kết quả phân tích")
    
    # Summary statistics
    if st.session_state.analysis_results:
        warning_count = len([r for r in st.session_state.analysis_results if r['severity'] == 'warning'])
        suggestion_count = len([r for r in st.session_state.analysis_results if r['severity'] == 'suggestion'])
        success_count = len([r for r in st.session_state.analysis_results if r['severity'] == 'success'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⚠️ Cảnh báo", warning_count)
        with col2:
            st.metric("💡 Gợi ý", suggestion_count)
        with col3:
            st.metric("✅ Đạt yêu cầu", success_count)
        
        # Filter buttons
        st.markdown("### 🎯 Lọc kết quả")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            show_all = st.button("Tất cả", use_container_width=True)
        with col2:
            show_warnings = st.button("Cảnh báo", use_container_width=True)
        with col3:
            show_suggestions = st.button("Gợi ý", use_container_width=True)
        with col4:
            show_success = st.button("Đạt yêu cầu", use_container_width=True)
        
        # Filter logic
        filtered_results = st.session_state.analysis_results
        if show_warnings:
            filtered_results = [r for r in st.session_state.analysis_results if r['severity'] == 'warning']
        elif show_suggestions:
            filtered_results = [r for r in st.session_state.analysis_results if r['severity'] == 'suggestion']
        elif show_success:
            filtered_results = [r for r in st.session_state.analysis_results if r['severity'] == 'success']
        
        # Display recommendations
        st.markdown("### 💎 Đề xuất cải thiện")
        for recommendation in filtered_results:
            display_recommendation_card(recommendation)
        
        # Export option
        st.markdown("---")
        if st.button("📥 Xuất báo cáo chi tiết", use_container_width=True):
            st.info("Tính năng xuất báo cáo chỉ có trong phiên bản Premium!")
    
    # Share button
    st.markdown("---")
    share_col1, share_col2, share_col3 = st.columns([1, 2, 1])
    with share_col2:
        if st.button("📱 Chia sẻ kết quả", use_container_width=True):
            st.success("Liên kết chia sẻ đã được sao chép!")

# Main app flow
if not st.session_state.authenticated:
    landing_page()
else:
    main_app()
    
    # Logout button in sidebar
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_name = ""
            st.session_state.analysis_results = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📞 Hỗ trợ")
        st.info("""
        **Liên hệ hỗ trợ:**
        - Email: support@aidecor.com
        - Hotline: 1900 1234
        - Zalo: 0912 345 678
        """)

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col2:
    st.caption("© 2024 AI Decor & Phong Thủy. Phiên bản 1.0.0")
