import streamlit as st
from Bot_main.use_models import get_responses
import post_install

st.markdown("# Chat bot GALAXY")
st.sidebar.markdown("# GALAXY🧞‍♂️")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tin nhắn gửi tới GALAXY", max_chars=6000):
    with st.chat_message("user"):
        st.markdown(prompt)

    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = get_responses(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    # Append assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
