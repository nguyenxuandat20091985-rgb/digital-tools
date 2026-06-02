import streamlit as st
import urllib.parse

# 1. CẤU HÌNH THÔNG TIN AFFILIATE CỦA ANH ĐẠT
ACCESSTRADE_ID = "103085"  # Mã ID AT103085 của anh Đạt
UTM_SOURCE = "taxi_promax_app"

def tao_link_affiliate(link_goc):
    """
    Hàm tự động bọc link gốc (Shopee/Lazada) thành link Affiliate của Accesstrade
    """
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    link_affiliate = f"{base_url}?merchant_id=shopee&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"
    return link_affiliate

# 2. CẤU HÌNH GIAO DIỆN STREAMLIT
st.set_page_config(page_title="Hệ Thống Săn Deal Tự Động", page_icon="🛍️", layout="wide")

# CSS Tùy chỉnh giao diện hiển thị chuyên nghiệp
st.markdown("""
    <style>
    .main-title { font-size:32px; font-weight:bold; color:#00B4D8; text-align:center; margin-bottom:20px; }
    .deal-card { background-color:#1e293b; padding:15px; border-radius:10px; border-left:5px solid #00B4D8; margin-bottom:15px; }
    .price-old { text-decoration: line-through; color:#94a3b8; font-size:14px; margin-bottom:2px; }
    .price-new { color:#ef4444; font-weight:bold; font-size:18px; margin-bottom:10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛍️ HỆ THỐNG TỔNG HỢP DEAL HOT & MÃ GIẢM GIÁ 🛍️</div>', unsafe_allow_html=True)
st.write("---")

# PHẦN 1: TỰ TẠO LINK AFFILIATE NHANH
st.subheader("🔗 Tự Tạo Link Giảm Giá Nhanh")
st.write("Dán bất kỳ đường link sản phẩm nào từ Shopee hoặc Lazada vào đây để hệ thống tự động bọc mã giảm giá kiếm tiền của anh:")
link_nhap = st.text_input("Nhập link sản phẩm tại đây:", placeholder="https://shopee.vn/...")

if link_nhap:
    link_kiem_tien = tao_link_affiliate(link_nhap)
    st.success("🎉 Đã tạo link tích hợp mã Affiliate thành công!")
    st.markdown(f'<a href="{link_kiem_tien}" target="_blank"><button style="background-color:#00B4D8; color:white; padding:12px 24px; border:none; border-radius:5px; cursor:pointer; font-weight:bold; font-size:16px;">👉 BẤM VÀO ĐÂY ĐỂ ĐẾN NƠI MUA GIẢM GIÁ</button></a>', unsafe_allow_html=True)

st.write("---")

# PHẦN 2: DỮ LIỆU KHO DEAL MẪU (SẼ DÙNG BOT CÀO TỰ ĐỘNG SAU NÀY)
st.subheader("🔥 Top Deal Phụ Tùng & Đồ Chơi Xe Hời Nhất Hôm Nay")

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

# Chia giao diện làm 3 cột để hiển thị các thẻ Deal
col1, col2, col3 = st.columns(3)
cac_cot = [col1, col2, col3]

for index, item in enumerate(danh_sach_deal):
    with cac_cot[index % 3]:
        link_aff = tao_link_affiliate(item["link"])
        st.markdown(f"""
            <div class="deal-card">
                <h4 style="color:white; margin-top:0; min-height:45px;">{item['ten']}</h4>
                <p class="price-old">Giá gốc: {item['gia_goc']}</p>
                <p class="price-new">Giá sale: {item['gia_giam']}</p>
                <a href="{link_aff}" target="_blank"><button style="background-color:#ef4444; color:white; padding:8px 15px; border:none; border-radius:5px; cursor:pointer; font-weight:bold; width:100%;">🛒 Lấy Mã & Mua Ngay</button></a>
            </div>
        """, unsafe_allow_html=True)
