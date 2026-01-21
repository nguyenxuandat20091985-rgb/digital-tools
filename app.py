import streamlit as st
import requests
import json
import time
from PIL import Image
import io
import base64
from datetime import datetime
import uuid
import sqlite3
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Optional
import hashlib
import random

# Page configuration
st.set_page_config(
    page_title="AI Decor & Phong Thủy Pro",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# DATABASE SETUP
# ============================================
@st.cache_resource
def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('decor_phongthuy.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            email TEXT,
            phone TEXT,
            subscription_type TEXT,
            subscription_expiry DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Analysis history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            analysis_id TEXT PRIMARY KEY,
            user_id TEXT,
            image_path TEXT,
            detected_objects TEXT,
            recommendations TEXT,
            feng_shui_score INTEGER,
            decor_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Payment transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            payment_id TEXT PRIMARY KEY,
            user_id TEXT,
            amount REAL,
            currency TEXT,
            payment_method TEXT,
            transaction_id TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Chat history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            chat_id TEXT PRIMARY KEY,
            user_id TEXT,
            message TEXT,
            response TEXT,
            is_user BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Decor templates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decor_templates (
            template_id TEXT PRIMARY KEY,
            style_name TEXT,
            description TEXT,
            color_palette TEXT,
            furniture_list TEXT,
            lighting_suggestions TEXT,
            feng_shui_tips TEXT,
            image_path TEXT,
            difficulty_level TEXT,
            estimated_cost TEXT
        )
    ''')
    
    conn.commit()
    return conn

# Initialize database
DB_CONN = init_database()

# ============================================
# DATA CLASSES
# ============================================
@dataclass
class User:
    user_id: str
    username: str
    email: str
    phone: str
    subscription_type: str

@dataclass
class DecorTemplate:
    template_id: str
    style_name: str
    description: str
    color_palette: List[str]
    furniture_list: List[str]
    lighting_suggestions: str
    feng_shui_tips: str
    image_path: str
    difficulty_level: str
    estimated_cost: str

# ============================================
# CUSTOM CSS FOR MOBILE-FIRST DESIGN
# ============================================
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
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
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
        .premium-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        .payment-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 5px solid #007bff;
        }
        .chat-message {
            padding: 10px 15px;
            border-radius: 18px;
            margin: 5px 0;
            max-width: 80%;
        }
        .user-message {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            margin-left: auto;
        }
        .bot-message {
            background: #f1f3f4;
            color: #333;
            margin-right: auto;
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
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        background-color: #f0f2f6;
    }
    
    /* Card grid for decor templates */
    .template-card {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .template-card:hover {
        border-color: #667eea;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = ""
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'subscription_type' not in st.session_state:
    st.session_state.subscription_type = "free"
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_chat' not in st.session_state:
    st.session_state.current_chat = []
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None

# ============================================
# PAYMENT GATEWAY INTEGRATION (MOCK)
# ============================================
class PaymentGateway:
    """Mock payment gateway for Momo and VNPay"""
    
    @staticmethod
    def create_momo_payment(amount, order_id, description):
        """Create MoMo payment request"""
        return {
            "payment_url": f"https://momo.vn/pay/{order_id}",
            "qr_code": f"data:image/png;base64,mock_qr_code_base64_{order_id}",
            "order_id": order_id,
            "amount": amount,
            "status": "pending"
        }
    
    @staticmethod
    def create_vnpay_payment(amount, order_id, description):
        """Create VNPay payment request"""
        return {
            "payment_url": f"https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?orderId={order_id}",
            "order_id": order_id,
            "amount": amount,
            "status": "pending"
        }
    
    @staticmethod
    def check_payment_status(order_id):
        """Check payment status"""
        # Mock status check
        statuses = ["pending", "success", "failed"]
        return random.choice(statuses)

# ============================================
# AI CHATBOT WITH FENG SHUI KNOWLEDGE
# ============================================
class FengShuiChatbot:
    """AI Chatbot with Feng Shui expertise"""
    
    def __init__(self):
        self.knowledge_base = {
            "phong thủy": {
                "keywords": ["phong thủy", "phongthuy", "tam tài", "ngũ hành", "bát quái"],
                "responses": [
                    "Phong thủy là nghệ thuật sắp xếp không gian sống hài hòa với thiên nhiên.",
                    "Ngũ hành bao gồm: Kim, Mộc, Thủy, Hỏa, Thổ. Mỗi yếu tố có màu sắc và hướng riêng.",
                    "Bát quái đồ giúp xác định vị trí tốt cho từng khu vực trong nhà."
                ]
            },
            "hướng nhà": {
                "keywords": ["hướng nhà", "hướng cửa", "tây tứ trạch", "đông tứ trạch"],
                "responses": [
                    "Hướng nhà nên dựa vào tuổi gia chủ. Tôi có thể tính toán giúp bạn!",
                    "Đông tứ trạch: Đông, Đông Nam, Bắc, Nam. Tây tứ trạch: Tây, Tây Bắc, Tây Nam, Đông Bắc."
                ]
            },
            "màu sắc": {
                "keywords": ["màu sắc", "màu", "màu phong thủy", "ngũ hành màu"],
                "responses": [
                    "Kim: trắng, bạc | Mộc: xanh lá | Thủy: đen, xanh dương | Hỏa: đỏ, tím | Thổ: vàng, nâu",
                    "Chọn màu theo mệnh: Kim hợp vàng/trắng, Mộc hợp xanh/đen, Thủy hợp trắng/xanh, Hỏa hợp xanh/đỏ, Thổ hợp đỏ/vàng"
                ]
            },
            "bố trí phòng": {
                "keywords": ["bố trí", "sắp xếp", "giường", "bàn làm việc", "bếp"],
                "responses": [
                    "Giường nên kê sát tường, không đối diện cửa ra vào.",
                    "Bàn làm việc nên quay lưng vào tường, có tầm nhìn ra cửa.",
                    "Bếp không nên đối diện nhà vệ sinh hoặc dưới cầu thang."
                ]
            },
            "cây cảnh": {
                "keywords": ["cây", "cây cảnh", "cây phong thủy", "thực vật"],
                "responses": [
                    "Cây kim tiền, lưỡi hổ, phát lộc mang lại tài lộc.",
                    "Tránh cây có gai nhọn trong nhà, nên chọn cây lá tròn.",
                    "Cây xanh giúp thanh lọc không khí và cân bằng năng lượng."
                ]
            }
        }
    
    def generate_response(self, user_message, user_data=None):
        """Generate chatbot response based on user message"""
        user_message_lower = user_message.lower()
        
        # Check for greeting
        if any(word in user_message_lower for word in ["xin chào", "hello", "hi", "chào"]):
            return "Xin chào! Tôi là trợ lý AI phong thủy. Tôi có thể giúp gì cho bạn về decor và phong thủy?"
        
        # Check for keywords in knowledge base
        for category, data in self.knowledge_base.items():
            for keyword in data["keywords"]:
                if keyword in user_message_lower:
                    return random.choice(data["responses"])
        
        # Default response
        default_responses = [
            "Tôi có thể giúp bạn về phong thủy, bố trí nội thất, chọn màu sắc, hoặc tính hướng nhà theo tuổi.",
            "Bạn có thể hỏi tôi về: hướng nhà theo tuổi, màu sắc phong thủy, bố trí phòng ngủ, hoặc cây cảnh hợp mệnh.",
            "Để tôi hỗ trợ tốt hơn, bạn có thể cung cấp tuổi của mình và loại phòng muốn tư vấn."
        ]
        
        return random.choice(default_responses)

# ============================================
# DECOR TEMPLATE LIBRARY
# ============================================
class DecorTemplateLibrary:
    """Library of decor templates by style"""
    
    def __init__(self):
        self.templates = [
            DecorTemplate(
                template_id="modern_minimal",
                style_name="Hiện đại Tối giản",
                description="Phong cách hiện đại với đường nét đơn giản, màu sắc trung tính và không gian mở",
                color_palette=["#FFFFFF", "#F5F5F5", "#333333", "#E0E0E0"],
                furniture_list=["Sofa da đơn sắc", "Bàn tròn kính", "Kệ treo tường", "Đèn LED âm trần"],
                lighting_suggestions="Ánh sáng gián tiếp, đèn LED dải, đèn spotlight cho điểm nhấn",
                feng_shui_tips="Giữ không gian thông thoáng, sử dụng gương để mở rộng không gian ảo",
                image_path="assets/templates/modern_minimal.jpg",
                difficulty_level="Dễ",
                estimated_cost="15-30 triệu VNĐ"
            ),
            DecorTemplate(
                template_id="scandinavian",
                style_name="Scandinavian",
                description="Phong cách Bắc Âu ấm áp với gỗ tự nhiên và ánh sáng tự nhiên",
                color_palette=["#F8F9FA", "#FFF8E1", "#4A6572", "#A1887F"],
                furniture_list=["Bàn gỗ nguyên tấm", "Ghế bành lông cừu", "Thảm len", "Kệ sách gỗ"],
                lighting_suggestions="Đèn treo tường, đèn bàn thiết kế đơn giản, tận dụng tối đa ánh sáng tự nhiên",
                feng_shui_tips="Sử dụng vật liệu tự nhiên, thêm cây xanh để cân bằng năng lượng",
                image_path="assets/templates/scandinavian.jpg",
                difficulty_level="Trung bình",
                estimated_cost="20-40 triệu VNĐ"
            ),
            DecorTemplate(
                template_id="industrial",
                style_name="Industrial",
                description="Phong cách công nghiệp với vật liệu thô và chi tiết kim loại",
                color_palette=["#2C3E50", "#7F8C8D", "#BDC3C7", "#ECF0F1"],
                furniture_list=["Bàn gỗ pallet", "Ghế sofa da cũ", "Kệ ống nước", "Đèn treo dây thép"],
                lighting_suggestions="Đèn Edison, đèn treo công nghiệp, ánh sáng vàng ấm",
                feng_shui_tips="Thêm cây xanh để làm mềm không gian, sử dụng gương giảm cảm giác thô cứng",
                image_path="assets/templates/industrial.jpg",
                difficulty_level="Khó",
                estimated_cost="25-50 triệu VNĐ"
            ),
            DecorTemplate(
                template_id="japanese",
                style_name="Nhật Bản",
                description="Phong cách Nhật với sự tối giản và hài hòa với thiên nhiên",
                color_palette=["#F5E6CA", "#8B7355", "#3B2F2F", "#C4B6A6"],
                furniture_list=["Bàn thấp", "Đệm ngồi", "Tủ gỗ shoji", "Bình hoa Ikebana"],
                lighting_suggestions="Đèn giấy washi, đèn tre thấp, ánh sáng dịu nhẹ",
                feng_shui_tips="Sắp xếp theo nguyên tắc Ma (khoảng trống), giữ không gian thanh tịnh",
                image_path="assets/templates/japanese.jpg",
                difficulty_level="Trung bình",
                estimated_cost="18-35 triệu VNĐ"
            ),
            DecorTemplate(
                template_id="bohemian",
                style_name="Bohemian",
                description="Phong cách tự do với màu sắc rực rỡ và họa tiết phong phú",
                color_palette=["#FF6B6B", "#4ECDC4", "#FFD166", "#118AB2"],
                furniture_list=["Ghế lười", "Thảm nhiều màu", "Đệm dựa", "Kệ mở"],
                lighting_suggestions="Đèn Moroccan, đèn chuỗi, nến thơm",
                feng_shui_tips="Cân bằng màu sắc rực rỡ với không gian thoáng, sử dụng chuông gió để năng lượng lưu thông",
                image_path="assets/templates/bohemian.jpg",
                difficulty_level="Dễ",
                estimated_cost="10-25 triệu VNĐ"
            )
        ]
    
    def get_templates_by_style(self, style=None):
        """Get templates filtered by style"""
        if style:
            return [t for t in self.templates if style.lower() in t.style_name.lower()]
        return self.templates
    
    def calculate_feng_shui_compatibility(self, template, birth_year):
        """Calculate Feng Shui compatibility based on birth year"""
        # Simplified compatibility calculation
        elements = {
            "modern_minimal": "Kim",
            "scandinavian": "Mộc",
            "industrial": "Kim",
            "japanese": "Thủy",
            "bohemian": "Hỏa"
        }
        
        # Determine user's element based on birth year
        element_map = {
            "Kim": [1932, 1933, 1940, 1941, 1954, 1955, 1962, 1963, 1970, 1971, 1984, 1985, 1992, 1993],
            "Mộc": [1930, 1931, 1938, 1939, 1950, 1951, 1958, 1959, 1972, 1973, 1980, 1981, 1988, 1989],
            "Thủy": [1936, 1937, 1944, 1945, 1952, 1953, 1966, 1967, 1974, 1975, 1982, 1983, 1996, 1997],
            "Hỏa": [1934, 1935, 1948, 1949, 1956, 1957, 1964, 1965, 1978, 1979, 1986, 1987, 1994, 1995],
            "Thổ": [1930, 1931, 1938, 1939, 1946, 1947, 1960, 1961, 1968, 1969, 1976, 1977, 1990, 1991]
        }
        
        user_element = None
        for element, years in element_map.items():
            if birth_year in years:
                user_element = element
                break
        
        if not user_element:
            user_element = "Mộc"  # Default
        
        template_element = elements.get(template.template_id, "Mộc")
        
        # Element compatibility
        compatibility = {
            ("Kim", "Kim"): 90,
            ("Kim", "Thủy"): 85,
            ("Kim", "Thổ"): 75,
            ("Mộc", "Mộc"): 90,
            ("Mộc", "Hỏa"): 85,
            ("Mộc", "Thủy"): 80,
            ("Thủy", "Thủy"): 90,
            ("Thủy", "Mộc"): 85,
            ("Hỏa", "Hỏa"): 90,
            ("Hỏa", "Thổ"): 85,
            ("Thổ", "Thổ"): 90,
            ("Thổ", "Hỏa"): 80,
        }
        
        return compatibility.get((user_element, template_element), 70)

# ============================================
# HOUSE DIRECTION CALCULATOR
# ============================================
class HouseDirectionCalculator:
    """Calculate auspicious directions based on birth year"""
    
    def __init__(self):
        self.direction_data = {
            "tây_tứ_trạch": {
                "years": [1930, 1931, 1933, 1936, 1939, 1941, 1944, 1947, 1950, 1953, 1956, 1959, 1962, 1965, 1968, 1971, 1974, 1977, 1980, 1983, 1986, 1989, 1992, 1995, 1998, 2001],
                "good_directions": ["Tây", "Tây Nam", "Tây Bắc", "Đông Bắc"],
                "bad_directions": ["Đông", "Đông Nam", "Bắc", "Nam"]
            },
            "đông_tứ_trạch": {
                "years": [1932, 1934, 1935, 1937, 1938, 1940, 1942, 1943, 1945, 1946, 1948, 1949, 1951, 1952, 1954, 1955, 1957, 1958, 1960, 1961, 1963, 1964, 1966, 1967, 1969, 1970, 1972, 1973, 1975, 1976, 1978, 1979, 1981, 1982, 1984, 1985, 1987, 1988, 1990, 1991, 1993, 1994, 1996, 1997, 1999, 2000, 2002],
                "good_directions": ["Đông", "Đông Nam", "Bắc", "Nam"],
                "bad_directions": ["Tây", "Tây Nam", "Tây Bắc", "Đông Bắc"]
            }
        }
    
    def calculate_direction(self, birth_year, gender="male"):
        """Calculate auspicious directions based on birth year and gender"""
        
        # Determine if Tây tứ trạch or Đông tứ trạch
        house_type = None
        for ht, data in self.direction_data.items():
            if birth_year in data["years"]:
                house_type = ht
                break
        
        if not house_type:
            return None
        
        directions = self.direction_data[house_type]
        
        # Detailed direction meanings
        direction_meanings = {
            "Đông": "Sinh Khí - Tài lộc, danh vọng, sức khỏe",
            "Đông Nam": "Thiên Y - Sức khỏe, học vấn",
            "Nam": "Diên Niên - Tình duyên, gia đạo",
            "Bắc": "Phục Vị - Bình an, ổn định",
            "Tây": "Tuyệt Mệnh - Không tốt, nên tránh",
            "Tây Nam": "Ngũ Quỷ - Tranh cãi, thị phi",
            "Tây Bắc": "Lục Sát - Thất bại, mất mát",
            "Đông Bắc": "Họa Hại - Tai ương, bệnh tật"
        }
        
        return {
            "house_type": house_type.replace("_", " ").title(),
            "good_directions": [(d, direction_meanings.get(d, "")) for d in directions["good_directions"]],
            "bad_directions": [(d, direction_meanings.get(d, "")) for d in directions["bad_directions"]],
            "recommendations": self.get_recommendations(house_type)
        }
    
    def get_recommendations(self, house_type):
        """Get recommendations based on house type"""
        recommendations = {
            "tây_tứ_trạch": [
                "Nên chọn nhà có cửa chính hướng Tây, Tây Nam, Tây Bắc hoặc Đông Bắc",
                "Phòng ngủ nên đặt ở hướng tốt tùy theo mục đích sử dụng",
                "Bếp nên quay về hướng tốt của gia chủ"
            ],
            "đông_tứ_trạch": [
                "Nên chọn nhà có cửa chính hướng Đông, Đông Nam, Bắc hoặc Nam",
                "Phòng làm việc nên đặt ở hướng Sinh Khí hoặc Thiên Y",
                "Phòng khách nên đặt ở hướng Diên Niên để gia đình hòa thuận"
            ]
        }
        return recommendations.get(house_type, [])

# ============================================
# USER AUTHENTICATION FUNCTIONS
# ============================================
def register_user(username, email, phone, subscription_type="free"):
    """Register new user in database"""
    user_id = str(uuid.uuid4())
    cursor = DB_CONN.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (user_id, username, email, phone, subscription_type, subscription_expiry)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            username,
            email,
            phone,
            subscription_type,
            datetime.now().date()
        ))
        
        DB_CONN.commit()
        
        # Initialize session state
        st.session_state.user_id = user_id
        st.session_state.user_name = username
        st.session_state.user_email = email
        st.session_state.subscription_type = subscription_type
        st.session_state.authenticated = True
        
        return True
    except Exception as e:
        st.error(f"Registration failed: {str(e)}")
        return False

def save_analysis_history(image_path, detected_objects, recommendations):
    """Save analysis to database"""
    if not st.session_state.user_id:
        return None
    
    analysis_id = str(uuid.uuid4())
    cursor = DB_CONN.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO analysis_history 
            (analysis_id, user_id, image_path, detected_objects, recommendations, feng_shui_score, decor_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis_id,
            st.session_state.user_id,
            image_path,
            json.dumps(detected_objects),
            json.dumps(recommendations),
            calculate_feng_shui_score(recommendations),
            calculate_decor_score(recommendations)
        ))
        
        DB_CONN.commit()
        return analysis_id
    except Exception as e:
        st.error(f"Failed to save analysis: {str(e)}")
        return None

def get_user_history():
    """Get user's analysis history"""
    if not st.session_state.user_id:
        return []
    
    cursor = DB_CONN.cursor()
    cursor.execute('''
        SELECT analysis_id, image_path, created_at, feng_shui_score, decor_score
        FROM analysis_history
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 10
    ''', (st.session_state.user_id,))
    
    return cursor.fetchall()

# ============================================
# HELPER FUNCTIONS
# ============================================
def calculate_feng_shui_score(recommendations):
    """Calculate Feng Shui score from recommendations"""
    if not recommendations:
        return 0
    
    total = len(recommendations)
    good = sum(1 for r in recommendations if r.get('severity') == 'success')
    
    return int((good / total) * 100) if total > 0 else 0

def calculate_decor_score(recommendations):
    """Calculate decor score from recommendations"""
    if not recommendations:
        return 0
    
    # Simplified decor scoring
    base_score = 70
    adjustments = {
        'warning': -10,
        'suggestion': 0,
        'success': 15
    }
    
    for rec in recommendations:
        base_score += adjustments.get(rec.get('severity', 'suggestion'), 0)
    
    return max(0, min(100, base_score))

# ============================================
# MAIN APPLICATION COMPONENTS
# ============================================
def landing_page():
    """Display landing/payment page"""
    st.title("🏠 AI Decor & Phong Thủy Pro")
    st.markdown("### Chào mừng đến với trợ lý AI thông minh cho không gian sống của bạn!")
    
    # Feature showcase
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
            <h4>🔮 Phong Thủy</h4>
            <p>Phân tích chuyên sâu theo ngũ hành</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4>🎨 Decor</h4>
            <p>Gợi ý theo xu hướng hiện đại</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h4>🤖 AI Chat</h4>
            <p>Tư vấn 24/7 với chuyên gia AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Registration Form
    st.markdown("### 📝 Đăng ký tài khoản")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Họ tên*", placeholder="Nguyễn Văn A")
            email = st.text_input("Email*", placeholder="example@email.com")
        with col2:
            phone = st.text_input("Số điện thoại*", placeholder="0912 345 678")
            birth_year = st.number_input("Năm sinh*", min_value=1900, max_value=2024, value=1990)
        
        subscription = st.selectbox(
            "Gói đăng ký*",
            ["Miễn phí (Demo)", "Cơ bản - 50,000đ/30 ngày", "Premium - 100,000đ/30 ngày", "VIP - 200,000đ/60 ngày"]
        )
        
        submitted = st.form_submit_button("🎯 ĐĂNG KÝ NGAY", type="primary")
        
        if submitted:
            if all([username, email, phone]):
                if register_user(username, email, phone, subscription):
                    st.success("✅ Đăng ký thành công! Đang chuyển hướng...")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("Vui lòng điền đầy đủ thông tin bắt buộc (*)")
    
    # Payment Information (for manual payment)
    st.markdown("---")
    st.markdown("### 💳 Thanh toán thủ công (nếu cần)")
    
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
        - Nội dung: KICHHOAT [Tên đăng ký]
        - Sau khi chuyển khoản, vui lòng liên hệ để nhận mã kích hoạt
        - Hỗ trợ 24/7 qua Zalo: 0912 345 678
        """)

def main_app():
    """Main application after authentication"""
    
    # Initialize chatbot and calculators
    chatbot = FengShuiChatbot()
    direction_calculator = HouseDirectionCalculator()
    template_library = DecorTemplateLibrary()
    payment_gateway = PaymentGateway()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.caption(f"📧 {st.session_state.user_email}")
        st.caption(f"🎫 Gói: {st.session_state.subscription_type}")
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Chức năng chính",
            ["🏠 Trang chủ", "📸 Phân tích ảnh", "💬 Chatbot AI", "📚 Mẫu Decor", "🧭 Xem hướng nhà", "📊 Lịch sử", "💳 Nâng cấp"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_id = ""
            st.session_state.user_name = ""
            st.session_state.user_email = ""
            st.rerun()
    
    # Main content area
    if page == "🏠 Trang chủ":
        show_dashboard()
    elif page == "📸 Phân tích ảnh":
        show_image_analysis()
    elif page == "💬 Chatbot AI":
        show_chatbot(chatbot)
    elif page == "📚 Mẫu Decor":
        show_decor_templates(template_library)
    elif page == "🧭 Xem hướng nhà":
        show_direction_calculator(direction_calculator)
    elif page == "📊 Lịch sử":
        show_history()
    elif page == "💳 Nâng cấp":
        show_payment_upgrade(payment_gateway)

def show_dashboard():
    """Show main dashboard"""
    st.title("🏠 Trang chủ")
    
    # Quick actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📸 Phân tích ảnh", use_container_width=True):
            st.switch_page("main_app")
    with col2:
        if st.button("💬 Hỏi AI", use_container_width=True):
            st.switch_page("main_app")
    with col3:
        if st.button("📚 Mẫu Decor", use_container_width=True):
            st.switch_page("main_app")
    
    # Recent activity
    st.markdown("### 📈 Hoạt động gần đây")
    history = get_user_history()
    
    if history:
        for item in history[:3]:
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <p><strong>Phân tích:</strong> {item[1]}</p>
                    <p><strong>Thời gian:</strong> {item[2]}</p>
                    <p><strong>Điểm Phong Thủy:</strong> {item[3]} | <strong>Điểm Decor:</strong> {item[4]}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Chưa có hoạt động nào. Hãy bắt đầu bằng cách phân tích ảnh phòng của bạn!")

def show_image_analysis():
    """Show image analysis interface"""
    st.title("📸 Phân tích ảnh phòng")
    
    tab1, tab2 = st.tabs(["📷 Chụp ảnh", "📁 Tải ảnh lên"])
    
    with tab1:
        st.markdown("### Chụp ảnh trực tiếp")
        captured_image = st.camera_input("Chụp ảnh phòng của bạn", key="camera_capture")
        if captured_image:
            process_image_analysis(captured_image)
    
    with tab2:
        st.markdown("### Tải ảnh từ thiết bị")
        uploaded_image = st.file_uploader(
            "Chọn ảnh phòng",
            type=['jpg', 'jpeg', 'png', 'heic'],
            help="Tải lên ảnh phòng bạn muốn phân tích"
        )
        if uploaded_image:
            process_image_analysis(uploaded_image)

def process_image_analysis(image_file):
    """Process image for analysis"""
    with st.spinner("🔄 Đang phân tích hình ảnh với AI..."):
        progress_bar = st.progress(0)
        
        # Simulate AI processing
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        # Load image
        image = Image.open(image_file)
        
        # Display results
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Hình ảnh của bạn", use_container_width=True)
        
        with col2:
            st.markdown("### 🔍 Phát hiện vật thể")
            
            # Mock detected objects
            detected_objects = [
                {"name": "Giường", "confidence": 0.95, "status": "✅ Đã phát hiện"},
                {"name": "Cửa sổ", "confidence": 0.88, "status": "✅ Đã phát hiện"},
                {"name": "Bàn làm việc", "confidence": 0.75, "status": "✅ Đã phát hiện"},
                {"name": "Gương", "confidence": 0.65, "status": "⚠️ Mờ nhạt"},
                {"name": "Tủ quần áo", "confidence": 0.92, "status": "✅ Đã phát hiện"}
            ]
            
            for obj in detected_objects:
                st.markdown(f"- **{obj['name']}**: {obj['status']} ({obj['confidence']*100:.0f}%)")
        
        # Generate recommendations
        st.markdown("### 💎 Đề xuất cải thiện")
        
        recommendations = [
            {
                "category": "Phong Thủy",
                "object": "Giường",
                "rule": "Đầu giường hướng ra cửa",
                "severity": "warning",
                "description": "Đầu giường đang hướng thẳng ra cửa, gây mất ngủ",
                "suggestion": "Xoay giường 90 độ để đầu giường dựa vào tường"
            },
            {
                "category": "Decor",
                "object": "Màu sắc",
                "rule": "Cân bằng màu sắc",
                "severity": "suggestion",
                "description": "Phòng sử dụng quá nhiều màu lạnh",
                "suggestion": "Thêm điểm nhấn màu ấm (vàng, cam, nâu)"
            },
            {
                "category": "Phong Thủy",
                "object": "Cửa sổ",
                "rule": "Ánh sáng tự nhiên",
                "severity": "success",
                "description": "Cửa sổ đón đủ ánh sáng tự nhiên",
                "suggestion": "Tiếp tục giữ rèm cửa mở vào ban ngày"
            }
        ]
        
        for rec in recommendations:
            display_recommendation_card(rec)
        
        # Save to history
        if st.button("💾 Lưu phân tích", use_container_width=True):
            analysis_id = save_analysis_history(
                "uploaded_image.jpg",
                detected_objects,
                recommendations
            )
            if analysis_id:
                st.success(f"✅ Đã lưu phân tích #{analysis_id[:8]}")
        
        progress_bar.empty()

def display_recommendation_card(recommendation):
    """Display recommendation card"""
    severity_config = {
        "warning": {"icon": "⚠️", "color": "#ff6b6b"},
        "suggestion": {"icon": "💡", "color": "#ffd93d"},
        "success": {"icon": "✅", "color": "#6bce75"}
    }
    
    config = severity_config.get(recommendation['severity'], severity_config['suggestion'])
    
    st.markdown(f"""
    <div class="card" style="border-left: 5px solid {config['color']};">
        <div style="display: flex; align-items: center; gap: 10px;">
            <h4 style="margin: 0; color: {config['color']};">{config['icon']} {recommendation['category']}</h4>
            <span style="background: {config['color']}20; color: {config['color']}; padding: 2px 8px; border-radius: 10px; font-size: 12px;">
                {recommendation['object']}
            </span>
        </div>
        <p><strong>{recommendation['rule']}</strong></p>
        <p>{recommendation['description']}</p>
        <p><em>💡 {recommendation['suggestion']}</em></p>
    </div>
    """, unsafe_allow_html=True)

def show_chatbot(chatbot):
    """Show AI chatbot interface"""
    st.title("💬 Chatbot AI Phong Thủy")
    
    st.info("""
    🤖 Tôi là trợ lý AI chuyên về Phong Thủy và Decor. 
    Tôi có thể giúp bạn về: hướng nhà, màu sắc, bố trí nội thất, cây cảnh phong thủy.
    """)
    
    # Chat container
    chat_container = st.container(height=400, border=True)
    
    with chat_container:
        for chat in st.session_state.current_chat:
            if chat["is_user"]:
                st.markdown(f"""
                <div style="text-align: right; margin: 10px 0;">
                    <div class="chat-message user-message">
                        {chat["message"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="text-align: left; margin: 10px 0;">
                    <div class="chat-message bot-message">
                        {chat["message"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Quick questions
    st.markdown("### 💡 Câu hỏi nhanh")
    col1, col2, col3 = st.columns(3)
    
    quick_questions = [
        ("Hướng nhà tốt cho tuổi tôi?", "direction"),
        ("Màu sắc hợp mệnh Thổ?", "color"),
        ("Cách bố trí phòng ngủ?", "bedroom"),
        ("Cây cảnh phong thủy?", "plants"),
        ("Ngũ hành là gì?", "elements"),
        ("Cải tạo nhà cũ?", "renovation")
    ]
    
    for idx, (question, key) in enumerate(quick_questions):
        if idx < 3:
            with [col1, col2, col3][idx]:
                if st.button(question, use_container_width=True):
                    response = chatbot.generate_response(key)
                    st.session_state.current_chat.append({"message": question, "is_user": True})
                    st.session_state.current_chat.append({"message": response, "is_user": False})
                    st.rerun()
    
    # Chat input
    user_input = st.chat_input("Nhập câu hỏi của bạn...")
    
    if user_input:
        # Add user message
        st.session_state.current_chat.append({"message": user_input, "is_user": True})
        
        # Generate AI response
        with st.spinner("Đang suy nghĩ..."):
            time.sleep(1)
            response = chatbot.generate_response(user_input)
            st.session_state.current_chat.append({"message": response, "is_user": False})
        
        st.rerun()

def show_decor_templates(template_library):
    """Show decor template library"""
    st.title("📚 Thư viện mẫu Decor")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        style_filter = st.selectbox(
            "Lọc theo phong cách",
            ["Tất cả", "Hiện đại", "Scandinavian", "Industrial", "Nhật Bản", "Bohemian"]
        )
    
    with col2:
        difficulty_filter = st.selectbox(
            "Độ khó",
            ["Tất cả", "Dễ", "Trung bình", "Khó"]
        )
    
    with col3:
        cost_filter = st.selectbox(
            "Ngân sách",
            ["Tất cả", "Dưới 20tr", "20-40tr", "Trên 40tr"]
        )
    
    # Show templates
    templates = template_library.get_templates_by_style(
        None if style_filter == "Tất cả" else style_filter
    )
    
    # Apply additional filters
    if difficulty_filter != "Tất cả":
        templates = [t for t in templates if t.difficulty_level == difficulty_filter]
    
    if cost_filter != "Tất cả":
        cost_map = {
            "Dưới 20tr": lambda x: "15" in x.estimated_cost or "10" in x.estimated_cost,
            "20-40tr": lambda x: "20" in x.estimated_cost or "30" in x.estimated_cost,
            "Trên 40tr": lambda x: "40" in x.estimated_cost or "50" in x.estimated_cost
        }
        templates = [t for t in templates if cost_map[cost_filter](t)]
    
    if not templates:
        st.info("Không tìm thấy mẫu nào phù hợp với bộ lọc.")
        return
    
    # Display templates in a grid
    for template in templates:
        with st.expander(f"🎨 {template.style_name} - {template.difficulty_level} - {template.estimated_cost}"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Placeholder for template image
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {template.color_palette[0]}, {template.color_palette[2]}); 
                            height: 200px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <h3 style="color: white;">{template.style_name}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**Mô tả:** {template.description}")
                st.markdown(f"**Bảng màu:** {', '.join(template.color_palette)}")
                st.markdown(f"**Nội thất chính:** {', '.join(template.furniture_list[:3])}...")
                st.markdown(f"**Ánh sáng:** {template.lighting_suggestions}")
                st.markdown(f"**Mẹo Phong Thủy:** {template.feng_shui_tips}")
                
                # Compatibility check
                if st.button(f"Kiểm tra hợp mệnh", key=f"check_{template.template_id}"):
                    birth_year = st.number_input("Nhập năm sinh của bạn", min_value=1900, max_value=2024, value=1990)
                    score = template_library.calculate_feng_shui_compatibility(template, birth_year)
                    st.success(f"💫 Độ tương hợp: {score}%")
                
                if st.button(f"Áp dụng mẫu này", key=f"apply_{template.template_id}"):
                    st.session_state.selected_template = template
                    st.success(f"Đã chọn mẫu {template.style_name}!")

def show_direction_calculator(calculator):
    """Show house direction calculator"""
    st.title("🧭 Tính hướng nhà theo tuổi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        birth_year = st.number_input(
            "Năm sinh của bạn",
            min_value=1900,
            max_value=2024,
            value=1990,
            help="Nhập năm sinh dương lịch"
        )
        
        gender = st.radio(
            "Giới tính",
            ["Nam", "Nữ"],
            horizontal=True
        )
        
        if st.button("🔮 Tính toán hướng nhà", type="primary", use_container_width=True):
            result = calculator.calculate_direction(birth_year, gender.lower())
            
            if result:
                st.session_state.direction_result = result
                st.rerun()
    
    with col2:
        if 'direction_result' in st.session_state:
            result = st.session_state.direction_result
            
            st.markdown(f"### 📊 Kết quả: {result['house_type']}")
            
            st.markdown("#### 🟢 Hướng tốt:")
            for direction, meaning in result['good_directions']:
                st.markdown(f"- **{direction}**: {meaning}")
            
            st.markdown("#### 🔴 Hướng xấu:")
            for direction, meaning in result['bad_directions']:
                st.markdown(f"- **{direction}**: {meaning}")
            
            st.markdown("#### 💡 Khuyến nghị:")
            for rec in result['recommendations']:
                st.markdown(f"- {rec}")
            
            # Visual compass
            st.markdown("### 🧭 La bàn hướng nhà")
            directions = ["Bắc", "Đông Bắc", "Đông", "Đông Nam", "Nam", "Tây Nam", "Tây", "Tây Bắc"]
            
            compass_html = """
            <div style="text-align: center; padding: 20px;">
                <div style="position: relative; width: 300px; height: 300px; margin: 0 auto; 
                            background: radial-gradient(circle, #f8f9fa, #e9ecef); border-radius: 50%;">
            """
            
            for i, direction in enumerate(directions):
                angle = i * 45
                rad = angle * 3.14159 / 180
                x = 150 + 120 * math.sin(rad)
                y = 150 - 120 * math.cos(rad)
                
                is_good = any(direction in good[0] for good in result['good_directions'])
                is_bad = any(direction in bad[0] for bad in result['bad_directions'])
                
                color = "#28a745" if is_good else "#dc3545" if is_bad else "#6c757d"
                weight = "bold" if is_good or is_bad else "normal"
                
                compass_html += f"""
                <div style="position: absolute; left: {x}px; top: {y}px; transform: translate(-50%, -50%);
                            color: {color}; font-weight: {weight}; font-size: 14px;">
                    {direction}
                </div>
                """
            
            compass_html += """
                <div style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
                            width: 20px; height: 20px; background: #ff6b6b; border-radius: 50%;">
                </div>
            </div>
            </div>
            """
            
            st.markdown(compass_html, unsafe_allow_html=True)

def show_history():
    """Show user's analysis history"""
    st.title("📊 Lịch sử phân tích")
    
    history = get_user_history()
    
    if not history:
        st.info("Chưa có phân tích nào được lưu.")
        return
    
    for idx, item in enumerate(history):
        with st.expander(f"Phân tích #{idx+1} - {item[2]}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Mã phân tích:** {item[0]}")
                st.markdown(f"**Ảnh:** {item[1]}")
                st.markdown(f"**Thời gian:** {item[2]}")
            
            with col2:
                st.metric("Phong Thủy", f"{item[3]}%")
                st.metric("Decor", f"{item[4]}%")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Xem chi tiết", key=f"view_{item[0]}"):
                    st.info("Chi tiết phân tích đang được tải...")
            with col2:
                if st.button("📥 Xuất PDF", key=f"export_{item[0]}"):
                    st.success("PDF đang được tạo...")
            with col3:
                if st.button("🗑️ Xóa", key=f"delete_{item[0]}"):
                    st.warning("Tính năng xóa đang được phát triển")

def show_payment_upgrade(payment_gateway):
    """Show payment and upgrade options"""
    st.title("💳 Nâng cấp gói dịch vụ")
    
    # Subscription plans
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🎯 Cơ bản</h3>
            <h2>50,000đ</h2>
            <p>/ 30 ngày</p>
            <hr>
            <p>✅ 10 phân tích/ngày</p>
            <p>✅ Chatbot cơ bản</p>
            <p>❌ Không lưu lịch sử</p>
            <p>❌ Không xuất PDF</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Chọn gói Cơ bản", key="basic_plan", use_container_width=True):
            st.session_state.selected_plan = "basic"
    
    with col2:
        st.markdown("""
        <div class="card premium-card">
            <h3>⭐ Premium</h3>
            <h2>100,000đ</h2>
            <p>/ 30 ngày</p>
            <hr>
            <p>✅ Không giới hạn phân tích</p>
            <p>✅ Chatbot nâng cao</p>
            <p>✅ Lưu lịch sử 100 bài</p>
            <p>✅ Xuất PDF</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Chọn gói Premium", key="premium_plan", use_container_width=True, type="primary"):
            st.session_state.selected_plan = "premium"
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>👑 VIP</h3>
            <h2>200,000đ</h2>
            <p>/ 60 ngày</p>
            <hr>
            <p>✅ Tất cả tính năng Premium</p>
            <p>✅ Tư vấn 1-1 với chuyên gia</p>
            <p>✅ Thiết kế 3D phòng</p>
            <p>✅ Ưu tiên hỗ trợ 24/7</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Chọn gói VIP", key="vip_plan", use_container_width=True):
            st.session_state.selected_plan = "vip"
    
    # Payment methods
    if 'selected_plan' in st.session_state:
        st.markdown("---")
        st.markdown(f"### 💰 Thanh toán gói {st.session_state.selected_plan.upper()}")
        
        payment_method = st.radio(
            "Chọn phương thức thanh toán",
            ["MoMo", "VNPay", "Chuyển khoản ngân hàng", "Thẻ quốc tế (Visa/Mastercard)"],
            horizontal=True
        )
        
        order_id = f"ORDER_{st.session_state.user_id[:8]}_{int(time.time())}"
        
        if payment_method == "MoMo":
            if st.button("Thanh toán bằng MoMo", use_container_width=True, type="primary"):
                payment = payment_gateway.create_momo_payment(
                    amount=100000 if st.session_state.selected_plan == "premium" else 50000,
                    order_id=order_id,
                    description=f"Upgrade to {st.session_state.selected_plan}"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Mã đơn hàng:** {order_id}")
                    st.info(f"**Số tiền:** {payment['amount']:,.0f} VNĐ")
                
                with col2:
                    # QR code display
                    st.markdown("**Quét QR Code để thanh toán:**")
                    # In production, you would display the actual QR code
                    st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + payment['payment_url'])
                    
                    st.markdown(f"[🔗 Mở MoMo App]({payment['payment_url']})")
        
        elif payment_method == "VNPay":
            if st.button("Thanh toán bằng VNPay", use_container_width=True, type="primary"):
                payment = payment_gateway.create_vnpay_payment(
                    amount=100000 if st.session_state.selected_plan == "premium" else 50000,
                    order_id=order_id,
                    description=f"Upgrade to {st.session_state.selected_plan}"
                )
                
                st.info(f"**Mã đơn hàng:** {order_id}")
                st.info(f"**Số tiền:** {payment['amount']:,.0f} VNĐ")
                st.markdown(f"[🔗 Chuyển đến VNPay]({payment['payment_url']})")
        
        elif payment_method == "Chuyển khoản ngân hàng":
            st.markdown("""
            <div class="payment-info">
                <h4>Thông tin chuyển khoản:</h4>
                <p>🏦 Ngân hàng: BIDV</p>
                <p>📞 Số tài khoản: 4430269669</p>
                <p>👤 Chủ tài khoản: NGUYỄN XUÂN ĐẠT</p>
                <p>💬 Nội dung: KICHHOAT {tên bạn} {mã đơn hàng}</p>
                <p>💰 Số tiền: {số tiền}</p>
            </div>
            """, unsafe_allow_html=True)
            
            activation_code = st.text_input("Nhập mã kích hoạt sau khi chuyển khoản")
            if st.button("Xác nhận mã kích hoạt", use_container_width=True):
                st.success("✅ Kích hoạt thành công! Tài khoản đã được nâng cấp.")

# ============================================
# MAIN APPLICATION FLOW
# ============================================
import math  # Add this import at the top

def main():
    """Main application flow"""
    if not st.session_state.authenticated:
        landing_page()
    else:
        main_app()
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption("© 2024 AI Decor & Phong Thủy Pro. Phiên bản 2.0.0")
        st.caption("📞 Hotline: 1900 1234 | 📧 Email: support@aidecorpro.com")

if __name__ == "__main__":
    main()
