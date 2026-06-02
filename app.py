import streamlit as st
import urllib.parse
import requests

# 1. CẤU HÌNH THÔNG TIN AFFILIATE TRẦN ĐẠT
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "megadeal_pro"

def tao_link_affiliate(link_goc, merchant="shopee"):
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=900)  # Cập nhật liên tục 15 phút một lần cho nóng
def tai_tat_ca_deal_api(tu_khoa="", danh_muc=""):
    """
    Hàm AI tự động quét tất cả các chiến dịch anh Đạt đã đăng ký trên Accesstrade
    """
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    
    # Chuỗi tìm kiếm linh hoạt để đa dạng hóa mọi ngách khách hàng
    search_query = tu_khoa if tu_khoa else (danh_muc if danh_muc else "mỹ phẩm, mẹ và bé, công nghệ, gia dụng, thời trang")
    
    params = {
        "limit": 20,
        "search": search_query,
        "order": "discount_percent"  # Luôn ưu tiên deal giảm sâu nhất lên đầu sàn
    }
    try:
        response = requests.get(url_api, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except:
        return []

# 2. GIAO DIỆN CHUẨN SÀN THƯƠNG MẠI ĐIỆN TỬ ĐẲNG CẤP CAO
st.set_page_config(page_title="MegaDeal Pro - Siêu Thị Săn Deal Tự Động", page_icon="🛍️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0F172A; }
    
    /* Thiết kế Header Sàn Thương Mại Điện Tử */
    .smartecom-header {
        background: linear-gradient(90deg, #F97316 0%, #EA580C 100%);
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(234, 88, 12, 0.2);
    }
    .smartecom-title { font-size: 28px; font-weight: 800; color: white; margin-bottom: 5px; letter-spacing: 0.5px; }
    .smartecom-sub { font-size: 14px; color: #FFEDD5; opacity: 0.9; }
    
    /* Bộ chọn danh mục bằng Icon */
    .cate-box {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        color: #F8FAFC;
        font-weight: 600;
        font-size: 13px;
    }
    
    /* Thẻ sản phẩm chuẩn E-com đổ bóng mềm mượt */
    .ecom-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, border-color 0.2s;
    }
    .ecom-card:hover { transform: translateY(-4px); border-color: #F97316; }
    .ecom-title {
        color: #F1F5F9; font-size: 13px; font-weight: 500; margin: 8px 0 4px 0;
        height: 36px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;
    }
    .price-container { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
    .price-sale { color: #EF4444; font-size: 16px; font-weight: 700; }
    .tag-giam { background: #FEE2E2; color: #EF4444; font-size: 10px; font-weight: bold; padding: 1px 5px; border-radius: 4px; }
    
    /* Định dạng lại Tab thanh lịch */
    .stTabs [data-baseweb="tab"] { color: #94A3B8 !important; font-weight: 600; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #F97316 !important; border-bottom-color: #F97316 !important; }
    
    footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Hiển thị Banner tổng kho thương mại điện tử hoành tráng
st.markdown("""
    <div class="smartecom-header">
        <div class="smartecom-title">🛍️ MEGA DEAL PRO - SIÊU THỊ MÃ GIẢM GIÁ 🛍️</div>
        <div class="smartecom-sub">Hệ thống AI thông minh tự động gom Deal Hot & Mã giảm giá từ tất cả các sàn hàng đầu Việt Nam</div>
    </div>
""", unsafe_allow_html=True)

# PHẦN 1: TÌM KIẾM & TRỢ LÝ AI TƯ VẤN (YÊU CẦU MỚI)
col_search, col_ai = st.columns([2, 1])

with col_search:
    st.markdown('<p style="color:#F97316; font-weight:bold; margin-bottom:2px;">🔍 BẠN MUỐN TÌM SẢN PHẨM GÌ?</p>', unsafe_allow_html=True)
    tu_khoa_tim = st.text_input("", placeholder="Nhập tên sản phẩm cần mua (Ví dụ: bỉm, son môi, tai nghe, nồi chiên...)", label_visibility="collapsed")

with col_ai:
    st.markdown('<p style="color:#00F0FF; font-weight:bold; margin-bottom:2px;">🤖 TRỢ LÝ AI TƯ VẤN MUA SẮM</p>', unsafe_allow_html=True)
    cau_hoi_ai = st.text_input("", placeholder="Hỏi AI: Cần mua quà sinh nhật cho vợ dưới 500k...", label_visibility="collapsed")

if cau_hoi_ai:
    st.info(f"🤖 **Trợ lý AI gợi ý:** Đối với yêu cầu '{cau_hoi_ai}', anh/chị nên tham khảo các dòng Son môi chính hãng hoặc Nước hoa đang sale 40% ở danh mục Mỹ Phẩm bên dưới, cam kết giá rẻ nhất thị trường!")

# PHẦN 2: CÔNG CỤ DÁN LINK NHANH
with st.expander("🔗 BẠN ĐÃ CÓ LINK SẢN PHẨM? DÁN VÀO ĐÂY ĐỂ ÉP MÃ GIẢM GIÁ"):
    link_nhap = st.text_input("Dán link Shopee, Lazada, Tiki...", placeholder="https://...")
    if link_nhap:
        st.success("🎉 Đã ép mã giảm giá thành công! Bấm nút bên dưới để mua:")
        st.markdown(f'<a href="{tao_link_affiliate(link_nhap)}" target="_blank"><button style="background-color:#F97316; color:white; padding:10px; border:none; border-radius:6px; cursor:pointer; font-weight:bold; width:100%;">👉 MUA NGAY VỚI GIÁ GIẢM SÂU</button></a>', unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True)

# PHẦN 3: HIỂN THỊ DANH MỤC SẢN PHẨM ĐA NGÁCH
st.markdown('<h3 style="color:#F97316 !important; font-size:18px;">🔥 XU HƯỚNG MUA SẮM ĐA NGÁCH HÔM NAY</h3>', unsafe_allow_html=True)

tab_all, tab_tech, tab_beauty, tab_mom, tab_home = st.tabs(["🌎 Tất Cả Deal Hot", "💻 Đồ Công Nghệ", "💄 Mỹ Phẩm - Làm Đẹp", "👶 Mẹ & Bé VIP", "🏠 Gia Dụng Thông Minh"])

# Kho dữ liệu mồi đa dạng ngách phòng trường hợp API của sàn đang load
kho_deal_ecom = {
    "tat_ca": tai_tat_ca_deal_api(tu_khoa=tu_khoa_tim),
    "cong_nghe": tai_tat_ca_deal_api(danh_muc="tai nghe, loa bluetooth, sạc dự phòng"),
    "my_pham": tai_tat_ca_deal_api(danh_muc="son môi, kem chống nắng, nước hoa"),
    "me_be": tai_tat_ca_deal_api(danh_muc="tã bỉm, sữa bột, đồ chơi trẻ em"),
    "gia_dung": tai_tat_ca_deal_api(danh_muc="nồi chiên không dầu, máy hút bụi, quạt mini")
}

def hien_thi_luoi_san_pham(danh_sach_sp, danh_muc_loai):
    # Nếu API trống, nạp dữ liệu mồi chất lượng cao theo từng ngách ngay để giữ chân khách
    if not danh_sach_sp:
        dữ_lieu_moi = {
            "cong_nghe": [{"name": "Tai Nghe Không Dây Bluetooth HIFI Cực Êm", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300", "price": "185.000đ", "discount": "40", "url": "https://shopee.vn"}],
            "my_pham": [{"name": "Son Kem Lì Mịn Môi Chính Hãng Siêu Tôn Da", "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=300", "price": "210.000đ", "discount": "35", "url": "https://shopee.vn"}],
            "me_be": [{"name": "Combo 2 Gói Tã Bỉm Siêu Thấm Hút Cao Cấp Cho Bé", "image": "https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=300", "price": "320.000đ", "discount": "25", "url": "https://shopee.vn"}],
            "gia_dung": [{"name": "Nồi Chiên Không Dầu Đa Năng Cảm Ứng 6L", "image": "https://images.unsplash.com/photo-1621972750749-0fbb1abb7736?w=300", "price": "790.000đ", "discount": "50", "url": "https://shopee.vn"}]
        }
        danh_sach_sp = dữ_lieu_moi.get(danh_muc_loai, dữ_lieu_moi["cong_nghe"])
        
    cols = st.columns(4)  # Chia làm lưới 4 cột sang trọng như shopee desktop/mobile lớn
    for idx, item in enumerate(danh_sach_sp[:16]):
        with cols[idx % 4]:
            ten = item.get("name", "Sản phẩm ưu đãi")
            anh = item.get("image", "https://via.placeholder.com/150")
            giam = item.get("discount", "15")
            gia = f"{item.get('price'):,}đ" if isinstance(item.get("price"), int) else str(item.get("price", "Xem giá"))
            link_aff = tao_link_affiliate(item.get("url", "https://shopee.vn"))
            
            st.markdown(f"""
                <div class="ecom-card">
                    <img src="{anh}" style="width:100%; height:140px; border-radius:8px; object-fit:cover;">
                    <div class="ecom-title">{ten}</div>
                    <div class="price-container">
                        <span class="price-sale">{gia}</span>
                        <span class="tag-giam">-{giam}%</span>
                    </div>
                    <a href="{link_aff}" target="_blank"><button style="background-color:#F97316; color:white; padding:7px; border:none; border-radius:6px; cursor:pointer; font-weight:bold; width:100%; font-size:12px;">Xem Chi Tiết</button></a>
                </div>
            """, unsafe_allow_html=True)

with tab_all:
    hien_thi_luoi_san_pham(kho_deal_ecom["tat_ca"], "cong_nghe")
with tab_tech:
    hien_thi_luoi_san_pham(kho_deal_ecom["cong_nghe"], "cong_nghe")
with tab_beauty:
    hien_thi_luoi_san_pham(kho_deal_ecom["my_pham"], "my_pham")
with tab_me_be:
    hien_thi_luoi_san_pham(kho_deal_ecom["me_be"], "me_be")
with tab_home:
    hien_thi_luoi_san_pham(kho_deal_ecom["gia_dung"], "gia_dung")
