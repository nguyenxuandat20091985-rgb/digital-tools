import streamlit as st
import urllib.parse
import requests

# 1. CẤU HÌNH THÔNG TIN AFFILIATE CỦA ANH ĐẠT (ĐÃ TÍCH HỢP MÃ THẬT)
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  # Mã API Key thật của anh Đạt
UTM_SOURCE = "taxi_promax_app"

def tao_link_affiliate(link_goc):
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id=shopee&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=3600)  # Bộ nhớ đệm 1 tiếng cập nhật deal 1 lần cho mượt app
def lay_deal_tu_dong_api():
    """
    Hàm kết nối trực tiếp API Accesstrade lấy các sản phẩm hot nhất thuộc ngành Xe/Công nghệ
    """
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Content-Type": "application/json"
    }
    # Cấu hình bộ lọc tìm kiếm đồ tài xế hay mua
    params = {
        "limit": 15,
        "search": "sạc dự phòng, giá đỡ điện thoại, bạt phủ xe, tẩu sạc ô tô",
        "order": "discount_percent"
    }
    
    try:
        response = requests.get(url_api, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        return []
    except:
        return []

# 2. GIAO DIỆN CHUYÊN NGHIỆP STYLED BY TAXI PROMAX
st.set_page_config(page_title="Săn Deal Tự Động Pro", page_icon="🛍️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; }
    .main-title { font-size: 24px; font-weight: 800; color: #00E5FF; text-align: center; margin-top: 10px; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }
    .sub-title { font-size: 14px; color: #94A3B8; text-align: center; margin-bottom: 25px; }
    .deal-card { background: linear-gradient(145deg, #1E293B, #111827); padding: 20px; border-radius: 16px; border: 1px solid #334155; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); margin-bottom: 20px; }
    .deal-title { color: #F8FAFC; font-size: 15px; font-weight: 600; margin-top: 0px; margin-bottom: 12px; line-height: 1.4; min-height: 42px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .price-new { color: #FF4D4D; font-weight: 700; font-size: 19px; margin-bottom: 15px; }
    .discount-badge { background-color: #EF4444; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-left: 10px; }
    h3 { color: #00E5FF !important; font-size: 18px !important; font-weight: 700 !important; }
    div[data-testid="stMarkdownContainer"] p { color: #CBD5E1; }
    img { border-radius: 8px; margin-bottom: 12px; object-fit: cover; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛍️ TỔNG HỢP DEAL HOT AUTO 24/7 🛍️</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Hệ thống AI tự động quét và bọc link Affiliate của anh Đạt Nguyễn</div>', unsafe_allow_html=True)

# PHẦN 1: TẠO LINK NHANH
st.subheader("🔗 Tự Tạo Link Giảm Giá Nhanh")
link_nhap = st.text_input("Dán link sản phẩm Shopee / Lazada vào đây:", placeholder="https://shopee.vn/...")
if link_nhap:
    link_kiem_tien = tao_link_affiliate(link_nhap)
    st.success("🎉 Đã bọc link kiếm tiền thành công!")
    st.markdown(f'<a href="{link_kiem_tien}" target="_blank"><button style="background-color:#00E5FF; color:#0B0F19; padding:12px 24px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; font-size:15px; width:100%;">👉 BẤM ĐỂ ĐẾN MUA SẢN PHẨM GIẢM GIÁ</button></a>', unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True)

# PHẦN 2: HIỂN THỊ DEAL THẬT TỰ ĐỘNG TỪ API
st.subheader("🔥 Top Deal Đồ Chơi Xe & Công Nghệ Hot Nhất Hệ Thống")

danh_sach_deal = lay_deal_tu_dong_api()

if not danh_sach_deal:
    st.info("💡 Hệ thống đang kết nối lấy dữ liệu deal thật từ Accesstrade, vui lòng đợi vài giây hoặc tải lại trang.")
else:
    for item in danh_sach_deal:
        ten_sp = item.get("name", "Sản phẩm ưu đãi")
        hinh_anh = item.get("image", "https://via.placeholder.com/150")
        gia_ban = f"{int(item.get('price', 0)):,}đ" if item.get('price') else "Xem giá tại shop"
        link_goc_sp = item.get("url", "")
        phandram_giam = item.get("discount", "0")
        
        link_aff = tao_link_affiliate(link_goc_sp)
        
        st.markdown(f"""
            <div class="deal-card">
                <img src="{hinh_anh}" width="100%" height="160px">
                <div class="deal-title">{ten_sp}</div>
                <div class="price-new">{gia_ban} <span class="discount-badge">-{phandram_giam}%</span></div>
                <a href="{link_aff}" target="_blank"><button style="background-color:#FF4D4D; color:white; padding:10px 15px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:14px;">🛒 Lấy Mã & Mua Ngay</button></a>
            </div>
        """, unsafe_allow_html=True)
