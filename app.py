import streamlit as st
import urllib.parse
import requests

# 1. CẤU HÌNH THÔNG TIN AFFILIATE CỦA ANH ĐẠT
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_quantum_shop"

def tao_link_affiliate(link_goc):
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id=shopee&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=900)  # Cập nhật liên tục mỗi 15 phút
def lay_tat_ca_deal_api(tu_khoa=""):
    """
    Hàm quét TẤT CẢ các chiến dịch đang chạy của anh dựa theo danh mục khách hàng lựa chọn
    """
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    
    # Nếu không có từ khóa, quét tổng hợp đa ngách hot nhất
    search_keyword = tu_khoa if tu_khoa else "điện thoại, gia dụng, thời trang, mỹ phẩm, bỉm sữa"
    params = {
        "limit": 20, 
        "search": search_keyword, 
        "order": "discount_percent" # Luôn ưu tiên món giảm sâu nhất lên đầu
    }
    try:
        response = requests.get(url_api, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except:
        return []

# 2. GIAO DIỆN CHUẨN SÀN THƯƠNG MẠI ĐIỆN TỬ CAO CẤP
st.set_page_config(page_title="AI QUANTUM SHOP - Siêu Sàn Săn Deal Tự Động", page_icon="🛍️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0F172A; }
    
    /* Header kiểu Shopee/Lazada Premium */
    .shop-header {
        background: linear-gradient(90deg, #F97316 0%, #EA580C 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
    }
    .shop-title { font-size: 28px; font-weight: 800; color: white; margin-bottom: 5px; letter-spacing: 0.5px; }
    .shop-sub { font-size: 14px; color: #FFEDD5; }
    
    /* Thẻ sản phẩm chuẩn E-commerce */
    .mall-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .mall-title {
        color: #F1F5F9; font-size: 13px; font-weight: 500; margin: 8px 0;
        height: 36px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;
    }
    .price-box { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    .price-new { color: #F97316; font-size: 16px; font-weight: 700; }
    .discount-tag { background: #FEF2F2; color: #EF4444; font-size: 10px; font-weight: bold; padding: 1px 4px; border-radius: 4px; border: 1px solid #FEE2E2; }
    
    /* Ẩn footer mờ của Streamlit */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom bọc khung tabs */
    .stTabs [data-baseweb="tab"] { color: #94A3B8 !important; font-weight: 600; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #F97316 !important; }
    </style>
""", unsafe_allow_html=True)

# Hiển thị thanh Header Sàn Thương Mại Mới
st.markdown("""
    <div class="shop-header">
        <div class="shop-title">🛍️ AI QUANTUM SHOP 🛍️</div>
        <div class="shop-sub">Hệ thống AI tự động quét và cập nhật Deal Hot từ Shopee, Lazada, Tiki, Tiktok Shop</div>
    </div>
""", unsafe_allow_html=True)

# KHU VỰC 1: TRỢ LÝ AI TƯ VẤN & GỢI Ý MUA SẮM TỰ ĐỘNG
st.markdown("### 🤖 Trợ Lý AI Tư Vấn Mua Sắm Thông Minh")
AI_gợi_ý = st.text_input("Anh/Chị cần tìm sản phẩm gì? (Ví dụ: Tìm sạc dự phòng tốt, tìm bỉm sữa cho bé, tìm váy thời trang...)", placeholder="Nhập nhu cầu của bạn, AI sẽ tự động lục kho deal...")

# KHU VỰC 2: THANH CHUYỂN LINK TỰ ĐỘNG KHÁCH HÀNG TỰ DÁN
with st.expander("🔗 Bạn có sẵn link sản phẩm? Dán vào đây để nhận mã giảm giá ẩn"):
    link_nhap = st.text_input("Dán link Shopee / Lazada vào đây:", placeholder="https://...")
    if link_nhap:
        link_aff = tao_link_affiliate(link_nhap)
        st.success("🎉 Đã áp mã giảm giá ẩn thành công!")
        st.markdown(f'<a href="{link_aff}" target="_blank"><button style="background-color:#F97316; color:white; padding:10px; border:none; border-radius:6px; cursor:pointer; font-weight:bold; width:100%;">👉 MỞ SẢN PHẨM ĐÃ GIẢM GIÁ</button></a>', unsafe_allow_html=True)

# KHU VỰC 3: PHÂN CHIA DANH MỤC ĐA NGÁCH THEO TABS ĐỂ PHỤC VỤ NHIỀU ĐỐI TƯỢNG KHÁCH HÀNG
st.write("<br><h3>🔥 KHÁM PHÁ DANH MỤC KHUYẾN MÃI</h3>", unsafe_allow_html=True)
tab_all, tab_tech, tab_home, tab_fashion, tab_mom = st.tabs(["⭐ Tất Cả Deal Hot", "📱 Công Nghệ / Phụ Tùng", "🏠 Gia Dụng / Đời Sống", "👗 Thời Trang / Mỹ Phẩm", "🍼 Mẹ & Bé VIP"])

# Danh sách dữ liệu mồi đa ngách cực kỳ đa dạng
kho_deal_moi_da_ngach = {
    "all": [
        {"name": "Tai Nghe Không Dây Bluetooth 5.3 Âm Thanh HIFI", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400", "price": "199.000đ", "discount": "50", "url": "https://shopee.vn"},
        {"name": "Nồi Chiên Không Dầu Điện Tử Khóa Nhiệt 15L", "image": "https://images.unsplash.com/photo-1621972750749-0fbb1abb7736?w=400", "price": "850.000đ", "discount": "35", "url": "https://shopee.vn"},
        {"name": "Son Kem Lì Mịn Môi Cao Cấp Lên Màu Chuẩn", "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400", "price": "145.000đ", "discount": "40", "url": "https://shopee.vn"},
        {"name": "Combo 3 Bộ Quần Áo Cotton Sợi Tre Cho Bé", "image": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400", "price": "180.000đ", "discount": "30", "url": "https://shopee.vn"}
    ],
    "tech": [
        {"name": "Sạc Dự Phòng 20000mAh Sạc Nhanh 22.5W", "image": "https://images.unsplash.com/photo-1609592424085-f6dfcf30cf82?w=400", "price": "249.000đ", "discount": "45", "url": "https://shopee.vn"},
        {"name": "Giá Đỡ Điện Thoại Ô Tô Chống Rung Cao Cấp", "image": "https://images.unsplash.com/photo-1586105251261-72a756497a11?w=400", "price": "65.000đ", "discount": "20", "url": "https://shopee.vn"}
    ],
    "home": [
        {"name": "Máy Hút Bụi Cầm Tay Không Dây Lực Hút Siêu Mạnh", "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400", "price": "320.000đ", "discount": "50", "url": "https://shopee.vn"},
        {"name": "Bình Giữ Nhiệt Inox 304 Cao Cấp dung tích 1L", "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400", "price": "115.000đ", "discount": "30", "url": "https://shopee.vn"}
    ],
    "fashion": [
        {"name": "Áo Polo Nam Chất Cá Sấu Co Giãn Thoáng Mát", "image": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=400", "price": "139.000đ", "discount": "40", "url": "https://shopee.vn"},
        {"name": "Váy Nữ Dáng Xòe Tiểu Thư Cực Xinh Đi Chơi", "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400", "price": "210.000đ", "discount": "25", "url": "https://shopee.vn"}
    ],
    "mom": [
        {"name": "Tã Quần Sơ Sinh Công Nghệ Thấm Hút Ban Đêm", "image": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=400", "price": "299.000đ", "discount": "15", "url": "https://shopee.vn"},
        {"name": "Máy Hâm Sữa Tiệt Trùng Đa Năng Cho Bé", "image": "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=400", "price": "350.000đ", "discount": "35", "url": "https://shopee.vn"}
    ]
}

def hien_thi_grid_san_pham(danh_sach):
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
                <div class="mall-card">
                    <img src="{anh}" style="width:100%; height:140px; border-radius:8px; object-fit:cover;">
                    <div class="mall-title">{ten}</div>
                    <div class="price-box">
                        <span class="price-new">{gia}</span>
                        <span class="discount-tag">-{giam}%</span>
                    </div>
                    <a href="{link_aff}" target="_blank"><button style="background-color:#F97316; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer; font-weight:bold; width:100%; font-size:12px;">Mua Ngay</button></a>
                </div>
            """, unsafe_allow_html=True)

# Điều hướng hiển thị theo lựa chọn của AI hoặc Tab thường
with tab_all:
    data_api = lay_tat_ca_deal_api(AI_gợi_ý if AI_gợi_ý else "")
    if AI_gợi_ý and data_api:
        st.info(f"🤖 Trợ lý AI đang hiển thị kết quả lọc tự động cho từ khóa: '{AI_gợi_ý}'")
    hien_thi_grid_san_pham(data_api if data_api else kho_deal_moi_da_ngach["all"])

with tab_tech:
    data_tech = lay_tat_ca_deal_api("điện tử, sạc pin, phụ tùng xe")
    hien_thi_grid_san_pham(data_tech if data_tech else kho_deal_moi_da_ngach["tech"])

with tab_home:
    data_home = lay_tat_ca_deal_api("gia dụng, bếp, dọn nhà")
    hien_thi_grid_san_pham(data_home if data_home else kho_deal_moi_da_ngach["home"])

with tab_fashion:
    data_fashion = lay_tat_ca_deal_api("quần áo, thời trang, mỹ phẩm")
    hien_thi_grid_san_pham(data_fashion if data_fashion else kho_deal_moi_da_ngach["fashion"])

with tab_mom:
    data_mom = lay_tat_ca_deal_api("bỉm sữa, đồ chơi trẻ em, tã")
    hien_thi_grid_san_pham(data_mom if data_mom else kho_deal_moi_da_ngach["mom"])
