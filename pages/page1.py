import streamlit as st
from Bot_main.Text_summary import text_summary

st.markdown("# Chức năng tóm tắt văn bản của bot")
st.sidebar.markdown("# Text summary")

if "summary_history" not in st.session_state:
    st.session_state.summary_history = []
    st.session_state.upload_counter = 0

for chat_message in st.session_state.summary_history:
    with st.chat_message(chat_message["role"]):
        if isinstance(chat_message["content"], str):
            st.markdown(chat_message["content"])

if user_input := st.chat_input("Nhập văn bản cần tóm tắt", max_chars=12000):
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.summary_history.append({"role": "user", "content": user_input})

    response = text_summary(user_input)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.summary_history.append({"role": "assistant", "content": response})
