import streamlit as st

st.markdown("# Hình ảnh một số chức năng tiêu biểu của bot")
st.sidebar.markdown("# Demo images")

# Tạo hàng đầu tiên với 3 cột
col1, col2 = st.columns(2)

with col1:
    st.write("Chào hỏi với bot")
    st.image("imgs/image1.png", use_column_width=True)

with col2:
    st.write("Chức năng thời tiết của bot")
    st.image("imgs/image2.png", use_column_width=True)

# Tạo hàng đầu tiên với 3 cột
col3, col4 = st.columns(2)

with col3:
    st.write("Chức năng thời tiết của bot")
    st.image("imgs/image3.png", use_column_width=True)

with col4:
    st.write("Chức năng tóm tắt văn bản của bot")
    st.image("imgs/image4.png", use_column_width=True)
