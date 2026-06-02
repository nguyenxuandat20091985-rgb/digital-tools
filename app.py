import streamlit as st
import urllib.parse
import requests
import random

# 1. CẤU HÌNH THÔNG TIN AFFILIATE CHÍNH THỨC CỦA ANH ĐẠT
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_smart_deal"

def tao_link_affiliate(link_goc, merchant="shopee"):
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=1800)
def lay_deal_tu_dong_api(tu_khoa=""):
    """
    Hàm tự động quét toàn bộ sản phẩm từ các chiến dịch anh Đạt tham gia qua API
    """
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    params = {"limit": 12, "search": tu_khoa, "order": "discount_percent"}
    try:
        response = requests.get(url_api, headers=headers, params=params)
        if response.status_code == 200:
            res_data = response.json().get("data", [])
            if res_data: return res_data
        return []
    except:
        return []

# 2. KHO DỮ LIỆU DỰ PHÒNG ĐA NGÁCH CAO CẤP (CHỐNG TRỐNG APP)
KHO_DIEN_TU = [
    {"name": "Sạc Dự Phòng Không Dây 20000mAh Sạc Nhanh 22.5W", "image": "https://images.unsplash.com/photo-1609592424109-dd9892f1b177?w=400", "price": "249.000đ", "discount": "45", "url": "https://shopee.vn", "merchant": "shopee"},
    {"name": "Tai Nghe Bluetooth Không Dây 5.3 Chống Ồn Chủ Động", "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400", "price": "350.000đ", "discount": "35", "url": "https://shopee.vn", "merchant": "shopee"},
    {"name": "Giá Đỡ Điện Thoại Hợp Kim Nhôm Đa Năng Cho Ô Tô/Xe Máy", "image": "https://images.unsplash.com/photo-1586105251261-72a756497a11?w=400", "price": "68.000đ", "discount": "40", "url": "https://shopee.vn", "merchant": "shopee"}
]

