import streamlit as st
import urllib.parse

# 1. CẤU HÌNH THÔNG TIN AFFILIATE CỦA ANH ĐẠT
ACCESSTRADE_ID = "103085"  # Lấy từ mã AT103085 trong ảnh của anh
UTM_SOURCE = "taxi_promax_app" # Để anh biết nguồn tiền từ app nào về

def tao_link_affiliate(link_goc):
    """
    Hàm tự động bọc link gốc (Shopee/Lazada) thành link Affiliate của Accesstrade
    """
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    
    # Mã hóa link gốc để đưa vào URL bọc
    link_ma_hoa = urllib.parse.quote(link_goc)
    
    # Tạo đường dẫn kết quả tích hợp mã ID của anh Đạt
    link_affiliate = f"{base_url}?merchant_id=shopee&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"
    return link_affiliate

# 2. GIAO DIỆN CHUYÊN NGHIỆP BẰNG STREAMLIT
st.set_page_config(page_title="Hệ Thống Săn Deal Tự Động", page_icon="🛍️", layout="wide")

# CSS Tùy chỉnh giao diện màu sắc hiện đại giống Taxi ProMax
st.markdown("""
    <style>
    .main-title { font-size:32px; font-weight:bold; color:#00B4D8; text-align:center; margin-bottom:20px; }
    .deal-card { background-color:#1e293b; padding:15px; border-radius:10px; border-left:5px solid #00B4D8; margin-bottom:15px; }
    .price-old { text-decoration: line-through; color:#94a3b8; font-size:14px; }
    .price-new { color:#ef4444; font-weight:bold; font-size:18px; }
    </style>
""", unsafe_allow_name=True)

st.markdown('<div class="main-title">🛍️ HỆ THỐNG TỔNG HỢP DEAL HOT & MÃ GIẢM GIÁ 🛍️</div>', unsafe_allow_html=True)
st.write("---")

# CỘT 1: TÍNH NĂNG CHUYỂN LINK NHANH (Dành cho anh em tự dán link muốn mua)
st.subheader("🔗 Tự Tạo Link Giảm Giá Nhanh")
link_nhap = st.text_input("Dán link sản phẩm Shopee / Lazada bạn muốn mua vào đây:")

if link_nhap:
    link_kiem_tien = tao_link_affiliate(link_nhap)
    st.success("🎉 Đã tạo mã giảm giá thành công! Bấm nút bên dưới để mua với giá ưu đãi.")
    st.video("https://assets.mixkit.co/videos/preview/mixkit-shopping-at-the-mall-40149-large.mp4") # Video minh họa nhỏ nếu thích
    st.markdown(f'<a href="{link_kiem_tien}" target="_blank"><button style="background-color:#00B4D8; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">👉 BẤM VÀO ĐÂY ĐỂ ĐẾN NƠI GIẢM GIÁ</button></a>', unsafe_allow_html=True)

st.write("---")

# CỘT 2: KHO DEAL TỰ ĐỘNG (Dữ liệu này sau này sẽ dùng Python cào tự động vào)
st.subheader("🔥 Top Deal Phụ Tùng & Đồ Chơi Xe Hời Nhất Hôm Nay")

# Mockup dữ liệu mẫu để anh thấy cách hiển thị
danh_sach_deal = [
    {
        "ten": "Sạc dự phòng không dây 20000mAh cho Tài xế",
        "gia_goc": "450.000đ",
        "gia_giam": "249.000đ",
        "link": "https://shopee.vn/product/123456/789"
    },
    {
        "ten": "Nước hoa treo xe ô tô VinFast cao cấp",
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

# Hiển thị danh sách deal ra giao diện
col1, col2, col3 = st.columns(3)
cac_cot = [col1, col2, col3]

for index, item in enumerate(danh_sach_deal):
    with cac_cot[index % 3]:
        link_aff = tao_link_affiliate(item["link"])
        st.markdown(f"""
            <div class="deal-card">
                <h4 style="color:white; margin-top:0;">{item['ten']}</h4>
                <p class="price-old">Giá gốc: {item['gia_goc']}</p>
                <p class="price-new">Giá sale: {item['gia_giam']}</p>
                <a href="{link_aff}" target="_blank"><button style="background-color:#ef4444; color:white; padding:5px 10px; border:none; border-radius:3px; cursor:pointer;">🛒 Lấy Mã & Mua Ngay</button></a>
            </div>
        """, unsafe_allow_html=True)
