import streamlit as st
import urllib.parse
import requests

# 1. CẤU HÌNH THÔNG TIN AFFILIATE CỦA ANH ĐẠT
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "sandeal_pro_app"

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

# 2. THIẾT KẾ UI/UX CHUYÊN NGHIỆP CẤP CAO
st.set_page_config(page_title="Săn Deal Tự Động Pro", page_icon="🛍️", layout="wide")

st.markdown("""
    <style>
    /* Nền tối sâu tạo độ nổi bật cho sản phẩm */
    .stApp { background-color: #0F172A; }
    
    /* Giao diện Banner Gradient Luxury */
    .hero-banner {
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
        padding: 35px 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(255, 65, 108, 0.25);
    }
    .hero-title { font-size: 26px; font-weight: 800; color: #FFFFFF; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    .hero-sub { font-size: 13px; color: #FFFFFF; font-weight: 400; opacity: 0.95; }
    
    /* Khung nhập link bo góc mịn màng */
    .tool-box {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 35px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Định dạng thanh nhập liệu Text Input của Streamlit cho đẹp hơn */
    div[data-testid="stTextInput"] input {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #FF4B2B !important;
        box-shadow: 0 0 0 2px rgba(255, 75, 43, 0.2) !important;
    }
    
    /* Thẻ Sản phẩm phong cách Kính Mờ cao cấp */
    .product-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    .product-title {
        color: #F1F5F9;
        font-size: 14.5px;
        font-weight: 600;
        margin: 12px 0 8px 0;
        height: 44px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        line-height: 1.5;
    }
    .price-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px; }
    .price-actual { color: #F43F5E; font-size: 19px; font-weight: 700; letter-spacing: -0.5px; }
    .badge-discount { background: #10B981; color: white; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 8px; }
    
    /* Nút bấm mua hàng bo tròn mượt mà */
    .btn-buy { background: linear-gradient(90deg, #FF416C, #FF4B2B); color: white; padding: 12px; border: none; border-radius: 12px; cursor:pointer; font-weight:700; width:100%; font-size:14px; box-shadow: 0 4px 12px rgba(255, 65, 108, 0.2); transition: all 0.2s; }
    
    /* Cấu hình các thanh Tabs phân loại sàn */
    button[data-baseweb="tab"] { color: #94A3B8 !important; font-size: 14px !important; font-weight: 600 !important; }
    button[aria-selected="true"] { color: #FF4B2B !important; }
    div[data-testid="stMarkdownContainer"] h3 { color: #F1F5F9 !important; font-size: 16px !important; margin-bottom: 10px !important; }
    
    /* Dọn dẹp thanh thừa */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Hiển thị Banner Đẳng Cấp Thương Hiệu Riêng
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🛍️ SĂN DEAL TỰ ĐỘNG PRO 🛍️</div>
        <div class="hero-sub">Hệ thống AI tự động quét mã giảm giá và bọc link Affiliate độc quyền 24/7</div>
    </div>
""", unsafe_allow_html=True)

# PHẦN 1: TÍNH NĂNG CHUYỂN LINK
st.markdown('<div class="tool-box">', unsafe_allow_html=True)
st.markdown('<h3>🔗 Dán Link Sản Phẩm Nhận Ưu Đãi</h3>', unsafe_allow_html=True)
link_nhap = st.text_input("", placeholder="Dán link Shopee, Lazada hoặc TiktokShop vào đây...", label_visibility="collapsed")
if link_nhap:
    link_kiem_tien = tao_link_affiliate(link_nhap)
    st.success("🎉 Hệ thống đã bọc mã ưu đãi thành công!")
    st.markdown(f'<a href="{link_kiem_tien}" target="_blank"><button class="btn-buy" style="background: linear-gradient(90deg, #00F0FF, #0072FF); color:#0F172A;">👉 BẤM ĐỂ MUA VỚI GIÁ KHUYẾN MÃI</button></a>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Tab phân loại sàn giao diện tinh tế
tab1, tab2, tab3 = st.tabs(["🔥 Deal Xe & Công Nghệ", "🧡 Sàn Shopee", "💙 Sàn Lazada"])

# Kho dữ liệu mồi hình ảnh cực nét, chuẩn đồ công nghệ xe cộ tài xế mê
kho_deal_vip = [
    {
        "name": "Bơm Lốp Ô Tô Điện Tử Cầm Tay Đa Năng Tự Ngắt Siêu Tốc A8",
        "image": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=500&q=80",
        "price": "399.000đ",
        "discount": "45",
        "url": "https://shopee.vn"
    },
    {
        "name": "Giá Đỡ Điện Thoại Ô Tô Chống Rung Hút Chân Không Cao Cấp",
        "image": "https://images.unsplash.com/photo-1584438784894-089d6a128f3e?w=500&q=80",
        "price": "89.000đ",
        "discount": "30",
        "url": "https://shopee.vn"
    },
    {
        "name": "Tẩu Sạc Nhanh Ô Tô 120W Tích Hợp Đèn LED Hiển Thị Điện Áp",
        "image": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=500&q=80",
        "price": "125.000đ",
        "discount": "50",
        "url": "https://shopee.vn"
    },
    {
        "name": "Nước Hoa Treo Xe Ô Tô Khử Mùi Hương Tự Nhiên Nhập Khẩu",
        "image": "https://images.unsplash.com/photo-1615396899839-c99c121888b0?w=500&q=80",
        "price": "149.000đ",
        "discount": "35",
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
                    <img src="{anh}" style="width:100%; height:150px; border-radius:14px; object-fit:cover;">
                    <div class="product-title">{ten}</div>
                    <div class="price-row">
                        <span class="price-actual">{gia}</span>
                        <span class="badge-discount">🔥 Giảm {giam}%</span>
                    </div>
                    <a href="{link_aff}" target="_blank"><button class="btn-buy">🛒 Lấy Mã & Mua Ngay</button></a>
                </div>
            """, unsafe_allow_html=True)

with tab2:
    st.info("💡 Mã giảm giá Shopee Live, Shopee Video sẽ tự động kích hoạt khi mua qua link.")
with tab3:
    st.info("💡 Voucher tích lũy và mã freeship Lazada được tích hợp tự động vào giỏ hàng.")
