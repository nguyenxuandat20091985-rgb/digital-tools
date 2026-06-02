import streamlit as st
import urllib.parse
import requests

# --- CẤU HÌNH HỆ THỐNG ---
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_quantum_mall"

# CẤU HÌNH GIAO DIỆN
st.set_page_config(page_title="AI QUANTUM MALL - Premium", page_icon="💎", layout="wide")

# --- HÀM BỌC LINK THÔNG MINH (Chống 404) ---
def tao_link_affiliate(link_goc, merchant="shopee"):
    # Kiểm tra nếu đã là link rút gọn thì trả về luôn để tránh lỗi 404
    if any(domain in link_goc for domain in ["shorten.asia", "go.isclix.com", "accesstrade"]):
        return link_goc
    
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

# --- HÀM LẤY DỮ LIỆU TỰ ĐỘNG ---
@st.cache_data(ttl=3600)
def lay_deal_tu_dong_api(tu_khoa=""):
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    params = {"limit": 50, "search": tu_khoa if tu_khoa else "điện thoại, gia dụng, thời trang", "order": "discount_percent"}
    try:
        response = requests.get(url_api, headers=headers, params=params)
        return response.json().get("data", []) if response.status_code == 200 else []
    except: return []

# --- CSS CAO CẤP (Giữ nguyên phong cách anh thích) ---
st.markdown("""
    <style>
    .stApp { background-color: #060913; }
    .mall-card { background: #0F172A; border: 1px solid #1E293B; border-radius: 20px; padding: 15px; margin-bottom: 24px; transition: 0.3s; }
    .mall-card:hover { transform: translateY(-6px); border-color: #00F0FF; }
    .mall-title { color: #F8FAFC; font-size: 14px; font-weight: 600; height: 42px; overflow: hidden; margin: 12px 0; }
    .mall-price { color: #FF3B30; font-size: 18px; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

# --- AI CHĂM SÓC KHÁCH HÀNG ---
def ai_tra_loi(user_msg):
    msg = user_msg.lower()
    if "giá" in msg: return "Dạ, giá sản phẩm trên app đã được em tự động áp mã giảm giá từ tổng kho, anh/chị cứ nhấn 'Mua Ngay' là được ạ!"
    if "hướng dẫn" in msg: return "Anh/chị chỉ cần dán link sản phẩm Shopee vào ô tìm kiếm, em sẽ tự bọc mã Affiliate để anh/chị mua giá tốt nhất!"
    return "Chào anh/chị! Em là AI của Quantum Mall. Em có thể giúp anh/chị tìm sản phẩm hoặc hướng dẫn săn deal ạ."

# --- MENU CHÍNH ---
menu = st.sidebar.radio("⚙️ HỆ THỐNG ĐIỀU HÀNH AI", ["🛍️ Sàn TMĐT Ưu Đãi", "🤖 AI CSKH Tự Động", "🛡️ Admin Console"])

if menu == "🛍️ Sàn TMĐT Ưu Đãi":
    st.markdown("## 💎 AI QUANTUM PREMIUM MALL")
    link = st.text_input("🔗 Dán link Shopee/Lazada tại đây:")
    if link:
        st.markdown(f'<a href="{tao_link_affiliate(link)}" target="_blank"><button style="width:100%; padding:15px; background:#00F0FF; border:none; border-radius:10px; font-weight:bold;">👉 CHUYỂN ĐẾN SÀN MUA GIÁ GIẢM</button></a>', unsafe_allow_html=True)
    
    st.write("---")
    data = lay_deal_tu_dong_api()
    cols = st.columns(2)
    for i, item in enumerate(data):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="mall-card">
                    <img src="{item.get('image', '')}" style="width:100%; height:150px; border-radius:14px; object-fit:cover;">
                    <div class="mall-title">{item.get('name', 'Sản phẩm')}</div>
                    <div class="mall-price">{item.get('price', 'Xem giá')}</div>
                    <a href="{tao_link_affiliate(item.get('url', '#'))}" target="_blank"><button style="width:100%; padding:8px; border:none; background:#1E293B; color:white; border-radius:10px; margin-top:10px;">🛒 Mua Ngay</button></a>
                </div>
            """, unsafe_allow_html=True)

elif menu == "🤖 AI CSKH Tự Động":
    st.subheader("💬 Trợ lý AI CSKH")
    q = st.text_input("Anh/chị cần em giúp gì ạ?")
    if q: st.write("AI Quantum:", ai_tra_loi(q))

elif menu == "🛡️ Admin Console":
    st.subheader("🚀 Công cụ Admin")
    st.info("Hệ thống đang hoạt động với 50 deal cập nhật tự động.")
