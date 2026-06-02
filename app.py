import streamlit as st
import urllib.parse
import requests

# --- CẤU HÌNH HỆ THỐNG ---
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_quantum_mall"

st.set_page_config(page_title="AI QUANTUM MALL - Premium", page_icon="💎", layout="wide")

# --- HÀM TẠO LINK AFFILIATE THÔNG MINH ---
def tao_link_affiliate(link_goc, merchant="shopee"):
    # Kiểm tra nếu đã là link affiliate thì không bọc nữa để tránh lỗi 404
    if any(domain in link_goc for domain in ["shorten.asia", "go.isclix.com", "accesstrade.com.vn"]):
        return link_goc
    
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

# --- HÀM LAY DỮ LIỆU TỰ ĐỘNG (TỐI ƯU 50 SẢN PHẨM) ---
@st.cache_data(ttl=3600)
def lay_deal_tu_dong_api(tu_khoa=""):
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    params = {"limit": 50, "search": tu_khoa if tu_khoa else "điện thoại, gia dụng", "order": "discount_percent"}
    try:
        response = requests.get(url_api, headers=headers, params=params)
        return response.json().get("data", []) if response.status_code == 200 else []
    except: return []

# --- CSS CAO CẤP (GIỮ NGUYÊN STYLE CỦA ANH) ---
st.markdown("""
    <style>
    .stApp { background-color: #060913; }
    .premium-banner { background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%); border: 1px solid #312E81; padding: 30px; border-radius: 24px; text-align: center; margin-bottom: 20px; }
    .mall-card { background: #0F172A; border: 1px solid #1E293B; border-radius: 20px; padding: 15px; margin-bottom: 20px; transition: 0.3s; height: 350px; }
    .mall-card:hover { border-color: #00F0FF; transform: translateY(-5px); }
    .mall-title { color: #F8FAFC; font-size: 14px; font-weight: 600; height: 40px; overflow: hidden; margin: 10px 0; }
    .mall-price { color: #FF3B30; font-size: 18px; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

# --- PHÂN HỆ AI CHĂM SÓC KHÁCH HÀNG ---
def ai_tra_loi(msg):
    msg = msg.lower()
    if "giá" in msg: return "Dạ, sản phẩm đã được AI áp mã giảm giá ẩn, anh/chị nhấn 'Mua Ngay' là có giá tốt nhất ạ!"
    if "hướng dẫn" in msg: return "Anh/chị dán link Shopee/Lazada vào ô 'Trợ lý nhận diện' là hệ thống tự bọc link ưu đãi nhé!"
    return "Dạ, em là AI của Quantum Mall. Em có thể hỗ trợ anh/chị săn deal hoặc giải đáp thắc mắc ạ!"

# --- MENU ĐIỀU HƯỚNG ---
menu = st.sidebar.radio("⚙️ HỆ THỐNG ĐIỀU HÀNH AI", ["🛍️ Sàn TMĐT Ưu Đãi", "🤖 AI CSKH 24/7", "🛡️ Quản Trị Admin"])

if menu == "🛍️ Sàn TMĐT Ưu Đãi":
    st.markdown('<div class="premium-banner"><div style="font-size:30px; color:#00F0FF; font-weight:900;">💎 AI QUANTUM PREMIUM MALL</div></div>', unsafe_allow_html=True)
    
    link_nhap = st.text_input("🔗 Dán link sản phẩm Shopee/Lazada tại đây:")
    if link_nhap:
        st.markdown(f'<a href="{tao_link_affiliate(link_nhap)}" target="_blank"><button style="width:100%; padding:15px; background:#00F0FF; border:none; border-radius:10px; font-weight:bold;">👉 NHẬN ƯU ĐÃI MUA NGAY</button></a>', unsafe_allow_html=True)

    data = lay_deal_tu_dong_api()
    cols = st.columns(3) # Hiển thị dạng lưới 3 cột cho đẹp
    for i, item in enumerate(data):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="mall-card">
                <img src="{item.get('image', '')}" style="width:100%; height:150px; border-radius:14px; object-fit:cover;">
                <div class="mall-title">{item.get('name', 'Sản phẩm')}</div>
                <div class="mall-price">{item.get('price', 'Xem giá')}</div>
                <a href="{tao_link_affiliate(item.get('url', '#'))}" target="_blank"><button style="width:100%; padding:10px; border:none; background:#1E293B; color:white; border-radius:8px; margin-top:10px;">🛒 MUA NGAY</button></a>
            </div>
            """, unsafe_allow_html=True)

elif menu == "🤖 AI CSKH 24/7":
    st.subheader("💬 Trợ lý AI sẵn sàng hỗ trợ")
    q = st.text_input("Anh/chị cần hỏi gì ạ?")
    if q: st.write("AI Quantum:", ai_tra_loi(q))

elif menu == "🛡️ Quản Trị Admin":
    st.subheader("🚀 Công cụ Admin")
    st.write("Hệ thống tự động hóa hoàn toàn. Đang quét 50 deal tốt nhất mỗi giờ.")
