import streamlit as st
import urllib.parse
import requests

# 1. CẤU HÌNH HỆ THỐNG
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_quantum_mall"

def is_affiliate_link(url):
    """Lớp bảo vệ: Tự động kiểm tra xem link đã là Affiliate hay chưa"""
    blocked_domains = ["shorten.asia", "go.isclix.com", "accesstrade"]
    return any(domain in url for domain in blocked_domains)

def tao_link_affiliate(link_goc, merchant="shopee"):
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

# 2. GIAO DIỆN PREMIUM DARK MODE
st.set_page_config(page_title="AI QUANTUM MALL", page_icon="💎", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #060913; }
    .premium-box { background: rgba(15, 23, 42, 0.8); padding: 25px; border-radius: 20px; border: 1px solid #1E293B; }
    h1 { color: #00F0FF !important; text-align: center; }
    .success-text { color: #00F0FF; font-weight: bold; }
    .error-text { color: #FF3B30; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>💎 AI QUANTUM MALL</h1>", unsafe_allow_html=True)

# 3. PHÂN HỆ XỬ LÝ LINK THÔNG MINH
st.markdown('<div class="premium-box">', unsafe_allow_html=True)
st.subheader("🔗 Trợ Lý Tạo Link Affiliate Thông Minh")
link_input = st.text_input("Dán link sản phẩm Shopee/Lazada tại đây:")

if link_input:
    if is_affiliate_link(link_input):
        st.markdown('<p class="error-text">⚠️ Cảnh báo: Đây là link đã là Affiliate rồi! Bạn có thể trực tiếp mang đi đăng bài, không cần qua hệ thống bọc link nữa.</p>', unsafe_allow_html=True)
        st.info(f"Link của bạn: {link_input}")
    else:
        with st.spinner("Đang kết nối API bọc mã giảm giá..."):
            merchant = "lazada" if "lazada.vn" in link_input else "shopee"
            try:
                link_final = tao_link_affiliate(link_input, merchant)
                st.markdown('<p class="success-text">✅ Thành công! Link Affiliate của bạn đã sẵn sàng:</p>', unsafe_allow_html=True)
                st.code(link_final, language="text")
                st.markdown(f'<a href="{link_final}" target="_blank"><button style="background-color:#00F0FF; color:#060913; padding:12px; border-radius:10px; border:none; width:100%; font-weight:bold;">MỞ LINK AFFILIATE NGAY</button></a>', unsafe_allow_html=True)
            except Exception as e:
                st.error("Hệ thống đang bận, vui lòng thử lại sau!")
st.markdown('</div>', unsafe_allow_html=True)

# 4. DANH MỤC DEAL CỐ ĐỊNH (Tối ưu để không load chậm)
st.markdown("---")
st.subheader("🔥 Deal Hot Được Lựa Chọn")
cols = st.columns(2)
# Dùng dữ liệu cứng an toàn để app chạy nhanh
products = [
    {"name": "Tai Nghe Bluetooth 5.3", "price": "450k"},
    {"name": "Robot Hút Bụi Cao Cấp", "price": "3.8tr"},
    {"name": "Nước Hoa Nam Lịch Lãm", "price": "1.2tr"},
    {"name": "Đồng Hồ Thông Minh", "price": "890k"}
]

for i, p in enumerate(products):
    with cols[i%2]:
        st.markdown(f"**{p['name']}**<br>Giá: {p['price']}", unsafe_allow_html=True)
