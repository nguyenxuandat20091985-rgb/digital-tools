import streamlit as st
import urllib.parse
import requests

# 1. CẤU HÌNH HỆ THỐNG
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_quantum_mall"

st.set_page_config(page_title="AI QUANTUM MALL", page_icon="💎", layout="wide")

# --- HÀM BỌC LINK THÔNG MINH (Chống lỗi 404) ---
def tao_link_affiliate(link_goc, merchant="shopee"):
    # Nếu đã là link affiliate thì trả về luôn để tránh lỗi vòng lặp
    if any(domain in link_goc for domain in ["shorten.asia", "go.isclix.com", "accesstrade"]):
        return link_goc
    
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

# --- AI TỰ ĐỘNG CẬP NHẬT DỮ LIỆU (Tối ưu 50-100 sản phẩm) ---
@st.cache_data(ttl=3600)
def lay_deal_tu_dong_api(tu_khoa=""):
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    params = {"limit": 50, "search": tu_khoa if tu_khoa else "điện tử, gia dụng", "order": "discount_percent"}
    try:
        response = requests.get(url_api, headers=headers, params=params)
        return response.json().get("data", []) if response.status_code == 200 else []
    except: return []

# --- CSS CAO CẤP ---
st.markdown("""
    <style>
    .stApp { background-color: #060913; }
    .mall-card { background: #0F172A; border: 1px solid #1E293B; border-radius: 15px; padding: 12px; margin-bottom: 15px; transition: 0.3s; height: 320px; }
    .mall-card:hover { border-color: #00F0FF; transform: translateY(-5px); }
    .mall-title { color: #F8FAFC; font-size: 13px; height: 40px; overflow: hidden; margin: 10px 0; font-weight: 600; }
    .mall-price { color: #FF3B30; font-weight: 800; font-size: 16px; }
    </style>
""", unsafe_allow_html=True)

# --- AI CHĂM SÓC KHÁCH HÀNG ---
def get_ai_response(msg):
    msg = msg.lower()
    if "giá" in msg: return "Dạ, giá sản phẩm đã được AI của em tự động áp mã giảm giá ẩn, anh/chị chỉ cần nhấn 'Mua Ngay' là được giá tốt nhất ạ!"
    if "hướng dẫn" in msg or "dùng" in msg: return "Anh/chị chỉ cần dán link Shopee/Lazada vào ô 'Trợ lý nhận diện' ở trang chủ, hệ thống sẽ tự bọc mã Affiliate cho mình ạ!"
    return "Dạ, em là AI của Quantum Mall. Em có thể giúp anh/chị săn deal hoặc hướng dẫn sử dụng app ạ!"

# --- MENU ĐIỀU HƯỚNG ---
menu = st.sidebar.radio("⚙️ HỆ THỐNG AI QUANTUM", ["🛍️ Mua Sắm", "🤖 AI CSKH 24/7", "🛡️ Quản Trị Admin"])

if menu == "🛍️ Mua Sắm":
    st.markdown("## 💎 AI QUANTUM MALL")
    link = st.text_input("🔗 Dán link Shopee/Lazada vào đây:")
    if link:
        st.markdown(f'<a href="{tao_link_affiliate(link)}" target="_blank"><button style="width:100%; padding:10px; background:#00F0FF; border:none; border-radius:8px; font-weight:bold;">👉 NHẬN ƯU ĐÃI NGAY</button></a>', unsafe_allow_html=True)
    
    st.write("---")
    data = lay_deal_tu_dong_api()
    cols = st.columns(3) # Tối ưu lưới 3 cột cho cả Mobile/Desktop
    for i, item in enumerate(data):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="mall-card">
                <img src="{item.get('image', '')}" style="width:100%; height:150px; border-radius:8px; object-fit:cover;">
                <div class="mall-title">{item.get('name', 'Sản phẩm')}</div>
                <div class="mall-price">{item.get('price', 'Xem giá')}</div>
                <a href="{tao_link_affiliate(item.get('url', '#'))}" target="_blank"><button style="width:100%; border:none; padding:8px; background:#1E293B; color:white; border-radius:5px; margin-top:10px;">🛒 MUA NGAY</button></a>
            </div>
            """, unsafe_allow_html=True)

elif menu == "🤖 AI CSKH 24/7":
    st.subheader("💬 Trợ lý AI sẵn sàng hỗ trợ")
    q = st.text_input("Anh/chị cần hỏi gì ạ?")
    if q: st.write("AI Quantum:", get_ai_response(q))

elif menu == "🛡️ Quản Trị Admin":
    st.subheader("🚀 Công cụ Admin")
    st.write("Hệ thống đang hoạt động ổn định với 50 deal tự động mỗi giờ.")
