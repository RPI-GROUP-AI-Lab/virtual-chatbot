import streamlit as st 
import os
from datetime import datetime
from streamlit_pdf_viewer import pdf_viewer
import time
st.set_page_config(
    page_title="HOME",
    page_icon="🏠",
    layout="wide"
)

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.image("assets/RPI_WHITE.png")

st.markdown("<div class='title'>Welcome to RPiBot</div>", unsafe_allow_html=True)
st.markdown("""
            <div class="description">
            Meet your smart Virtual Assistant! Upload a file, 
            ask a question, and get instant, context-aware 
            answers. Powered by RAG (Retrieval-Augmented Generation),
            this bot combines the best of AI and document search 
            to make finding information a breeze. 
            Fast, intuitive, and designed to boost your 
            productivity...<br>
            GIVE IT A TRY!
            </div>
            """,unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Please select your role...</div>", unsafe_allow_html=True)

# Admin button
admin_btn = st.button("Are you an Admin?", key="admin")

# User button
user_btn = st.button("Are you a User?", key="user")

# Logic based on button clicks
if admin_btn: 
    st.success("Redirecting to Admin panel...")
    time.sleep(1)
    # st.session_state.pop("timenow", None)
    st.session_state.clear()  # Clear session state to reset
    st.session_state["type"] = "Admin"
    st.query_params['page']="admin"
    st.switch_page(os.path.dirname(__file__)+"/admin_guide.py")

if user_btn:
    st.info("User access granted!")
    time.sleep(1)
    st.session_state.clear()  # Clear session state to reset
    st.session_state["file_uploaded"] = "user"
    st.session_state["type"] = "User"
    st.query_params['page']="main"
    st.switch_page(os.path.dirname(__file__)+"/user_guide.py")

st.write("\n")

st.markdown("""
<div style="text-align: center; padding: 20px; font-size: 16px;">
    <b>RPI</b> &copy; 2024 <b>Virtual Assistant(chatbot)</b>. All rights reserved.
</div>
""", unsafe_allow_html=True)

# Page navigation handling
query_params = st.query_params
if "page" in query_params:
    if query_params["page"] == ["admin"]:
        st.experimental_rerun()
    elif query_params["page"] == ["main"]:
        st.experimental_rerun()
