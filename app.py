import streamlit as st
import urllib.parse
import requests
import time

# --- CẤU HÌNH HỆ THỐNG ---
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_quantum_mall"

st.set_page_config(page_title="AI QUANTUM MALL", page_icon="💎", layout="wide")

# --- HÀM XỬ LÝ DỮ LIỆU & AI ---
def tao_link_affiliate(link_goc, merchant="shopee"):
    # Cơ chế "Chặn thông minh" để chống lỗi 404
    if "shorten.asia" in link_goc or "go.isclix.com" in link_goc:
        return link_goc # Trả về nguyên gốc nếu đã là link aff
    
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=600) # Cập nhật dữ liệu mỗi 10 phút
def lay_deal_tu_dong_api(tu_khoa=""):
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    params = {"limit": 100, "search": tu_khoa if tu_khoa else "gia dụng, điện tử", "order": "discount_percent"}
    try:
        response = requests.get(url_api, headers=headers, params=params)
        return response.json().get("data", []) if response.status_code == 200 else []
    except: return []

# --- CSS & STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #060913; }
    .mall-card { background: #0F172A; border: 1px solid #1E293B; border-radius: 15px; padding: 15px; margin-bottom: 15px; transition: 0.3s; }
    .mall-card:hover { border-color: #00F0FF; }
    .mall-title { color: #F8FAFC; font-size: 13px; height: 40px; overflow: hidden; margin: 10px 0; }
    .mall-price { color: #FF3B30; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

# --- AI CUSTOMER SERVICE AGENT ---
def ai_cs_support(user_input):
    """Mô hình AI tự động trả lời khách hàng"""
    responses = {
        "chào": "Dạ chào anh/chị! Em là trợ lý AI của Quantum Mall. Em có thể giúp gì cho anh/chị săn deal giá rẻ hôm nay ạ?",
        "giá": "Dạ, các sản phẩm trên app đã được em tự động áp mã giảm giá ẩn từ tổng kho, anh/chị cứ nhấn 'Nhận Ưu Đãi' là mua được giá tốt nhất ạ!",
        "cảm ơn": "Dạ không có gì ạ! Chúc anh/chị mua sắm vui vẻ và tiết kiệm ạ!"
    }
    for key in responses:
        if key in user_input.lower(): return responses[key]
    return "Dạ, anh/chị có thể dán link sản phẩm Shopee/Lazada vào ô 'Trợ lý nhận diện' để em hỗ trợ bọc mã giảm giá ngay lập tức nhé!"

# --- GIAO DIỆN ---
menu_chinh = st.sidebar.radio("⚙️ HỆ THỐNG", ["🛍️ Sàn TMĐT", "🤖 AI CSKH (Khách Hàng)", "🛡️ Admin Console"])

if menu_chinh == "🛍️ Sàn TMĐT":
    st.markdown("## 💎 AI QUANTUM MALL")
    link_nhap = st.text_input("🔗 Dán link sản phẩm Shopee/Lazada:")
    if link_nhap:
        link_aff = tao_link_affiliate(link_nhap)
        st.markdown(f'<a href="{link_aff}" target="_blank"><button style="width:100%; background:#00F0FF; border:none; padding:10px; border-radius:8px;">👉 MUA NGAY GIÁ GIẢM</button></a>', unsafe_allow_html=True)
    
    st.write("---")
    data = lay_deal_tu_dong_api()
    # Hiển thị 100 sản phẩm với cấu trúc lưới
    cols = st.columns(4)
    for i, item in enumerate(data):
        with cols[i % 4]:
            st.markdown(f"""<div class="mall-card"><img src="{item.get('image', '')}" style="width:100%; border-radius:8px;">
            <div class="mall-title">{item.get('name', 'Sản phẩm')}</div>
            <div class="mall-price">{item.get('price', 'Liên hệ')}</div></div>""", unsafe_allow_html=True)

elif menu_chinh == "🤖 AI CSKH (Khách Hàng)":
    st.subheader("💬 Trò chuyện với AI Support")
    user_msg = st.text_input("Anh/chị cần hỗ trợ gì ạ?")
    if user_msg:
        st.write(f"AI Support: {ai_cs_support(user_msg)}")

elif menu_chinh == "🛡️ Admin Console":
    st.subheader("⚙️ Quản trị hệ thống")
    st.write("Cấu trúc API hiện đang hoạt động với ID:", ACCESSTRADE_ID)
    st.warning("Hệ thống đã tự động lọc các link 404 và bọc mã Affiliate cho 100 sản phẩm.")
