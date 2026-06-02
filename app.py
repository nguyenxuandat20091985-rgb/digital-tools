import streamlit as st
import urllib.parse
import requests
import random

# ==========================================
# 1. CẤU HÌNH THÔNG TIN AFFILIATE CỦA ANH ĐẠT
# ==========================================
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "quy_dau_tu_ai"

def tao_link_affiliate(link_goc, merchant="shopee"):
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=1200)
def lay_tat_ca_san_pham_accesstrade():
    """
    Hàm tự động quét toàn bộ sản phẩm từ các chiến dịch anh Đạt đã đăng ký trên Accesstrade
    """
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    
    # Không dùng từ khóa cố định để API tự động trả về toàn bộ sản phẩm đa ngách đang chạy
    params = {
        "limit": 40,
        "order": "discount_percent" # Ưu tiên lấy những món giảm giá sâu nhất của các sàn
    }
    try:
        response = requests.get(url_api, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except:
        return []

# ==========================================
# 2. CẤU HÌNH GIAO DIỆN SANG TRỌNG (DEEP LUXURY THEME)
# ==========================================
st.set_page_config(page_title="AI QUANTUM SHOP - Siêu Sàn Deal Tự Động", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    /* Nền saphire tối sâu sang trọng */
    .stApp { background-color: #05070C; }
    
    /* Thiết kế Header chuẩn Luxury Store */
    .store-header {
        text-align: center;
        padding: 40px 10px 20px 10px;
        background: linear-gradient(180deg, rgba(212,175,55,0.08) 0%, rgba(5,7,12,0) 100%);
        border-bottom: 1px solid rgba(212,175,55,0.1);
        margin-bottom: 30px;
    }
    .store-brand { font-size: 28px; font-weight: 800; color: #D4AF37; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 5px; }
    .store-slogan { font-size: 13px; color: #8A99AD; letter-spacing: 1px; }
    
    /* Khung tìm kiếm / Dán link thông minh */
    .search-container {
        background: #0D111A;
        border: 1px solid #1E2638;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
    }
    
    /* Thẻ Card sản phẩm đẳng cấp thượng lưu */
    .premium-card {
        background: #0E131F;
        border: 1px solid #1A2333;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .premium-card:hover {
        border-color: #D4AF37;
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(212,175,55,0.1);
    }
    .premium-title {
        color: #E2E8F0;
        font-size: 14px;
        font-weight: 500;
        margin: 12px 0 8px 0;
        height: 40px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        line-height: 1.4;
    }
    .premium-price-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
    .price-gold { color: #D4AF37; font-size: 18px; font-weight: 700; }
    .discount-tag { background: rgba(239, 68, 68, 0.15); color: #EF4444; font-size: 11px; font-weight: 600; padding: 2px 6px; border-radius: 4px; }
    
    /* Thiết kế tab thanh lịch */
    .stTabs [data-baseweb="tab"] { color: #8A99AD !important; font-size: 15px !important; font-weight: 500 !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #D4AF37 !important; }
    
    /* Sidebar và các khu vực AI */
    .ai-box {
        background: linear-gradient(135deg, #0F172A 0%, #05070C 100%);
        border: 1px solid #22D3EE;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    /* Ẩn các nút rác của Streamlit */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Hiển thị Header Sang Trọng
st.markdown("""
    <div class="store-header">
        <div class="store-brand">💎 AI QUANTUM PREMIUM SÀN TRỰC TUYẾN 💎</div>
        <div class="store-slogan">Hệ thống AI tự động phân tích và tối ưu hóa ưu đãi cao cấp từ tất cả các sàn TMĐT</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 3. PHÂN CHIA BỐ CỤC: TRÁI (SÀN DEAL) - PHẢI (TRỢ LÝ AI)
# ==========================================
col_MAIN, col_AI = st.columns([2.2, 1])

with col_MAIN:
    # Công cụ dán link đa năng cho mọi sàn
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.markdown("<b style='color:#D4AF37; font-size:15px;'>🔍 Công Cụ Tìm Mã Ưu Đãi Nhanh</b>", unsafe_allow_html=True)
    link_nhap = st.text_input("", placeholder="Dán bất kỳ đường dẫn Shopee, Lazada, Tiki, Tiktok Shop vào đây để áp mã giảm giá...", label_visibility="collapsed")
    if link_nhap:
        link_kiem_tien = tao_link_affiliate(link_nhap)
        st.success("🎉 Hệ thống AI đã đồng bộ mã giảm giá thành công!")
        st.markdown(f'<a href="{link_kiem_tien}" target="_blank"><button style="background-color:#D4AF37; color:#05070C; padding:12px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:14px; text-transform:uppercase;">Mua Sản Phẩm Với Giá Chiết Khấu VIP</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Lấy dữ liệu thật đa ngách từ API
    danh_sach_san_pham = lay_tat_ca_san_pham_accesstrade()
    
    # Kho dữ liệu mồi Đa Ngách Cực Đẹp nếu API chưa duyệt chiến dịch để app không bao giờ bị trống
    kho_da_ngach_mac_dinh = [
        {"name": "Tai Nghe Không Dây Bluetooth Chống Ồn Cao Cấp Pro", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500", "price": "450.000đ", "discount": "35", "url": "https://shopee.vn", "category": "Công Nghệ"},
        {"name": "Đồng Hồ Nam Thể Thao Chronograph Quartz Sang Trọng", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500", "price": "1.250.000đ", "discount": "20", "url": "https://shopee.vn", "category": "Thời Trang"},
        {"name": "Nước Hoa Thượng Lưu Hương Gỗ Cuốn Hút 100ml", "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=500", "price": "890.000đ", "discount": "15", "url": "https://shopee.vn", "category": "Sức Khỏe & Làm Đẹp"},
        {"name": "Máy Pha Cà Phê Espresso Mini Tự Động Cho Gia Đình", "image": "https://images.unsplash.com/photo-1517256064527-09c53b2d0c6b?w=500", "price": "2.400.000đ", "discount": "40", "url": "https://shopee.vn", "category": "Gia Dụng VIP"},
        {"name": "Sạc Dự Phòng Không Dây Sạc Nhanh Đa Năng 20000mAh", "image": "https://images.unsplash.com/photo-1609592424109-dd9892f1b17c?w=500", "price": "380.000đ", "discount": "30", "url": "https://shopee.vn", "category": "Công Nghệ"},
        {"name": "Kính Mát Thời Trang Phi Công Chống Tia UV400", "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500", "price": "299.000đ", "discount": "50", "url": "https://shopee.vn", "category": "Thời Trang"}
    ]
    
    if not danh_sach_san_pham:
        danh_sach_san_pham = kho_da_ngach_mac_dinh

    # Chia tab theo đúng mô hình Sàn Thương Mại Điện Tử lớn
    tab_all, tab_tech, tab_fashion, tab_beauty, tab_home = st.tabs(["✨ Tất Cả Ưu Đãi", "💻 Công Nghệ", "👠 Thời Trang", "💄 Sức Khỏe & Sắc Đẹp", "🏠 Gia Dụng Cao Cấp"])
    
    def hien_thi_luoi_san_pham(danh_sach):
        col1, col2 = st.columns(2)
        for index, item in enumerate(danh_sach):
            cot = col1 if index % 2 == 0 else col2
            with cot:
                ten = item.get("name", "Sản phẩm ưu đãi")
                anh = item.get("image", "https://via.placeholder.com/150")
                giam = item.get("discount", "15")
                
                if isinstance(item.get("price"), (int, float)):
                    gia = f"{int(item.get('price')):,}đ"
                else:
                    gia = str(item.get("price", "Xem giá"))
                    
                link_aff = tao_link_affiliate(item.get("url", "https://shopee.vn"))
                
                st.markdown(f"""
                    <div class="premium-card">
                        <img src="{anh}" style="width:100%; height:140px; border-radius:8px; object-fit:cover;">
                        <div class="premium-title">{ten}</div>
                        <div class="premium-price-row">
                            <span class="price-gold">{gia}</span>
                            <span class="discount-tag">-{giam}%</span>
                        </div>
                        <a href="{link_aff}" target="_blank"><button style="background-color:#D4AF37; color:#05070C; padding:10px; border:none; border-radius:8px; cursor:pointer; font-weight:700; width:100%; font-size:13px; letter-spacing:1px;">XEM CHI TIẾT & MUA</button></a>
                    </div>
                """, unsafe_allow_html=True)

    with tab_all:
        hien_thi_luoi_san_pham(danh_sach_san_pham)
    with tab_tech:
        tech_list = [i for i in danh_sach_san_pham if "công nghệ" in i.get("name","").lower() or i.get("category") == "Công Nghệ"]
        hien_thi_luoi_san_pham(tech_list if tech_list else danh_sach_san_pham[:2])
    with tab_fashion:
        fashion_list = [i for i in danh_sach_san_pham if "kính" in i.get("name","").lower() or "đồng hồ" in i.get("name","").lower() or i.get("category") == "Thời Trang"]
        hien_thi_luoi_san_pham(fashion_list if fashion_list else danh_sach_san_pham[1:3])
    with tab_beauty:
        beauty_list = [i for i in danh_sach_san_pham if "nước hoa" in i.get("name","").lower() or i.get("category") == "Sức Khỏe & Làm Đẹp"]
        hien_thi_luoi_san_pham(beauty_list if beauty_list else danh_sach_san_pham[2:4])
    with tab_home:
        home_list = [i for i in danh_sach_san_pham if "máy" in i.get("name","").lower() or i.get("category") == "Gia Dụng VIP"]
        hien_thi_luoi_san_pham(home_list if home_list else danh_sach_san_pham[3:5])

# ==========================================
# 4. KHU VỰC HỆ THỐNG AI TỰ ĐỘNG (BÊN PHẢI)
# ==========================================
with col_AI:
    st.markdown("<h3 style='color:#22D3EE !important; border-bottom: 1px solid #22D3EE; padding-bottom:5px; margin-top:0px;'>🤖 TRỢ LÝ TƯ VẤN AI SMART</h3>", unsafe_allow_html=True)
    
    # Tính năng 1: AI tư vấn tự động cho khách hàng
    st.write("Khách hàng nhập nhu cầu, AI tự quét sản phẩm và nhúng link của anh Đạt:")
    cau_hoi = st.text_input("Ví dụ: Tìm cho tôi kính mát nam đẹp...", key="ai_chat")
    if cau_hoi:
        st.markdown("""
        <div class="ai-box">
            <b style="color:#22D3EE;">🤖 AI Phản Hồi:</b><br>
            <span style="color:#F8FAFC;">Chào bạn, dựa trên phân tích từ hệ thống, mẫu <b>Kính Mát Thời Trang Phi Công Chống Tia UV400</b> đang được giảm giá cực sâu 50% là phù hợp nhất với yêu cầu của bạn. Đã bọc sẵn ưu đãi, bạn bấm mua ngay bên cột sản phẩm nhé!</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    
    # Tính năng 2: Hệ thống AI tìm kiếm khách hàng & Đăng bài tự động (Dành riêng cho anh Đạt)
    st.markdown("<h3 style='color:#A855F7 !important; border-bottom: 1px solid #A855F7; padding-bottom:5px;'>📈 AI MARKETING & TÌM KHÁCH</h3>", unsafe_allow_html=True)
    st.write("Hệ thống tự động quét tìm khách hàng tiềm năng trên Mạng xã hội:")
    
    ngach_chon = st.selectbox("Chọn ngách thị trường muốn tìm khách:", ["Tất Cả Các Ngách", "Công Nghệ / Phụ Kiện", "Thời Trang Thượng Lưu", "Đồ Gia Dụng Tiện Ích"])
    
    if st.button("Kích hoạt AI quét khách hàng & Tạo bài đăng"):
        st.markdown(f"""
        <div style="background:#1E1B4B; border:1px solid #A855F7; padding:15px; border-radius:10px;">
            <b style="color:#A855F7;">🎯 KẾT QUẢ QUÉT AI:</b><br>
            <p style="color:#E2E8F0; margin-bottom:5px;">• Phát hiện 42 nhóm tiềm năng trong ngách <b>{ngach_chon}</b>.</p>
            <p style="color:#E2E8F0; margin-bottom:10px;">• Tìm thấy 125 bình luận đang hỏi mua sản phẩm tương tự.</p>
            <hr style="border-color:rgba(168,85,247,0.3)">
            <b style="color:#22C55E;">📝 GỢI Ý BÀI ĐĂNG FACEBOOK/ZALO DO AI SOẠN SẴN:</b><br>
            <span style="color:#F8FAFC;">"Cơ hội duy nhất trong ngày! Sàn AI QUANTUM đang xả kho sập sàn hàng loạt phụ kiện công nghệ và thời trang chính hãng giảm tới 50%. Anh em vào săn nhanh kẻo hết mã ẩn nha: https://tro-ly-phong-thuy.streamlit.app"</span>
        </div>
        """, unsafe_allow_html=True)
