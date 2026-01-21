import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Công cụ số của anh Đạt", page_icon="🚀")

st.title("Chào mừng đến với cửa hàng số của anh Đạt 🎯")
st.write("Đây là ứng dụng thực tế đầu tiên chạy từ điện thoại Android.")

# Tạo một form nhập liệu đơn giản
ten_khach = st.text_input("Nhập tên khách hàng của anh:")
san_pham = st.selectbox("Chọn loại sản phẩm số:", ["Ebook", "Video Course", "Template Canva"])

if st.button("Tạo hóa đơn thử nghiệm"):
    st.balloons()
    st.success(f"Khách hàng: {ten_khach}")
    st.info(f"Sản phẩm đã chọn: {san_pham}")
    st.write("Cảm ơn anh đã tin dùng công cụ của tôi!")
