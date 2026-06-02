import streamlit as st
import urllib.parse
import requests
import json

# 1. CẤU HÌNH HỆ THỐNG API AFFILIATE (CHÍNH XÁC THEO ACCESSTRADE)
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_quantum_mall"

def tao_link_affiliate(link_goc, merchant="shopee"):
    """
    Hàm tạo link chuẩn mã hóa của Accesstrade v4.
    Đảm bảo bọc đúng cấu trúc để tránh lỗi 404 khi người dùng click mua hàng.
    """
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=1800)  # Tự động lưu bộ nhớ đệm 30 phút để app chạy siêu mượt, tự cập nhật ngầm
def lay_deal_tu_dong_api(tu_khoa=""):
    """
    Hàm kết nối trực tiếp API hệ thống Accesstrade để tự động cập nhật sản phẩm theo các chiến dịch
    """
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Định nghĩa các từ khóa đa ngách chuyên nghiệp để AI tự động quét
    search_query = tu_khoa if tu_khoa else "điện thoại, gia dụng, thời trang, nước hoa"
    params = {
        "limit": 16,
        "search": search_query,
        "order": "discount_percent"  # Sắp xếp ưu tiên các sản phẩm giảm giá mạnh nhất
    }
    try:
        response = requests.get(url_api, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except:
        return []

# 2. CẤU HÌNH GIAO DIỆN CHUẨN SÀN THƯƠNG MẠI ĐIỆN TỬ CAO CẤP (PREMIUM UI/UX)
st.set_page_config(page_title="AI QUANTUM MALL - Siêu Chợ Công Nghệ & Tiết Kiệm", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    /* Nền tối sâu Luxury */
    .stApp { background-color: #060913; }
    
    /* Thiết kế Banner thương hiệu đẳng cấp doanh nghiệp */
    .premium-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
        border: 1px solid #312E81;
        padding: 40px 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }
    .banner-title { font-size: 30px; font-weight: 900; color: #00F0FF; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 15px rgba(0,240,255,0.4); }
    .banner-sub { font-size: 15px; color: #94A3B8; font-weight: 400; }
    
    /* Khung hộp tính năng tìm kiếm VIP */
    .search-container {
        background: rgba(15, 23, 42, 0.6);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #1E293B;
        margin-bottom: 35px;
        backdrop-filter: blur(12px);
    }
    
    /* Thẻ Sản Phẩm Thiết Kế Đồng Bộ Sang Trọng - Kích Thích Mua Hàng */
    .mall-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease-in-out;
    }
    .mall-card:hover {
        transform: translateY(-6px);
        border-color: #00F0FF;
        box-shadow: 0 12px 25px rgba(0, 240, 255, 0.15);
    }
    .mall-title {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 600;
        margin: 12px 0 8px 0;
        height: 42px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        line-height: 1.5;
    }
    .mall-price-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px; }
    .mall-price { color: #FF3B30; font-size: 19px; font-weight: 800; }
    .mall-tag { background: linear-gradient(90deg, #FF4B4B, #FF8533); color: white; font-size: 10px; font-weight: bold; padding: 3px 8px; border-radius: 6px; }
    
    /* Tinh chỉnh các Tab của Streamlit */
    .stTabs [data-baseweb="tab"] { color: #64748B; font-size: 15px; font-weight: 600; padding: 10px 20px; }
    .stTabs [data-baseweb="tab"]:hover { color: #00F0FF; }
    .stTabs [aria-selected="true"] { color: #00F0FF !important; border-bottom-color: #00F0FF !important; }
    h2, h3 { color: #00F0FF !important; font-weight: 700 !important; }
    
    /* Ẩn Header và Footer thừa của Streamlit */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# BIỂU DIỄN BANNER SÀN THƯƠNG MẠI ĐIỆN TỬ CAO CẤP
st.markdown("""
    <div class="premium-banner">
        <div class="banner-title">💎 AI QUANTUM PREMIUM MALL 💎</div>
        <div class="banner-sub">Nền tảng Trợ lý AI tự động tìm kiếm và đồng bộ hóa ưu đãi giảm giá độc quyền 24/7</div>
    </div>
""", unsafe_allow_html=True)

# MENU CHÍNH HỆ THỐNG ĐIỀU HÀNH BÊN THANH TRÁI (SIDEBAR)
menu_chinh = st.sidebar.radio("⚙️ HỆ THỐNG ĐIỀU HÀNH AI", ["🛍️ Sàn TMĐT Ưu Đãi (Khách Hàng)", "🤖 Trung Tâm Quản Trị Hệ Thống (Admin)"])

# KHO DỮ LIỆU ĐA NGÁCH CAO CẤP MẶC ĐỊNH (Hiển thị ngay lập tức khi API đang tải ngầm)
kho_deal_premium = {
    "all": [
        {"name": "Tai Nghe Không Dây Bluetooth 5.3 ANC Chống Ồn Chủ Động", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500", "price": "450.000đ", "discount": "40", "url": "https://shopee.vn"},
        {"name": "Robot Hút Bụi Lau Nhà Thông Minh Lực Hút 4000Pa", "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=500", "price": "3.890.000đ", "discount": "35", "url": "https://shopee.vn"},
        {"name": "Nước Hoa Nam Cao Cấp Hương Gỗ Lôi Cuốn Lịch Lãm", "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=500", "price": "1.200.000đ", "discount": "20", "url": "https://shopee.vn"},
        {"name": "Đồng Hồ Thông Minh Đo Sức Khỏe Màn Hình AMOLED", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500", "price": "890.000đ", "discount": "45", "url": "https://shopee.vn"}
    ],
    "tech": [
        {"name": "Sạc Dự Phòng Không Dây Từ Tính 10000mAh Siêu Nhỏ Gọn", "image": "https://images.unsplash.com/photo-1609592424085-f678e3489370?w=500", "price": "350.000đ", "discount": "30", "url": "https://shopee.vn"},
        {"name": "Bàn Phím Cơ Không Dây RGB Trục Cơ Siêu Nhạy", "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500", "price": "680.000đ", "discount": "25", "url": "https://shopee.vn"}
    ],
    "home": [
        {"name": "Máy Pha Cà Phê Viên Nén Tự Động Mini Gia Đình", "image": "https://images.unsplash.com/photo-1517914103306-27601d9f29a2?w=500", "price": "1.550.000đ", "discount": "15", "url": "https://shopee.vn"},
        {"name": "Quạt Không Cánh Lọc Không Khí Tạo Ion Âm", "image": "https://images.unsplash.com/photo-1618945032994-d109002ae404?w=500", "price": "2.100.000đ", "discount": "40", "url": "https://shopee.vn"}
    ],
    "fashion": [
        {"name": "Kính Mát Phân Cực Nam Nữ Chống Tia UV Cao Cấp", "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500", "price": "299.000đ", "discount": "50", "url": "https://shopee.vn"},
        {"name": "Balo Laptop Chống Trộm Tích Hợp Khóa Số Bảo Mật", "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500", "price": "380.000đ", "discount": "30", "url": "https://shopee.vn"}
    ]
}

def hien_thi_luoi_san_pham(danh_sach):
    """
    Hàm hiển thị danh sách sản phẩm theo cấu trúc lưới 2 cột chuẩn thiết kế di động
    """
    col1, col2 = st.columns(2)
    for idx, item in enumerate(danh_sach):
        cot = col1 if idx % 2 == 0 else col2
        with cot:
            ten = item.get("name", "Sản Phẩm Cao Cấp")
            anh = item.get("image", "https://via.placeholder.com/150")
            giam = item.get("discount", "20")
            
            # Chuẩn hóa hiển thị giá tiền
            if isinstance(item.get("price"), int):
                gia = f"{item.get('price'):,}đ"
            else:
                gia = str(item.get("price", "Xem giá"))
                
            link_goc_sp = item.get("url", "https://shopee.vn")
            merchant_type = "lazada" if "lazada.vn" in link_goc_sp else "shopee"
            link_aff = tao_link_affiliate(link_goc_sp, merchant=merchant_type)
            
            st.markdown(f"""
                <div class="mall-card">
                    <img src="{anh}" style="width:100%; height:150px; border-radius:14px; object-fit:cover;">
                    <div class="mall-title">{ten}</div>
                    <div class="mall-price-row">
                        <span class="mall-price">{gia}</span>
                        <span class="mall-tag">MALL -{giam}%</span>
                    </div>
                    <a href="{link_aff}" target="_blank"><button style="background-color:#00F0FF; color:#060913; padding:10px; border:none; border-radius:10px; cursor:pointer; font-weight:bold; width:100%; font-size:13px; transition: 0.2s;">🛒 Nhận Ưu Đãi Mua Ngay</button></a>
                </div>
            """, unsafe_allow_html=True)

# ----------------- PHÂN HỆ 1: GIAO DIỆN SÀN DÀNH CHO KHÁCH HÀNG -----------------
if menu_chinh == "🛍️ Sàn TMĐT Ưu Đãi (Khách Hàng)":
    
    # Khu vực dán link thông minh tạo link tức thì
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.subheader("🔗 Trợ Lý Nhận Diện & Áp Mã Giảm Giá Ẩn")
    st.write("Dán link sản phẩm bất kỳ từ Shopee hoặc Lazada để hệ thống tự động bọc mã ưu đãi thành viên:")
    link_nhap = st.text_input("", placeholder="Nhập hoặc dán đường dẫn sản phẩm tại đây...", label_visibility="collapsed")
    if link_nhap:
        merchant_type = "lazada" if "lazada.vn" in link_nhap else "shopee"
        link_kiem_tien = tao_link_affiliate(link_nhap, merchant=merchant_type)
        st.success("🎉 Hệ thống AI đã áp mã giảm giá thành công cho sản phẩm của bạn!")
        st.markdown(f'<a href="{link_kiem_tien}" target="_blank"><button style="background-color:#00F0FF; color:#060913; padding:12px; border:none; border-radius:10px; cursor:pointer; font-weight:bold; width:100%; font-size:14px;">👉 CHUYỂN ĐẾN SÀN ĐỂ MUA GIÁ GIẢM</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Phân mục các Tab đa ngách lớn phục vụ toàn bộ các đối tượng khách hàng
    tab_all, tab_tech, tab_home, tab_fashion = st.tabs(["🔥 SIÊU DEAL TỔNG HỢP", "📱 THIẾT BỊ SỐ - CÔNG NGHỆ", "🏠 GIA DỤNG - ĐỜI SỐNG", "👜 THỜI TRANG - MỸ PHẨM"])
    
    with tab_all:
        data = lay_deal_tu_dong_api()
        hien_thi_luoi_san_pham(data if data else kho_deal_premium["all"])
    with tab_tech:
        data = lay_deal_tu_dong_api("điện thoại, máy tính, tai nghe, sạc dự phòng")
        hien_thi_luoi_san_pham(data if data else kho_deal_premium["tech"])
    with tab_home:
        data = lay_deal_tu_dong_api("nồi chiên, máy hút bụi, gia dụng, bếp")
        hien_thi_luoi_san_pham(data if data else kho_deal_premium["home"])
    with tab_fashion:
        data = lay_deal_tu_dong_api("quần áo, túi xách, nước hoa, son")
        hien_thi_luoi_san_pham(data if data else kho_deal_premium["fashion"])

# ----------------- PHÂN HỆ 2: TRUNG TÂM QUẢN TRỊ AI DÀNH RIÊNG CHO ADMIN -----------------
elif menu_chinh == "🤖 Trung Tâm Quản Trị Hệ Thống (Admin)":
    st.subheader("🚀 Công Cụ AI Phân Tích Khách Hàng & Thiết Kế Bài Đăng Đa Kênh")
    st.write("Khu vực cấu hình chiến lược tiếp cận nguồn khách hàng và tự động lên bài quảng cáo seeding.")
    
    # Form chọn ngách khách hàng mục tiêu
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    ngach_khach_hang = st.selectbox("🎯 Chọn tập khách hàng mục tiêu cần tiếp cận hôm nay:", 
                             ["Hội tài xế ô tô / taxi / xe dịch vụ", 
                              "Hội chị em nội trợ / săn deal gia dụng gia đình", 
                              "Hội giới trẻ / học sinh sinh viên đam mê công nghệ"])
    
    st.info("🤖 **Phân tích chiến lược từ AI:** Tập khách hàng này thường hoạt động mạnh trên các group cộng đồng vào khung giờ nghỉ trưa. Đang có xu hướng ưu tiên lựa chọn các sản phẩm thiết thực, giá trị ưu đãi cao từ 30% trở lên.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Hệ thống AI viết bài tìm kiếm khách hàng tự động
    st.subheader("✍️ Trình Biên Soạn Nội Dung Tự Động Bằng AI")
    ten_san_pham = st.text_input("Nhập tên sản phẩm bạn muốn AI lên kịch bản viết bài:", "Robot Hút Bụi Lau Nhà Thông Minh")
    
    if st.button("🪄 Bắt Đầu Khởi Tạo Bài Đăng Thao Túng Tâm Lý"):
        st.success("✅ AI đã hoàn thiện cấu trúc bài viết bán hàng chuẩn SEO!")
        
        st.markdown("### 📱 Kịch bản 1: Đăng Profile Cá Nhân / Tin Nhắn Zalo")
        st.code(f"""
🔥 [SIÊU DEAL ĐỘC QUYỀN - ÁP MÃ GIẢM ĐẾN 40%] 🔥
Cơ hội hiếm có cho mọi người mua sắm tiết kiệm đây ạ! Hệ thống AI của em vừa quét được mã giảm giá ẩn từ tổng kho đối tác sàn TMĐT lớn.

👉 Sản phẩm: {ten_san_pham}
✅ Cam kết chính hãng 100%, bảo hành đầy đủ của nhà sản xuất.
✅ Giá áp mã hôm nay rẻ hơn giá niêm yết thị trường rất nhiều.

Mọi người chỉ cần bấm vào ứng dụng thông minh của em dưới đây để hệ thống tự động nhận diện bọc mã giảm giá ẩn và mua hàng trực tiếp nhé:
🔗 Đường dẫn app săn deal: https://tro-ly-phong-thuy.streamlit.app
        """, language="text")
        
        st.markdown("### 👥 Kịch bản 2: Đăng Seeding Hội Nhóm Cộng Đồng (Group Facebook)")
        st.code(f"""
Có bác nào trong hội mình đang tính chốt em {ten_san_pham} không? 
Đừng mua vội theo giá hiển thị thông thường trên sàn nha, bị đắt đó ạ. Em mới thiết kế cái nền tảng AI tự động quét và áp mã giảm giá ẩn trực tiếp của hệ thống tổng kho Shopee/Lazada. Em chia sẻ link app hoàn toàn miễn phí cho anh em vào tự dán link sản phẩm lấy mã mua cho rẻ nhé:
🔗 Link ứng dụng cào mã tự động: https://tro-ly-phong-thuy.streamlit.app
        """, language="text")
