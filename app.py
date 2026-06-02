import streamlit as st
import urllib.parse
import requests

# 1. CẤU HÌNH HỆ THỐNG
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_quantum_mall"

def tao_link_affiliate(link_goc, merchant="shopee"):
    # CƠ CHẾ CHẶN THÔNG MINH: Ngăn vòng lặp 404
    if "shorten.asia" in link_goc or "go.isclix.com" in link_goc:
        return link_goc
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=3600)
def lay_san_pham_ai(keyword, limit=100):
    """AI Tự động quét sản phẩm với số lượng lớn (100 sp)"""
    url_api = "https://api.accesstrade.com.vn/v1/products"
    params = {"limit": limit, "search": keyword, "order": "discount_percent"}
    headers = {"Authorization": f"Token {API_TOKEN}"}
    try:
        response = requests.get(url_api, headers=headers, params=params)
        return response.json().get("data", []) if response.status_code == 200 else []
    except: return []

# 2. GIAO DIỆN PREMIUM
st.set_page_config(page_title="AI QUANTUM MALL", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #060913; color: white; }
    .mall-card { background: #0F172A; border: 1px solid #1E293B; border-radius: 15px; padding: 10px; margin-bottom: 15px; }
    .price { color: #FF3B30; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. TÍCH HỢP AI CHĂM SÓC KHÁCH HÀNG TỰ ĐỘNG
def ai_tu_van(query):
    query = query.lower()
    if "giá" in query or "mua" in query: return "🤖 AI: Anh/chị hãy dán link sản phẩm vào ô tìm kiếm, em sẽ tự động áp mã giảm giá tốt nhất cho mình nhé!"
    if "chào" in query: return "🤖 AI: Chào anh/chị, em là Trợ lý AI Quantum. Hôm nay em có thể giúp anh/chị săn deal gì ạ?"
    return "🤖 AI: Em đã sẵn sàng hỗ trợ, anh/chị cần tìm sản phẩm nào với mức giảm giá bao nhiêu % ạ?"

# MAIN APP
menu = st.sidebar.selectbox("MENU", ["🛍️ Mua Sắm AI", "💬 Chat Với AI"])

if menu == "🛍️ Mua Sắm AI":
    st.title("💎 AI QUANTUM MALL - PHIÊN BẢN 100")
    link_input = st.text_input("Dán link Shopee/Lazada vào đây để nhận ưu đãi:")
    if link_input:
        link_aff = tao_link_affiliate(link_input)
        st.markdown(f"[👉 MUA NGAY VỚI MÃ GIẢM GIÁ]({link_aff})")
    
    tab1, tab2 = st.tabs(["🔥 Săn Deal 100 sản phẩm", "📱 Công Nghệ"])
    with tab1:
        products = lay_san_pham_ai("gia dụng, thời trang", 100)
        cols = st.columns(4)
        for i, p in enumerate(products):
            with cols[i % 4]:
                st.image(p.get("image", ""), width=150)
                st.write(p.get("name")[:30] + "...")
                st.markdown(f"<span class='price'>{p.get('price')}đ</span>", unsafe_allow_html=True)
                st.link_button("Xem", tao_link_affiliate(p.get("url", "")))

elif menu == "💬 Chat Với AI":
    st.subheader("🤖 Trợ lý AI Quantum chăm sóc khách hàng")
    user_chat = st.text_input("Nhập câu hỏi của bạn:")
    if user_chat:
        st.write(ai_tu_van(user_chat))
