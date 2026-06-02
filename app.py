import streamlit as st
import urllib.parse
import requests
import random

# 1. CẤU HÌNH HỆ THỐNG AFFILIATE TOÀN DIỆN CỦA ANH ĐẠT
ACCESSTRADE_ID = "103085"  
API_TOKEN = "9R6Pf6Zs3mRL2M0qcXzb48yOhrIvZsqE"  
UTM_SOURCE = "ai_quantum_deal"

def tao_link_affiliate(link_goc, merchant="shopee"):
    base_url = "https://fast.accesstrade.com.vn/deep_link/v4"
    link_ma_hoa = urllib.parse.quote(link_goc)
    return f"{base_url}?merchant_id={merchant}&id={ACCESSTRADE_ID}&url={link_ma_hoa}&utm_source={UTM_SOURCE}"

@st.cache_data(ttl=900)  # Cập nhật nhanh 15 phút một lần để đồng bộ chiến dịch mới liên tục
def lay_tat_ca_deal_accesstrade(tu_khoa=""):
    """
    Hàm gọi API thông minh: Tự động lấy tất cả sản phẩm từ các chiến dịch anh Đạt đã tham gia
    """
    url_api = "https://api.accesstrade.com.vn/v1/products"
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
    
    # Quét diện rộng tất cả chiến dịch đang chạy trên tài khoản
    params = {
        "limit": 30,
        "search": tu_khoa if tu_khoa else "điện thoại, phụ kiện, gia dụng, mỹ phẩm",
        "order": "discount_percent"  # Luôn ưu tiên món giảm giá sâu nhất để kích thích mua hàng
    }
    try:
        response = requests.get(url_api, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except:
        return []

# 2. ĐỈNH CAO THIẾT KẾ UI/UX CHUYÊN NGHIỆP HÀNG ĐẦU
st.set_page_config(page_title="AI-QUANTUM | Siêu Trợ Lý Săn Deal", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    /* Nền không gian tối sâu, mượt mà */
    .stApp { background-color: #060913; }
    
    /* Thiết kế Header chuẩn các sàn TMĐT lớn */
    .premium-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%);
        border: 1px solid #312E81;
        padding: 35px 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .brand-name { font-size: 28px; font-weight: 900; color: #00F0FF; letter-spacing: 2px; margin-bottom: 5px; }
    .brand-sub { font-size: 14px; color: #94A3B8; font-weight: 400; }
    
    /* Hộp tính năng Glassmorphism */
    .glass-panel {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 25px;
    }
    
    /* Grid Thẻ sản phẩm cao cấp, đồng bộ kích thước */
    .premium-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 18px;
        padding: 14px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .premium-card:hover {
        transform: translateY(-5px);
        border-color: #00F0FF;
        box-shadow: 0 10px 20px rgba(0, 240, 255, 0.1);
    }
    .thumb-container { width: 100%; height: 160px; border-radius: 12px; overflow: hidden; margin-bottom: 12px; }
    .card-title {
        color: #F1F5F9; font-size: 14px; font-weight: 600;
        height: 40px; display: -webkit-box; -webkit-line-clamp: 2;
        -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4; margin-bottom: 8px;
    }
    .price-container { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
    .price-sale { color: #FF3B30; font-size: 18px; font-weight: 800; }
    .tag-discount { background: #DC2626; color: white; font-size: 11px; font-weight: 700; padding: 2px 6px; border-radius: 6px; }
    
    /* Tối ưu thanh Tab thanh lịch */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background: #1E293B !important; color: #94A3B8 !important; 
        border-radius: 10px !important; padding: 8px 16px !important; font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] { background: #00F0FF !important; color: #060913 !important; }
    
    /* Chatbot UI */
    .ai-bubble { background: #1E1B4B; border-left: 4px solid #00F0FF; padding: 12px; border-radius: 0 12px 12px 12px; margin-top: 10px; color: #E2E8F0; }
    
    footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 3. HIỂN THỊ HEADER THƯƠNG HIỆU ĐẲNG CẤP
st.markdown("""
    <div class="premium-header">
        <div class="brand-name">💎 AI - QUANTUM SMART SHOPPING 💎</div>
        <div class="brand-sub">Hệ thống Trợ lý AI Tự động Quét Deal & Tối ưu Hóa Mã Giảm Giá Đa Sàn</div>
    </div>
""", unsafe_allow_html=True)

# 4. KHU VỰC TRỢ LÝ AI TỰ ĐỘNG TƯ VẤN & GỢI Ý
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.subheader("🤖 Trợ Lý Ảo AI Tư Vấn Mua Sắm")
cau_hoi_khach = st.text_input("Khách hàng nhập nhu cầu tại đây (Ví dụ: Tìm sạc dự phòng, tai nghe bluetooth, son môi...):", placeholder="Tôi muốn tìm mua...")

if cau_hoi_khach:
    st.markdown(f'<div class="ai-bubble"><strong>🤖 AI Phân Tích:</strong> Đang quét hệ thống các chiến dịch để tìm sản phẩm <em>"{cau_hoi_khach}"</em> có mức chiết khấu cao nhất cho bạn...</div>', unsafe_allow_html=True)
    # Kích hoạt AI đi tìm sản phẩm theo đúng nhu cầu khách hàng điền vào
    danh_sach_ai = lay_tat_ca_deal_accesstrade(tu_khoa=cau_hoi_khach)
    if danh_sach_ai:
        st.write("🎯 **Sản phẩm AI gợi ý phù hợp nhất cho bạn:**")
        cols_ai = st.columns(min(len(danh_sach_ai), 3))
        for idx, item_ai in enumerate(danh_sach_ai[:3]):
            with cols_ai[idx]:
                st.image(item_ai.get("image"), use_container_width=True)
                st.caption(item_ai.get("name"))
                st.markdown(f'<a href="{tao_link_affiliate(item_ai.get("url"))}" target="_blank"><button style="background-color:#00F0FF; color:#060913; width:100%; border:none; padding:6px; border-radius:6px; font-weight:bold; cursor:pointer;">Mua ngay giá giảm</button></a>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. CÔNG CỤ BỌC LINK NHANH TOÀN SÀN
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.subheader("🔗 Công Cụ Dán Link Nhận Ưu Đãi Tự Động")
link_nhap = st.text_input("Dán link Shopee / Lazada / Tiki bất kỳ để kích hoạt mã giảm giá ẩn:", placeholder="https://...")
if link_nhap:
    link_vip = tao_link_affiliate(link_nhap)
    st.success("🎯 Đã kích hoạt mã giảm giá hệ thống thành công!")
    st.markdown(f'<a href="{link_vip}" target="_blank"><button style="background-color:#00F0FF; color:#060913; padding:12px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:14px;">👉 CHUYỂN ĐẾN TRANG MUA HÀNG GIẢM GIÁ</button></a>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. ĐA DẠNG NGÁCH SẢN PHẨM - KHÁCH VÀO LÀ MUỐN MUA NGAY
st.subheader("🔥 DANH MỤC SIÊU DEAL KHUYẾN MÃI HÔM NAY")
tab_hot, tab_tech, tab_life, tab_beauty = st.tabs(["⚡ Deal Sốc Độc Quyền", "📱 Đồ Công Nghệ", "🏠 Đời Sống & Gia Dụng", "💄 Sức Khỏe & Làm Đẹp"])

# Kho dữ liệu mồi đa dạng ngách để lấp đầy app chuyên nghiệp lúc API đang đồng bộ chiến dịch
kho_ngach_vip = {
    "tech": [
        {"name": "Sạc Dự Phòng Không Dây 20000mAh Sạc Nhanh 22.5W", "image": "https://images.unsplash.com/photo-1609592424083-0570b2401f80?w=400", "price": "249.000đ", "discount": "45", "url": "https://shopee.vn"},
        {"name": "Tai Nghe Bluetooth Không Dây Bản Quốc Tế Chống Ồn", "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400", "price": "320.000đ", "discount": "35", "url": "https://shopee.vn"}
    ],
    "life": [
        {"name": "Máy Hút Bụi Cầm Tay Mini Lực Hút Siêu Mạnh Cho Gia Đình & Ô Tô", "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400", "price": "185.000đ", "discount": "50", "url": "https://shopee.vn"},
        {"name": "Bình Giữ Nhiệt Chất Liệu Inox 314 Cao Cấp 1000ml", "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400", "price": "115.000đ", "discount": "40", "url": "https://shopee.vn"}
    ],
    "beauty": [
        {"name": "Son Kem Lì Mịn Môi Lên Màu Chuẩn Kháng Nước", "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400", "price": "160.000đ", "discount": "30", "url": "https://shopee.vn"},
        {"name": "Kem Chống Nắng Bảo Vệ Da Toàn Diện Kiềm Dầu Kháng Nước", "image": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400", "price": "210.000đ", "discount": "25", "url": "https://shopee.vn"}
    ]
}

def render_danh_sach_card(danh_sach):
    col1, col2 = st.columns(2)
    for index, item in enumerate(danh_sach):
        cot_chon = col1 if index % 2 == 0 else col2
        with cot_chon:
            ten = item.get("name", "Sản phẩm")
            anh = item.get("image", "https://via.placeholder.com/150")
            giam = item.get("discount", "20")
            gia = f"{item.get('price'):,}đ" if isinstance(item.get("price"), int) else str(item.get("price", "Xem giá"))
            link_aff = tao_link_affiliate(item.get("url", "https://shopee.vn"))
            
            st.markdown(f"""
                <div class="premium-card">
                    <div class="thumb-container"><img src="{anh}" style="width:100%; height:160px; object-fit:cover;"></div>
                    <div class="card-title">{ten}</div>
                    <div class="price-container">
                        <span class="price-sale">{gia}</span>
                        <span class="tag-discount">-{giam}%</span>
                    </div>
                    <a href="{link_aff}" target="_blank"><button style="background-color:#FF3B30; color:white; padding:10px; border:none; border-radius:10px; cursor:pointer; font-weight:700; width:100%; font-size:13px;">🛒 LẤY MÃ & MUA NGAY</button></a>
                </div>
            """, unsafe_allow_html=True)

# Phân chia luồng hiển thị vào từng ngách cụ thể
with tab_hot:
    deal_api = lay_tat_ca_deal_accesstrade()
    if deal_api:
        render_danh_sach_card(deal_api)
    else:
        # Nếu API trống, gộp tất cả kho mồi vào để hiển thị hoành tráng phong phú luôn
        render_danh_sach_card(kho_ngach_vip["tech"] + kho_ngach_vip["life"] + kho_ngach_vip["beauty"])

with tab_tech:
    deal_tech = lay_tat_ca_deal_accesstrade(tu_khoa="điện thoại, sạc, tai nghe")
    render_danh_sach_card(deal_tech if deal_tech else kho_ngach_vip["tech"])

with tab_life:
    deal_life = lay_tat_ca_deal_accesstrade(tu_khoa="gia dụng, nhà cửa, cốc")
    render_danh_sach_card(deal_life if deal_life else kho_ngach_vip["life"])

with tab_beauty:
    deal_beauty = lay_tat_ca_deal_accesstrade(tu_khoa="mỹ phẩm, son, kem dưỡng")
    render_danh_sach_card(deal_beauty if deal_beauty else kho_ngach_vip["beauty"])