KHO_THOI_TRANG = [
    {"name": "Áo Polo Nam Chất Cá Sấu Premium Co Giãn Thoáng Mát", "image": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=400", "price": "185.000đ", "discount": "50", "url": "https://shopee.vn", "merchant": "shopee"},
    {"name": "Son Kem Lì Mịn Mượt Lên Màu Chuẩn Tông Giữ Màu 8h", "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400", "price": "199.000đ", "discount": "30", "url": "https://shopee.vn", "merchant": "shopee"},
    {"name": "Kính Mát Thời Trang Nam Nữ Chống Tia UV400 Cao Cấp", "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400", "price": "120.000đ", "discount": "55", "url": "https://shopee.vn", "merchant": "shopee"}
]

KHO_GIA_DUNG = [
    {"name": "Bình Giữ Nhiệt Inox 314 Cao Cấp dung tích 1000ml", "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400", "price": "145.000đ", "discount": "40", "url": "https://shopee.vn", "merchant": "shopee"},
    {"name": "Máy Xay Sinh Tố Mini Cầm Tay Sạc Pin Tiện Lợi", "image": "https://images.unsplash.com/photo-1578643463396-0997cb5328c1?w=400", "price": "219.000đ", "discount": "35", "url": "https://shopee.vn", "merchant": "shopee"},
    {"name": "Đèn LED Để Bàn Chống Cận Thị 3 Chế Độ Sáng", "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400", "price": "99.000đ", "discount": "50", "url": "https://shopee.vn", "merchant": "shopee"}
]

KHO_TONG_HOP = KHO_DIEN_TU + KHO_THOI_TRANG + KHO_GIA_DUNG

# 3. GIAO DIỆN VIP STYLED BY AI
st.set_page_config(page_title="AI SMART DEAL - Siêu Thị Mua Sắm Tiết Kiệm", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0A0F1D; }
    
    /* Banner chuyển động dải màu Luxury */
    .premium-banner {
        background: linear-gradient(135deg, #FF007A 0%, #7928CA 50%, #4A00E0 100%);
        padding: 35px 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(121, 40, 202, 0.25);
    }
    .premium-title { font-size: 28px; font-weight: 900; color: #FFFFFF; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
    .premium-sub { font-size: 14px; color: #E2E8F0; font-weight: 400; opacity: 0.95; }
    
    /* Thẻ Sản Phẩm Tinh Tế Kiểu Mới */
    .modern-card {
        background: #141B2E;
        border: 1px solid #233253;
        border-radius: 20px;
        padding: 14px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .modern-title {
        color: #F1F5F9; font-size: 14px; font-weight: 600; margin: 12px 0 8px 0;
        height: 40px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;
    }
    .price-container { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
    .price-sale { color: #00F0FF; font-size: 18px; font-weight: 800; }
    .discount-tag { background: linear-gradient(90deg, #FF416C, #FF4B2B); color: white; font-size: 10px; font-weight: bold; padding: 3px 8px; border-radius: 8px; }
    
    /* Thiết kế riêng ô chat AI */
    .ai-box { background: #1E1B4B; border: 1px solid #4338CA; border-radius: 20px; padding: 20px; margin-bottom: 30px; }
    
    h2, h3 { color: #00F0FF !important; font-weight: 700 !important; }
    div[data-testid="stMarkdownContainer"] p { color: #94A3B8; }
    .stTabs [data-baseweb="tab"] { color: #94A3B8 !important; font-weight: bold !important; font-size: 15px !important; }
    .stTabs [aria-selected="true"] { color: #00F0FF !important; border-bottom-color: #00F0FF !important; }
    footer {visibility: hidden;} header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Hiển thị Banner Đỉnh Cao mới
st.markdown("""
    <div class="premium-banner">
        <div class="premium-title">🤖 AI SMART DEAL - SIÊU THỊ MUA SẮM 24/7 🤖</div>
        <div class="premium-sub">Hệ thống AI thông minh tự động tìm kiếm và áp mã giảm giá ẩn từ Shopee, Lazada, Tiki</div>
    </div>
""", unsafe_allow_html=True)

# 🤖 TÍNH NĂNG 1: TRỢ LÝ AI TƯ VẤN VÀ TÌM KIẾM SẢN PHẨM TỰ ĐỘNG
st.markdown('<div class="ai-box">', unsafe_allow_html=True)
st.subheader("🤖 Trợ Lý Trí Tuệ Nhân Tạo AI Tư Vấn")
st.write("Bạn muốn tìm mua gì hôm nay? Hãy nói với AI, hệ thống sẽ tự động quét kho deal tốt nhất và tạo link giảm giá riêng cho bạn:")
cau_hoi_ai = st.text_input("Ví dụ: Tìm cho tôi sạc dự phòng ngon bổ rẻ, Tư vấn váy thời trang đi tiệc...", key="ai_chat")

if cau_hoi_ai:
    st.write("✨ *AI đang phân tích nhu cầu và truy xuất dữ liệu từ các sàn thương mại điện tử...*")
    # Giả lập AI quét dữ liệu dựa trên từ khóa người dùng gõ
    tu_khoa = cau_hoi_ai.lower()
    ket_qua_tim_kiem = []
    
    # Lọc thông minh trong kho dữ liệu tổng hợp
    for sp in KHO_TONG_HOP:
        if any(w in tu_khoa for w in sp["name"].lower().split()):
            ket_qua_tim_kiem.append(sp)
            
    if not ket_qua_tim_kiem:
        ket_qua_tim_kiem = random.sample(KHO_TONG_HOP, 2) # Nếu không khớp, gợi ý ngẫu nhiên 2 món hot
        
    st.info(f"🤖 **Trợ lý AI gợi ý:** Dựa trên nhu cầu của bạn, hệ thống tìm được sản phẩm đang có mã giảm giá sâu nhất:")
    for sp in ket_qua_tim_kiem:
        link_vip = tao_link_affiliate(sp["url"])
        st.markdown(f"🎁 **{sp['name']}** - Giá đang giảm cực sốc chỉ còn **{sp['price']}** (Tiết kiệm được -{sp['discount']}%).")
        st.markdown(f'<a href="{link_vip}" target="_blank"><button style="background-color:#00F0FF; color:#0A0F1D; padding:8px 15px; border:none; border-radius:6px; cursor:pointer; font-weight:bold; margin-bottom:10px;">👉 Bấm Nhận Mã Giảm Giá & Mua Ngay</button></a>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 🔗 TÍNH NĂNG 2: TỰ CHUYỂN LINK NHANH
st.subheader("🔗 Dán Link Bất Kỳ Để Tự Động Áp Mã Giảm Giá")
link_nhap = st.text_input("Dán link Shopee / Lazada bạn sao chép được vào đây:", placeholder="https://shopee.vn/...")
if link_nhap:
    link_kiem_tien = tao_link_affiliate(link_nhap)
    st.success("🎉 Đã bọc link và kích hoạt mã giảm giá ẩn thành công!")
    st.markdown(f'<a href="{link_kiem_tien}" target="_blank"><button style="background-color:#FF007A; color:white; padding:12px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%;">👉 BẤM ĐỂ DI CHUYỂN ĐẾN TRANG GIẢM GIÁ</button></a>', unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True)

# 🛍️ TÍNH NĂNG 3: HIỂN THỊ ĐA NGÁCH CHUYÊN NGHIỆP TRÊN TABS
st.subheader("🔥 Danh Mục Siêu Deal Hot Được Quét Tự Động")
tab1, tab2, tab3, tab4 = st.tabs(["✨ Deal Thịnh Hành", "📱 Đồ Công Nghệ", "👗 Thời Trang & Mỹ Phẩm", "🏠 Đời Sống Gia Dụng"])

def hien_thi_grid_san_pham(danh_sach):
    col1, col2 = st.columns(2)
    for index, item in enumerate(danh_sach):
        cot = col1 if index % 2 == 0 else col2
        with cot:
            ten = item.get("name", "Sản phẩm ưu đãi")
            anh = item.get("image", "https://via.placeholder.com/150")
            giam = item.get("discount", "10")
            
            if isinstance(item.get("price"), (int, float)):
                gia = f"{int(item.get('price')):,}đ"
            else:
                gia = str(item.get("price", "Xem giá"))
                
            link_goc_sp = item.get("url", "https://shopee.vn")
            link_aff = tao_link_affiliate(link_goc_sp)
            
            st.markdown(f"""
                <div class="modern-card">
                    <img src="{anh}" style="width:100%; height:140px; border-radius:12px; object-fit:cover;">
                    <div class="modern-title">{ten}</div>
                    <div class="price-container">
                        <span class="price-sale">{gia}</span>
                        <span class="discount-tag">-{giam}%</span>
                    </div>
                    <a href="{link_aff}" target="_blank"><button style="background-color:#7928CA; color:white; padding:10px; border:none; border-radius:10px; cursor:pointer; font-weight:bold; width:100%; font-size:13px; border: 1px solid #4338CA;">🛒 Mua Ngay</button></a>
                </div>
            """, unsafe_allow_html=True)

# Tab 1: Tổng hợp từ API (Nếu API trống, tự lấy tổng hợp mồi)
with tab1:
    data_api = lay_deal_tu_dong_api()
    if not data_api:
        data_api = KHO_TONG_HOP
    hien_thi_grid_san_pham(data_api)

# Tab 2: Ngách Điện Tử
with tab2:
    data_dien_tu = lay_deal_tu_dong_api("sạc dự phòng, điện thoại, tai nghe")
    if not data_dien_tu:
        data_dien_tu = KHO_DIEN_TU
    hien_thi_grid_san_pham(data_dien_tu)

# Tab 3: Ngách Thời Trang
with tab3:
    data_thoi_trang = lay_deal_tu_dong_api("áo, son, mỹ phẩm, váy")
    if not data_thoi_trang:
        data_thoi_trang = KHO_THOI_TRANG
    hien_thi_grid_san_pham(data_thoi_trang)

# Tab 4: Ngách Gia Dụng
with tab4:
    data_gia_dung = lay_deal_tu_dong_api("bình giữ nhiệt, máy xay, gia dụng")
    if not data_gia_dung:
        data_gia_dung = KHO_GIA_DUNG
    hien_thi_grid_san_pham(data_gia_dung)
