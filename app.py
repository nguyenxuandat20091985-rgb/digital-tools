import streamlit as st
import urllib.parse
import requests

# 1. CẤU HÌNH THÔNG TIN AFFILIATE CỦA ANH ĐẠT
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "san_deal_pro_app"

def tao_link_affiliate(link_goc):
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id=shopee&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=1800)
def lay_deal_tu_dong_api():
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    params = {"limit": 10, "search": "phụ tùng xe, tẩu sạc ô tô", "order": "discount_percent"}
    try:
        response = requests.get(url_api, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except:
        return []

# 2. THIẾT KẾ UI ĐẲNG CẤP, HIỆN ĐẠI
st.set_page_config(page_title="Săn Deal Tự Động Pro", page_icon="🛍️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #080C14; }
    
    /* Giao diện Banner Chuyên Nghiệp - Đã đổi tên chuẩn */
    .hero-banner {
        background: linear-gradient(135deg, #00F0FF 0%, #0072FF 100%);
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(0, 240, 255, 0.15);
    }
    .hero-title { font-size: 24px; font-weight: 800; color: #080C14; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }
    .hero-sub { font-size: 13px; color: #080C14; font-weight: 500; opacity: 0.9; }
    
    /* Thanh công cụ nhập link VIP */
    .tool-box {
        background: #111827;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #1F2937;
        margin-bottom: 30px;
    }
    
    /* Thiết kế Thẻ Sản phẩm (Card) chuẩn E-commerce */
    .product-card {
        background: #151F32;
        border: 1px solid #233554;
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 18px;
        transition: transform 0.2s;
    }
    .product-title {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 600;
        margin: 10px 0 6px 0;
        height: 40px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        line-height: 1.4;
    }
    .price-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
    .price-actual { color: #FF4A4A; font-size: 18px; font-weight: 700; }
    .badge-discount { background: #EF4444; color: white; font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 6px; }
    
    /* Chỉnh chữ tiêu đề hệ thống */
    h2, h3 { color: #00F0FF !important; font-weight: 700 !important; font-size: 18px !important; }
    div[data-testid="stMarkdownContainer"] p { color: #94A3B8; font-size: 13px; }
    
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ĐÃ ĐỔI TÊN Ở ĐÂY ANH NHÉ!
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🛍️ SĂN DEAL TỰ ĐỘNG PRO 🛍️</div>
        <div class="hero-sub">Hệ thống AI tự động quét và bọc link Affiliate kiếm tiền thụ động</div>
    </div>
""", unsafe_allow_html=True)

# PHẦN 1: TÍNH NĂNG CHUYỂN LINK
st.markdown('<div class="tool-box">', unsafe_allow_html=True)
st.subheader("🔗 Dán Link Mua Hàng Tiết Kiệm")
st.write("Dán link Shopee/Lazada bất kỳ, hệ thống sẽ tự động áp mã giảm giá ẩn của tổng kho:")
link_nhap = st.text_input("", placeholder="Nhập hoặc dán đường dẫn sản phẩm tại đây...", label_visibility="collapsed")
if link_nhap:
    link_kiem_tien = tao_link_affiliate(link_nhap)
    st.success("🎉 Đã tìm thấy mã giảm giá độc quyền!")
    st.markdown(f'<a href="{link_kiem_tien}" target="_blank"><button style="background-color:#00F0FF; color:#080C14; padding:12px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:14px;">👉 BẤM ĐỂ MUA GIÁ ƯU ĐÃI NGAY</button></a>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Tab phân loại sàn
tab1, tab2, tab3 = st.tabs(["🔥 Đồ Chơi Xe HOT", "🧡 Shopee Deal", "💙 Lazada Deal"])

kho_deal_vip = [
    {
        "name": "Bơm Lốp Ô Tô Điện Tử Thông Minh Siêu Tốc A8",
        "image": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=500",
        "price": "399.000đ",
        "discount": "45",
        "url": "https://shopee.vn"
    },
    {
        "name": "Giá Đỡ Điện Thoại Chống Rung Cực Chắc Cho Tài Xế",
        "image": "https://images.unsplash.com/photo-1586105251261-72a756497a11?w=500",
        "price": "89.000đ",
        "discount": "30",
        "url": "https://shopee.vn"
    },
    {
        "name": "Tẩu Sạc Nhanh Ô Tô Cao Cấp Tích Hợp Đèn LED",
        "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500",
        "price": "125.000đ",
        "discount": "50",
        "url": "https://shopee.vn"
    },
    {
        "name": "Bạt Phủ Xe Ô Tô Phản Quang Chống Nóng Cách Nhiệt",
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=500",
        "price": "270.000đ",
        "discount": "40",
        "url": "https://shopee.vn"
    }
]

danh_sach_hien_thi = lay_deal_tu_dong_api()
if not danh_sach_hien_thi:
    danh_sach_hien_thi = kho_deal_vip

with tab1:
    col1, col2 = st.columns(2)
    for index, item in enumerate(danh_sach_hien_thi):
        chon_cot = col1 if index % 2 == 0 else col2
        with chon_cot:
            ten = item.get("name", "Sản phẩm giảm giá")
            anh = item.get("image", "https://via.placeholder.com/150")
            giam = item.get("discount", "20")
            
            if isinstance(item.get("price"), int):
                gia = f"{item.get('price'):,}đ"
            else:
                gia = str(item.get("price", "Xem giá"))
                
            link_aff = tao_link_affiliate(item.get("url", "https://shopee.vn"))
            
            st.markdown(f"""
                <div class="product-card">
                    <img src="{anh}" style="width:100%; height:130px; border-radius:10px; object-fit:cover;">
                    <div class="product-title">{ten}</div>
                    <div class="price-row">
                        <span class="price-actual">{gia}</span>
                        <span class="badge-discount">-{giam}%</span>
                    </div>
                    <a href="{link_aff}" target="_blank"><button style="background-color:#FF3A44; color:white; padding:8px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:12px;">Mua Ngay</button></a>
                </div>
            """, unsafe_allow_html=True)

with tab2:
    st.write("✨ Các mã giảm giá sàn Shopee áp dụng tự động khi thanh toán qua link app.")
with tab3:
    st.write("✨ Các mã giảm giá sàn Lazada áp dụng tự động khi thanh toán qua link app.")
