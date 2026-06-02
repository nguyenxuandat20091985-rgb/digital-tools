import streamlit as st
import urllib.parse

# 1. CẤU HÌNH THÔNG TIN AFFILIATE CỦA ANH ĐẠT
ACCESSTRADE_ID = "103085"  
UTM_SOURCE = "taxi_promax_app"

def tao_link_affiliate(link_goc):
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    link_affiliate = f"{base_url}?merchant_id=shopee&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"
    return link_affiliate

# 2. CẤU HÌNH GIAO DIỆN CHUYÊN NGHIỆP
st.set_page_config(page_title="Săn Deal Tự Động Pro", page_icon="🛍️", layout="wide")

# Ép toàn bộ giao diện sang nền tối và chỉnh sửa font chữ, nút bấm sắc nét
st.markdown("""
    <style>
    /* Chỉnh nền toàn bộ app sang màu tối đồng bộ */
    .stApp {
        background-color: #0B0F19;
    }
    
    /* Làm lại tiêu đề chính chỉnh chu, có ánh kim cyan */
    .main-title { 
        font-size: 24px; 
        font-weight: 800; 
        color: #00E5FF; 
        text-align: center; 
        margin-top: 10px;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .sub-title {
        font-size: 14px;
        color: #94A3B8;
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* Thiết kế lại thẻ Card Deal nhìn xịn sò, bo góc, có bóng mờ */
    .deal-card { 
        background: linear-gradient(145deg, #1E293B, #111827);
        padding: 20px; 
        border-radius: 16px; 
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px; 
    }
    
    .deal-title {
        color: #F8FAFC;
        font-size: 16px;
        font-weight: 600;
        margin-top: 0px;
        margin-bottom: 12px;
        line-height: 1.4;
    }
    
    .price-old { 
        text-decoration: line-through; 
        color: #64748B; 
        font-size: 13px; 
        margin-bottom: 2px; 
    }
    
    .price-new { 
        color: #FF4D4D; 
        font-weight: 700; 
        font-size: 20px; 
        margin-bottom: 15px; 
    }
    
    /* Chỉnh lại các chữ tiêu đề mặc định của Streamlit thành màu sáng */
    h3 {
        color: #00E5FF !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stMarkdownContainer"] p {
        color: #CBD5E1;
    }
    </style>
""", unsafe_allow_html=True)

# Hiển thị tiêu đề
st.markdown('<div class="main-title">🛍️ TỔNG HỢP DEAL HOT & MÃ GIẢM GIÁ 🛍️</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Hệ thống tự động cập nhật mã ưu đãi Shopee & Lazada liên tục</div>', unsafe_allow_html=True)

# PHẦN 1: TỰ TẠO LINK QUICK-ACCESS
st.subheader("🔗 Tự Tạo Link Giảm Giá Nhanh")
link_nhap = st.text_input("Dán link sản phẩm Shopee / Lazada vào đây:", placeholder="https://shopee.vn/...")

if link_nhap:
    link_kiem_tien = tao_link_affiliate(link_nhap)
    st.success("🎉 Đã tích hợp mã giảm giá thành công!")
    st.markdown(f'<a href="{link_kiem_tien}" target="_blank"><button style="background-color:#00E5FF; color:#0B0F19; padding:12px 24px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; font-size:15px; width:100%;">👉 BẤM VÀO ĐÂY ĐỂ ĐẾN NƠI MUA GIẢM GIÁ</button></a>', unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True)

# PHẦN 2: DỮ LIỆU KHO DEAL MẪU
st.subheader("🔥 Top Deal Phụ Tùng & Đồ Chơi Xe Hot Hôm Nay")

danh_sach_deal = [
    {
        "ten": "Sạc dự phòng không dây 20000mAh cho Tài xế",
        "gia_goc": "450.000đ",
        "gia_giam": "249.000đ",
        "link": "https://shopee.vn/product/123456/789"
    },
    {
        "ten": "Nước hoa treo xe ô tô cao cấp",
        "gia_goc": "200.000đ",
        "gia_giam": "99.000đ",
        "link": "https://shopee.vn/product/654321/987"
    },
    {
        "ten": "Giá đỡ điện thoại chống rung gắn xe máy/ô tô",
        "gia_goc": "150.000đ",
        "gia_giam": "65.000đ",
        "link": "https://shopee.vn/product/111222/333"
    }
]

# Đưa các thẻ deal hiển thị mượt mà trên giao diện dọc điện thoại
for item in danh_sach_deal:
    link_aff = tao_link_affiliate(item["link"])
    st.markdown(f"""
        <div class="deal-card">
            <div class="deal-title">{item['ten']}</div>
            <div class="price-old">Giá gốc: {item['gia_goc']}</div>
            <div class="price-new">Giá sale: {item['gia_giam']}</div>
            <a href="{link_aff}" target="_blank"><button style="background-color:#FF4D4D; color:white; padding:10px 15px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:14px;">🛒 Lấy Mã & Mua Ngay</button></a>
        </div>
    """, unsafe_allow_html=True)
