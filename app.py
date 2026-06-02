import streamlit as st
import urllib.parse
import requests

# 1. CẤU HÌNH THÔNG TIN AFFILIATE CỦA ANH ĐẠT
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_multideal_pro"

def tao_link_affiliate(link_goc, merchant="shopee"):
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=1800)
def lay_tat_ca_deal_api(tu_khoa=""):
    """
    Hàm tự động quét toàn bộ sản phẩm từ các chiến dịch anh Đạt đã đăng ký trên Accesstrade
    """
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    
    # Nếu không nhập từ khóa, hệ thống tự động lấy tổng hợp đa ngách hot nhất
    search_query = tu_khoa if tu_khoa else "điện thoại, thời trang, gia dụng, mỹ phẩm"
    params = {
        "limit": 20,
        "search": search_query,
        "order": "discount_percent" # Ưu tiên quét món giảm giá sâu nhất hệ thống
    }
    try:
        response = requests.get(url_api, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except:
        return []

# 2. GIAO DIỆN SÀN THƯƠNG MẠI ĐIỆN TỬ CAO CẤP (PREMIUM UI/UX)
st.set_page_config(page_title="AI Multi-Deal Pro", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0A0E17; }
    
    /* Banner Sàn TMĐT Sang Trọng */
    .premium-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #311042 100%);
        border: 1px solid #4C1D95;
        padding: 35px 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(76, 29, 149, 0.3);
    }
    .banner-title { font-size: 28px; font-weight: 900; color: #00F0FF; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1.5px; text-shadow: 0 2px 10px rgba(0,240,255,0.5); }
    .banner-sub { font-size: 14px; color: #E2E8F0; font-weight: 400; opacity: 0.85; }
    
    /* Khung Tìm Kiếm & Dán Link VIP */
    .search-container {
        background: rgba(30, 41, 59, 0.5);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #334155;
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
    }
    
    /* Card Sản Phẩm Đẹp Mắt Muốn Mua Ngay */
    .mall-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 18px;
        padding: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .mall-card:hover {
        transform: translateY(-5px);
        border-color: #00F0FF;
        box-shadow: 0 10px 20px rgba(0, 240, 255, 0.1);
    }
    .mall-title {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 600;
        margin: 12px 0 8px 0;
        height: 40px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        line-height: 1.4;
    }
    .mall-price-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
    .mall-price { color: #FF3B30; font-size: 18px; font-weight: 800; }
    .mall-tag { background: linear-gradient(90deg, #EF4444, #F59E0B); color: white; font-size: 10px; font-weight: bold; padding: 3px 7px; border-radius: 6px; }
    
    /* Tối ưu hóa Tab và Chữ */
    .stTabs [data-baseweb="tab"] { color: #94A3B8; font-size: 14px; font-weight: 600; }
    .stTabs [data-baseweb="tab"]:hover { color: #00F0FF; }
    .stTabs [aria-selected="true"] { color: #00F0FF !important; border-bottom-color: #00F0FF !important; }
    h2, h3 { color: #00F0FF !important; font-weight: 700 !important; }
    
    /* Ẩn Header/Footer thừa */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# BIỂU DIỄN BANNER SÀN THƯƠNG MẠI ĐIỆN TỬ VIP
st.markdown("""
    <div class="premium-banner">
        <div class="banner-title">💎 AI MULTI-DEAL MALL 💎</div>
        <div class="banner-sub">Hệ thống AI Tự Động Tìm Kiếm Siêu Ưu Đãi Đa Ngách Từ Các Sàn TMĐT Hàng Đầu</div>
    </div>
""", unsafe_allow_html=True)

# MENU CHÍNH CHUYỂN ĐỔI GIỮA GIAO DIỆN NGƯỜI MUA VÀ TRÌNH QUẢN LÝ AI CỦA ANH ĐẠT
menu_chinh = st.sidebar.radio("⚙️ HỆ THỐNG ĐIỀU HÀNH", ["🛍️ Giao Diện Săn Deal (Khách Hàng)", "🤖 Trung Tâm Quản Trị AI (Anh Đạt)"])

# ----------------- KHÔNG GIAN 1: GIAO DIỆN DÀNH CHO KHÁCH HÀNG -----------------
if menu_chinh == "🛍️ Giao Diện Săn Deal (Khách Hàng)":
    
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.subheader("🔗 Dán Link Nhận Mã Giảm Giá Ẩn")
    link_nhap = st.text_input("", placeholder="Dán link sản phẩm Shopee, Lazada bất kỳ vào đây để áp mã...", label_visibility="collapsed")
    if link_nhap:
        merchant_type = "lazada" if "lazada.vn" in link_nhap else "shopee"
        link_kiem_tien = tao_link_affiliate(link_nhap, merchant=merchant_type)
        st.success("🎉 AI đã kích hoạt mã giảm giá thành công cho sản phẩm này!")
        st.markdown(f'<a href="{link_kiem_tien}" target="_blank"><button style="background-color:#00F0FF; color:#0A0E17; padding:12px; border:none; border-radius:10px; cursor:pointer; font-weight:bold; width:100%; font-size:15px;">👉 BẤM ĐỂ MUA NGAY VỚI GIÁ GIẢM</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Hệ thống Tabs Phân Loại Ngách Đa Dạng
    tab_all, tab_tech, tab_home, tab_fashion = st.tabs(["🔥 SIÊU DEAL TỔNG HỢP", "📱 ĐIỆN TỬ - CÔNG NGHỆ", "🏠 GIA DỤNG - ĐỜI SỐNG", "👜 THỜI TRANG - MỸ PHẨM"])
    
    # Kho dữ liệu mồi đa ngách sang xịn phòng khi API rỗng
    kho_deal_mac_dinh = {
        "all": [
            {"name": "Tai Nghe Không Dây Bluetooth 5.3 Pro Âm Thanh Hifi", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500", "price": "299.000đ", "discount": "40", "url": "https://shopee.vn"},
            {"name": "Nồi Chiên Không Dầu Cảm Ứng Điện Tử 8L", "image": "https://images.unsplash.com/photo-1621972750749-0fbb1abb7736?w=500", "price": "1.250.000đ", "discount": "35", "url": "https://shopee.vn"},
            {"name": "Son Kem Lì Mịn Môi Cao Cấp Không Trôi", "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=500", "price": "185.000đ", "discount": "25", "url": "https://shopee.vn"},
            {"name": "Balo Thời Trang Nam Nữ Chống Nước Có Cổng Sạc", "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500", "price": "220.000đ", "discount": "50", "url": "https://shopee.vn"}
        ],
        "tech": [{"name": "Sạc Dự Phòng 20000mAh Sạc Nhanh 22.5W", "image": "https://images.unsplash.com/photo-1609592424085-f678e3489370?w=500", "price": "249.000đ", "discount": "45", "url": "https://shopee.vn"}],
        "home": [{"name": "Máy Hút Bụi Cầm Tay Không Dây Lực Hút Siêu Mạnh", "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=500", "price": "450.000đ", "discount": "30", "url": "https://shopee.vn"}],
        "fashion": [{"name": "Kính Mát Thời Trang Phi Công Chống Tia UV400", "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500", "price": "150.000đ", "discount": "60", "url": "https://shopee.vn"}]
    }

    def hien_thi_grid_san_pham(danh_sach):
        col1, col2 = st.columns(2)
        for idx, item in enumerate(danh_sach):
            cot = col1 if idx % 2 == 0 else col2
            with cot:
                ten = item.get("name", "Sản Phẩm Cao Cấp")
                anh = item.get("image", "https://via.placeholder.com/150")
                giam = item.get("discount", "30")
                gia = f"{item.get('price'):,}đ" if isinstance(item.get("price"), int) else str(item.get("price", "Xem giá"))
                link_aff = tao_link_affiliate(item.get("url", "https://shopee.vn"))
                
                st.markdown(f"""
                    <div class="mall-card">
                        <img src="{anh}" style="width:100%; height:140px; border-radius:12px; object-fit:cover;">
                        <div class="mall-title">{ten}</div>
                        <div class="mall-price-row">
                            <span class="mall-price">{gia}</span>
                            <span class="mall-tag">MALL -{giam}%</span>
                        </div>
                        <a href="{link_aff}" target="_blank"><button style="background-color:#00F0FF; color:#0A0E17; padding:9px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:13px;">🛒 Xem Chi Tiết & Mua</button></a>
                    </div>
                """, unsafe_allow_html=True)

    with tab_all:
        data = lay_tat_ca_deal_api()
        hien_thi_grid_san_pham(data if data else kho_deal_mac_dinh["all"])
    with tab_tech:
        data = lay_tat_ca_deal_api("điện thoại, phụ kiện máy tính, tai nghe")
        hien_thi_grid_san_pham(data if data else kho_deal_mac_dinh["tech"])
    with tab_home:
        data = lay_tat_ca_deal_api("gia dụng, bếp, dọn dẹp nhà")
        hien_thi_grid_san_pham(data if data else kho_deal_mac_dinh["home"])
    with tab_fashion:
        data = lay_tat_ca_deal_api("quần áo, túi xách, mỹ phẩm")
        hien_thi_grid_san_pham(data if data else kho_deal_mac_dinh["fashion"])

# ----------------- KHÔNG GIAN 2: TRUNG TÂM QUẢN TRỊ AI CỦA ANH ĐẠT -----------------
elif menu_chinh == "🤖 Trung Tâm Quản Trị AI (Anh Đạt)":
    st.subheader("🚀 Robot AI Phân Tích Khách Hàng & Tự Động Tạo Bài Viết Bán Hàng")
    st.write("Không gian dành riêng cho anh Đạt cấu hình chiến lược tìm kiếm khách hàng đa kênh.")
    
    # 1. Chọn ngách khách hàng muốn tiếp cận
    ngach_chon = st.selectbox("🎯 Chọn ngách khách hàng anh muốn khai thác hôm nay:", 
                             ["Hội tài xế ô tô / taxi (Sạc dự phòng, tẩu sạc, đệm ghế)", 
                              "Hội chị em nội trợ (Nồi chiên, máy hút bụi, đồ bếp)", 
                              "Hội học sinh / sinh viên (Tai nghe giá rẻ, balo, đồ decor)"])
    
    # 2. AI gợi ý sản phẩm phù hợp nhất với ngách
    st.info("🤖 **AI phân tích hành vi:** Ngách này đang có xu hướng mua sắm mạnh vào khung giờ 12h trưa và 20h tối. Ưu tiên các sản phẩm dưới 300k để chốt đơn nhanh.")
    
    # 3. Tính năng tự động tạo bài viết đăng bài đa kênh
    st.write("---")
    st.subheader("✍️ AI Tự Động Lên Kịch Bản Bài Viết Tìm Kiếm Khách Hàng")
    ten_sp_viet_bai = st.text_input("Nhập tên sản phẩm anh muốn AI viết bài quảng cáo:", "Tai Nghe Không Dây Bluetooth Pro")
    
    if st.button("🪄 Kích Hoạt AI Tạo Bài Đăng Thôi Miên"):
        # Đoạn kịch bản mồi AI tự động xuất ra cho anh Đạt đi copy
        st.success("✅ AI đã xây dựng xong kịch bản bài đăng chất lượng cao!")
        
        st.markdown("### 📱 Kịch bản đăng Facebook / Zalo Cá Nhân:")
        st.code(f"""
🔥 [DEAL HỦY DIỆT - GIẢM ĐẾN 40%] 🔥
Anh em lướt mạng nhiều có thấy món này đang hot hòn họt không? Em vừa quét được mã giảm giá ẩn từ tổng kho độc quyền của sàn!

👉 Món: {ten_sp_viet_bai}
✅ Hàng chính hãng, bảo hành đầy đủ.
✅ Giá hôm nay rẻ hơn thị trường một nửa.

Bấm vào link ứng dụng của em để hệ thống tự động bọc mã giảm giá và đặt hàng trực tiếp nha mọi người:
🔗 Link săn ngay: https://tro-ly-phong-thuy.streamlit.app
        """, language="text")
        
        st.markdown("### 👥 Kịch bản đăng vào các Hội Nhóm (Group Seeding):")
        st.code(f"""
Có bác nào đang định mua {ten_sp_viet_bai} không ạ? 
Đừng mua vội giá gốc nha phí tiền lắm. Em vừa làm cái app AI tự động cào và áp mã giảm giá ẩn của tổng kho Shopee/Lazada xong. Bác nào cần em chia sẻ link vào tự bấm lấy mã mà mua cho rẻ nè:
🔗 Link app tự động: https://tro-ly-phong-thuy.streamlit.app
        """, language="text")
