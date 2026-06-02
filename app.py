import streamlit as st
import urllib.parse
import requests

# 1. CẤU HÌNH HỆ THỐNG
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_quantum_mall"

def tao_link_affiliate(link_goc, merchant="shopee"):
    # LOGIC CHẶN LINK RÁC: Tránh lặp Affiliate tạo lỗi 404
    if any(x in link_goc for x in ["shorten.asia", "go.isclix.com", "accesstrade"]):
        return link_goc # Trả về link gốc nếu đã là link affiliate
    
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=3600)
def lay_du_lieu_san_pham_lon():
    # Giả lập lấy 50-100 sản phẩm từ API
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}"}
    params = {"limit": 100, "order": "discount_percent"}
    try:
        response = requests.get(url_api, headers=headers, params=params)
        data = response.json().get("data", [])
        return data if data else []
    except:
        return []

# 2. GIAO DIỆN LUXURY
st.set_page_config(page_title="AI QUANTUM MALL", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #060913; }
    .mall-card { background: #0F172A; border: 1px solid #1E293B; border-radius: 20px; padding: 15px; margin-bottom: 20px; }
    .mall-title { color: #F8FAFC; font-size: 13px; font-weight: 600; height: 40px; overflow: hidden; }
    .mall-price { color: #FF3B30; font-size: 18px; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

# 3. PHÂN HỆ KHÁCH HÀNG
if st.sidebar.radio("MENU", ["🛍️ Sàn TMĐT", "🤖 AI CSKH"]) == "🛍️ Sàn TMĐT":
    st.title("💎 AI QUANTUM MALL")
    
    # Khu vực dán link thông minh
    link_input = st.text_input("Dán link sản phẩm (Shopee/Lazada):", placeholder="https://shopee.vn/...")
    if link_input:
        if "shorten.asia" in link_input:
            st.warning("⚠️ Đây đã là link Affiliate, bạn có thể chia sẻ luôn!")
        else:
            final_link = tao_link_affiliate(link_input)
            st.markdown(f'<a href="{final_link}" target="_blank"><button style="width:100%; background:#00F0FF; border:none; padding:10px; border-radius:10px; font-weight:bold;">👉 MUA NGAY VỚI GIÁ GIẢM</button></a>', unsafe_allow_html=True)

    # Hiển thị 50-100 sản phẩm
    products = lay_du_lieu_san_pham_lon()
    cols = st.columns(3)
    for idx, item in enumerate(products):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="mall-card">
                    <img src="{item.get('image', '')}" style="width:100%; height:120px; object-fit:cover; border-radius:10px;">
                    <div class="mall-title">{item.get('name', 'Sản phẩm hot')}</div>
                    <div class="mall-price">{item.get('price', 'Liên hệ')}đ</div>
                </div>
            """, unsafe_allow_html=True)

# 4. AI CSKH TỰ ĐỘNG
else:
    st.subheader("🤖 AI Trợ Lý CSKH 24/7")
    user_query = st.text_input("Khách hàng đang hỏi:")
    if user_query:
        # AI logic mô phỏng
        if "giá" in user_query:
            st.write("🤖 AI: Chào bạn, sản phẩm này đang được trợ lý AI của bên mình tự động áp mã giảm giá tốt nhất thị trường rồi ạ. Bạn nhấn 'Mua ngay' để kiểm tra giá sau giảm nhé!")
        elif "ship" in user_query:
            st.write("🤖 AI: Bên mình hỗ trợ giao hàng toàn quốc, đồng kiểm khi nhận hàng. Bạn yên tâm nhé!")
        else:
            st.write("🤖 AI: Cảm ơn bạn đã quan tâm, bạn có thể dán link sản phẩm vào tab 'Sàn TMĐT' để hệ thống quét ưu đãi nhé!")
