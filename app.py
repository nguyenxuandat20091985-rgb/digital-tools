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
def lay_deal_tu_dong_api(tu_khoa):
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    params = {"limit": 12, "search": tu_khoa, "order": "discount_percent"}
    try:
        response = requests.get(url_api, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except:
        return []

# 2. THIẾT KẾ UI/UX CAO CẤP - CHUẨN SÀN THƯƠNG MẠI ĐIỆN TỬ
st.set_page_config(page_title="Săn Deal Tự Động Pro", page_icon="🛍️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0A0E1A; }
    
    /* Banner VIP tinh tế, tiết kiệm không gian */
    .premium-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #311042 100%);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #4C1D95;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.15);
    }
    .premium-title { font-size: 22px; font-weight: 900; color: #00F0FF; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1.5px; text-shadow: 0 0 10px rgba(0,240,255,0.5); }
    .premium-sub { font-size: 12px; color: #94A3B8; font-weight: 400; }
    
    /* Khung nhập link bo tròn hiện đại */
    .search-box {
        background: #111827;
        padding: 15px;
        border-radius: 14px;
        border: 1px solid #1F2937;
        margin-bottom: 25px;
    }
    
    /* Thẻ sản phẩm bóng bẩy, thu hút ánh nhìn */
    .card-pro {
        background: #161F30;
        border: 1px solid #24344D;
        border-radius: 14px;
        padding: 10px;
        margin-bottom: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .card-pro:hover {
        border-color: #00F0FF;
        transform: translateY(-2px);
    }
    .card-title {
        color: #E2E8F0;
        font-size: 13px;
        font-weight: 600;
        margin: 8px 0 6px 0;
        height: 38px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        line-height: 1.4;
    }
    .card-price-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    .price-now { color: #FF4444; font-size: 16px; font-weight: 700; }
    .badge-sale { background: #EF4444; color: white; font-size: 9px; font-weight: 800; padding: 2px 5px; border-radius: 4px; }
    
    /* Tối ưu tab điều hướng */
    .stTabs [data-baseweb="tab"] { color: #94A3B8 !important; font-size: 14px !important; font-weight: 600 !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #00F0FF !important; border-bottom-color: #00F0FF !important; }
    
    footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# Hiển thị Banner Mới Sang Trọng
st.markdown("""
    <div class="premium-banner">
        <div class="premium-title">🛍️ SĂN DEAL TỰ ĐỘNG PRO 🛍️</div>
        <div class="premium-sub">Hệ thống AI tổng hợp mã giảm giá Shopee - Lazada cập nhật liên tục 24/7</div>
    </div>
""", unsafe_allow_html=True)

# PHẦN 1: TÌM KIẾM / DÁN LINK
st.markdown('<div class="search-box">', unsafe_allow_html=True)
st.markdown("<b style='color:#00F0FF; font-size:14px;'>🔗 Dán Link Sản Phẩm Bất Kỳ Để Nhận Giảm Giá</b>", unsafe_allow_html=True)
link_nhap = st.text_input("", placeholder="Dán đường dẫn Shopee hoặc Lazada vào đây để bọc mã...", label_visibility="collapsed")
if link_nhap:
    link_kiem_tien = tao_link_affiliate(link_nhap)
    st.success("🎉 Đã bọc mã giảm giá ẩn thành công!")
    st.markdown(f'<a href="{link_kiem_tien}" target="_blank"><button style="background-color:#00F0FF; color:#0A0E1A; padding:10px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:14px;">👉 BẤM ĐỂ MUA GIÁ GIẢM NGAY</button></a>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# PHẦN 2: SIÊU CHỢ SẢN PHẨM ĐA DẠNG DANH MỤC
st.markdown("<h3 style='color:#00F0FF; font-size:16px; margin-bottom:15px;'>🔥 DANH MỤC KHUYẾN MÃI SIÊU HOT HÔM NAY</h3>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["🚗 Đồ Chơi & Phụ Tùng Xe", "💻 Thiết Bị Công Nghệ", "🏠 Đồ Gia Dụng Thông Minh"])

# KHO DỮ LIỆU ĐA DẠNG (BACKUP KHI API CHƯA ĐỔ DỮ LIỆU)
kho_xe = [
    {"name": "Bơm Lốp Ô Tô Điện Tử Thông Minh Kèm Đèn LED Siêu Tốc", "image": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=400", "price": "399.000đ", "discount": "45", "url": "https://shopee.vn"},
    {"name": "Giá Đỡ Điện Thoại Ô Tô Chống Rung Cao Cấp Hút Chân Không", "image": "https://images.unsplash.com/photo-1586105251261-72a756497a11?w=400", "price": "89.000đ", "discount": "30", "url": "https://shopee.vn"},
    {"name": "Tẩu Sạc Nhanh Ô Tô 120W Chia Nhiều Cổng Tiện Lợi", "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400", "price": "145.000đ", "discount": "35", "url": "https://shopee.vn"},
    {"name": "Bạt Phủ Xe Ô Tô Cách Nhiệt Chống Nóng Phản Quang Cao Cấp", "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400", "price": "270.000đ", "discount": "40", "url": "https://shopee.vn"}
]

kho_cong_nghe = [
    {"name": "Sạc Dự Phòng Không Dây 20000mAh Sạc Siêu Nhanh 22.5W", "image": "https://images.unsplash.com/photo-1609592424109-dd9892f1b177?w=400", "price": "249.000đ", "discount": "50", "url": "https://shopee.vn"},
    {"name": "Tai Nghe Bluetooth Không Dây 5.3 Âm Thanh Hifi Khử Tiếng Ồn", "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400", "price": "185.000đ", "discount": "45", "url": "https://shopee.vn"},
    {"name": "Thẻ Nhớ Tốc Độ Cao 64GB/128GB Cho Camera Hành Trình", "image": "https://images.unsplash.com/photo-1558486740-bf5d55fa4385?w=400", "price": "95.000đ", "discount": "30", "url": "https://shopee.vn"},
    {"name": "Loa Bluetooth Mini Cầm Tay Bass Trầm Sâu Chống Nước IPX7", "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400", "price": "299.000đ", "discount": "40", "url": "https://shopee.vn"}
]

kho_gia_dung = [
    {"name": "Bình Giữ Nhiệt Inox 304 Cao Cấp Hiển Thị Nhiệt Độ LED", "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400", "price": "119.000đ", "discount": "35", "url": "https://shopee.vn"},
    {"name": "Quạt Tích Điện Cầm Tay Mini 5 Cấp Độ Gió Siêu Mát", "image": "https://images.unsplash.com/photo-1618941746270-08365610b37f?w=400", "price": "79.000đ", "discount": "50", "url": "https://shopee.vn"},
    {"name": "Máy Hút Bụi Mini Cầm Tay Không Dây Lực Hút Siêu Mạnh", "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400", "price": "215.000đ", "discount": "42", "url": "https://shopee.vn"},
    {"name": "Đèn LED Để Bàn Chống Cận Thị Tích Hợp Sạc Điện Thoại", "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400", "price": "165.000đ", "discount": "30", "url": "https://shopee.vn"}
]

def hien_thi_grid_deal(danh_sach):
    col1, col2 = st.columns(2)
    for index, item in enumerate(danh_sach):
        cot = col1 if index % 2 == 0 else col2
        with cot:
            ten = item.get("name", "Sản phẩm")
            anh = item.get("image", "https://via.placeholder.com/150")
            giam = item.get("discount", "20")
            gia = f"{item.get('price'):,}đ" if isinstance(item.get("price"), int) else str(item.get("price", "Xem giá"))
            link_aff = tao_link_affiliate(item.get("url", "https://shopee.vn"))
            
            st.markdown(f"""
                <div class="card-pro">
                    <img src="{anh}" style="width:100%; height:120px; border-radius:10px; object-fit:cover;">
                    <div class="card-title">{ten}</div>
                    <div class="card-price-row">
                        <span class="price-now">{gia}</span>
                        <span class="badge-sale">-{giam}%</span>
                    </div>
                    <a href="{link_aff}" target="_blank"><button style="background-color:#FF3A44; color:white; padding:8px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:12px; letter-spacing:0.5px;">🛒 MUA NGAY</button></a>
                </div>
            """, unsafe_allow_html=True)

# THỰC THI HIỂN THỊ THEO TAB
with tab1:
    data_xe = lay_deal_tu_dong_api("phụ tùng xe, tẩu sạc ô tô")
    hien_thi_grid_deal(data_xe if data_xe else kho_xe)

with tab2:
    data_tech = lay_deal_tu_dong_api("sạc dự phòng, tai nghe, thẻ nhớ")
    hien_thi_grid_deal(data_tech if data_tech else kho_cong_nghe)

with tab3:
    data_home = lay_deal_tu_dong_api("bình giữ nhiệt, quạt mini, máy hút bụi")
    hien_thi_grid_deal(data_home if data_home else kho_gia_dung)
