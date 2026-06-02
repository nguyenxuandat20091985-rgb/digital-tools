import streamlit as st
import urllib.parse
import requests

# 1. CẤU HÌNH HỆ THỐNG AFFILIATE & API (ANH ĐẠT NGUYỄN)
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_quantum_deal"

def tao_link_affiliate(link_goc, merchant="shopee"):
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=900)  # Cập nhật liên tục 15 phút/lần để đồng bộ chiến dịch mới
def lay_deal_tu_dong_tat_ca_chien_dich(tu_khoa="🔥"):
    """
    Hàm tự động quét toàn bộ sản phẩm từ các chiến dịch anh Đạt đã đăng ký trên Accesstrade
    """
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    params = {
        "limit": 20,
        "search": tu_khoa,
        "order": "discount_percent" # Ưu tiên lấy deal giảm sâu nhất của tất cả các sàn
    }
    try:
        response = requests.get(url_api, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except:
        return []

# 2. CẤU HÌNH GIAO DIỆN PREMIUM UI/UX (HỌC HỎI CÁC SÀN LỚN)
st.set_page_config(page_title="AI-QUANTUM | Siêu Trợ Lý Săn Deal", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #060913; }
    
    /* Banner Đỉnh Cao Phong Cách Công Nghệ */
    .premium-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border: 1px solid #3b82f6;
        padding: 35px 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
    }
    .premium-title { font-size: 28px; font-weight: 900; color: #00F0FF; margin-bottom: 8px; letter-spacing: 2px; }
    .premium-sub { font-size: 14px; color: #E2E8F0; opacity: 0.9; font-weight: 400; }
    
    /* Khung Tìm Kiếm & Dán Link */
    .search-container {
        background: #0f172a;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #1e293b;
        margin-bottom: 35px;
    }
    
    /* Lưới Sản Phẩm Đa Dạng */
    .product-grid-card {
        background: #111c30;
        border: 1px solid #1e365d;
        border-radius: 18px;
        padding: 14px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .product-grid-card:hover { border-color: #00F0FF; }
    .product-grid-title {
        color: #F8FAFC; font-size: 14px; font-weight: 600; margin: 12px 0 6px 0;
        height: 40px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;
    }
    .price-group { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
    .price-new { color: #FF3B3B; font-size: 18px; font-weight: 700; }
    .discount-tag { background: #DC2626; color: white; font-size: 11px; font-weight: bold; padding: 2px 6px; border-radius: 6px; }
    
    /* Nút Mua VIP */
    .btn-buy {
        background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%);
        color: white; border: none; padding: 10px; border-radius: 10px;
        font-weight: bold; width: 100%; cursor: pointer; transition: 0.3s; font-size: 14px;
    }
    
    /* Khung Trợ lý AI */
    .ai-box {
        background: linear-gradient(145deg, #0f172a, #1e1b4b);
        border: 1px solid #6366f1;
        border-radius: 20px;
        padding: 20px;
        margin-top: 30px;
    }
    
    /* CSS cho thanh Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b; color: #94A3B8; border-radius: 8px; padding: 8px 16px; font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; color: white !important; }
    
    footer {visibility: hidden;} header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# BANNER CAO CẤP CHUẨN THƯƠNG HIỆU CỦA ANH ĐẠT
st.markdown("""
    <div class="premium-banner">
        <div class="premium-title">💎 AI-QUANTUM SMART COMMERCE 💎</div>
        <div class="premium-sub">Hệ thống AI tự động quét và tối ưu mã giảm giá từ tất cả chiến dịch đã đăng ký</div>
    </div>
""", unsafe_allow_html=True)

# 3. TÍNH NĂNG TỰ ĐỘNG BỌC LINK ĐA NĂNG
st.markdown('<div class="search-container">', unsafe_allow_html=True)
st.subheader("🔍 Công Cụ Tối Ưu Link Mua Sắm Toàn Năng")
st.write("Hỗ trợ tự động bọc mã ID đối với mọi sản phẩm từ Shopee, Lazada, Tiki, Tiktok Shop...")
link_nhap = st.text_input("", placeholder="Dán bất kỳ đường link sản phẩm nào vào đây để nhận giá ưu đãi...", label_visibility="collapsed")
if link_nhap:
    merchant_detect = "shopee"
    if "lazada" in link_nhap.lower(): merchant_detect = "lazada"
    elif "tiki" in link_nhap.lower(): merchant_detect = "tiki"
    
    link_vip = tao_link_affiliate(link_nhap, merchant=merchant_detect)
    st.success("🎉 Cấu hình link Affiliate thành công! Sẵn sàng chia sẻ kiếm tiền hoa hồng.")
    st.markdown(f'<a href="{link_vip}" target="_blank"><button class="btn-buy" style="background: linear-gradient(90deg, #00F0FF 0%, #0072FF 100%); color:#060913;">👉 CLICK ĐỂ ĐẾN NƠI GIẢM GIÁ MẠNH NHẤT</button></a>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 4. DANH MỤC ĐA NGÁCH PHỤC VỤ MỌI ĐỐI TƯỢNG KHÁCH HÀNG
st.subheader("🛍️ Kho Deal Thật Khổng Lồ Tự Động Từ Các Chiến Dịch")
tab_all, tab_tech, tab_home, tab_mom = st.tabs(["🔥 SIÊU DEAL TỔNG HỢP", "💻 ĐIỆN TỬ & CÔNG NGHỆ", "🏠 GIA DỤNG & ĐỜI SỐNG", "🍼 MẸ & BÉ GIÁ TỐT"])

# Dữ liệu dự phòng siêu đẹp (Chống trống giao diện khi API của sàn đang xử lý đồng bộ)
kho_backups = {
    "🔥": [{"name": "Sạc Dự Phòng Cực Khủng 20000mAh Sạc Nhanh 22.5W", "image": "https://images.unsplash.com/photo-1609592424109-dd9892f1b17c?w=400", "price": "249.000đ", "discount": "45", "url": "https://shopee.vn"},
            {"name": "Tai Nghe Không Dây Bluetooth Âm Thanh Sống Động", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400", "price": "185.000đ", "discount": "50", "url": "https://shopee.vn"}],
    "công nghệ": [{"name": "Giá Đỡ Điện Thoại Kim Loại Cao Cấp Chống Rung Ô Tô", "image": "https://images.unsplash.com/photo-1586105251261-72a756497a11?w=400", "price": "65.000đ", "discount": "35", "url": "https://shopee.vn"}],
    "gia dụng": [{"name": "Máy Hút Bụi Cầm Tay Không Dây Lực Hút Siêu Mạnh", "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400", "price": "320.000đ", "discount": "40", "url": "https://shopee.vn"}],
    "mẹ và bé": [{"name": "Bình Sữa Cổ Rộng Nhập Khẩu Cao Cấp An Toàn Cho Bé", "image": "https://images.unsplash.com/photo-1522836924445-4478bdeb860c?w=400", "price": "145.000đ", "discount": "25", "url": "https://shopee.vn"}]
}

def hien_thi_danh_sach_deal(tu_khoa, backup_key):
    # Lấy deal thật từ API tự động cập nhật
    data_api = lay_deal_tu_dong_api() if tu_khoa == "🔥" else lay_deal_tu_dong_api() # Thực tế sẽ lọc theo từ khóa
    if not data_api:
        data_api = kho_backups[backup_key]
        
    col1, col2 = st.columns(2)
    for index, item in enumerate(data_api):
        cot_chon = col1 if index % 2 == 0 else col2
        with cot_chon:
            ten = item.get("name", "Sản phẩm ưu đãi")
            anh = item.get("image", "https://via.placeholder.com/150")
            giam = item.get("discount", "30")
            gia = f"{item.get('price'):,}đ" if isinstance(item.get("price"), int) else str(item.get("price", "Xem giá"))
            link_final = tao_link_affiliate(item.get("url", "https://shopee.vn"))
            
            st.markdown(f"""
                <div class="product-grid-card">
                    <img src="{anh}" style="width:100%; height:140px; border-radius:12px; object-fit:cover;">
                    <div class="product-grid-title">{ten}</div>
                    <div class="price-group">
                        <span class="price-new">{gia}</span>
                        <span class="discount-tag">-{giam}%</span>
                    </div>
                    <a href="{link_final}" target="_blank"><button class="btn-buy">🛒 Xem Chi Tiết & Mua Ngay</button></a>
                </div>
            """, unsafe_allow_html=True)

with tab_all: hien_thi_danh_sach_deal("🔥", "🔥")
with tab_tech: hien_thi_danh_sach_deal("điện tử, sạc", "công nghệ")
with tab_home: hien_thi_danh_sach_deal("gia dụng, máy hút bụi", "gia dụng")
with tab_mom: hien_thi_danh_sach_deal("bình sữa, tã em bé", "mẹ và bé")

# 5. KHU VỰC SIÊU TRỢ LÝ AI ĐIỀU HÀNH - TÌM KIẾM KHÁCH HÀNG & LÊN KỊCH BẢN TỰ ĐỘNG
st.markdown('<div class="ai-box">', unsafe_allow_html=True)
st.subheader("🤖 TRỢ LÝ AI-QUANTUM: TỰ ĐỘNG TÌM KHÁCH & SOẠN BÀI")
st.write("Hệ thống trí tuệ nhân tạo hỗ trợ anh Đạt phân tích hành vi và lên bài đăng tự động lan tỏa link:")

ngach_chon = st.selectbox("1. Chọn ngách sản phẩm anh muốn ra đơn hôm nay:", ["Đồ dùng/Đồ chơi dành cho tài xế xe công nghệ", "Đồ gia dụng thông minh cho gia đình", "Sản phẩm bỉm sữa, đồ chơi trẻ em"])
kenh_dang = st.selectbox("2. Chọn kênh anh muốn triển khai tìm kiếm khách hàng:", ["Hội nhóm Facebook công khai", "Nhóm Chat Zalo / Telegram", "Trang cá nhân thu hút thụ động"])

if st.button("🧠 KÍCH HOẠT AI PHÂN TÍCH & SOẠN BÀI"):
    st.info("🔮 AI đang phân tích tệp khách hàng trực tuyến...")
    
    if "tài xế" in ngach_chon.lower():
        st.markdown(f"""
        **🎯 Tệp khách hàng mục tiêu:** Tài xế chạy xe taxi công nghệ, xe dịch vụ, hay di chuyển ngoài đường. Thói quen online vào khung giờ nghỉ trưa (11h30-13h) và đêm muộn sau ca chạy.
        
        **📝 Gợi ý kịch bản đăng bài (Copy rải nhóm Facebook/Zalo):**
```text
        Anh em tài xế chạy ca ngày nắng nóng hay bị sập nguồn điện thoại thì vào đây xem thử nhé. 
        Em vừa săn được mã giảm 45% cho con Sạc dự phòng 20000mAh sạc siêu nhanh, hàng chính hãng dùng bao mượt cho anh em di chuyển liên tục.
        Anh em vào lấy mã ưu đãi tại app tổng kho của em nhé: [https://tro-ly-phong-thuy.streamlit.app](https://tro-ly-phong-thuy.streamlit.app)
        ```
        """)
    else:
        st.markdown(f"""
        **🎯 Tệp khách hàng mục tiêu:** Hội chị em phụ nữ, các bà mẹ bỉm sữa thích săn hàng sale giá rẻ, thích săn mã freeship vào khung giờ vàng 0h và 12h trưa.
        
        **📝 Gợi ý kịch bản đăng bài:**
```text
        Các mom ơi, em vừa dùng hệ thống AI quét được lô bình sữa cao cấp và máy hút bụi cầm tay đang được trợ giá giảm sâu tận 40-50% trên sàn lớn này.
        Mọi người không cần tìm kiếm đâu xa, cứ vào thẳng cổng tổng hợp deal an toàn của em chọn món mình cần là tự áp mã giảm nhé: [https://tro-ly-phong-thuy.streamlit.app](https://tro-ly-phong-thuy.streamlit.app)
        ```
        """)
st.markdown('</div>', unsafe_allow_html=True)
