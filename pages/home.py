import streamlit as st
import os
from datetime import datetime
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.image("assets/RPI_BLUE.png") 
st.sidebar.page_link("pages/admin.py",label="ADMIN",icon="🛡️")
st.sidebar.page_link("pages/home.py",label="HOME",icon="🏠")
st.sidebar.page_link("pages/about.py",label="ABOUT",icon="📚")
st.sidebar.page_link("main.py",label="CHAT",icon="💬")

# Custom button style
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: violet;
        color: black;
        padding: 12px 24px;
        font-size: 18px;
        border: solid white 2px;
        border-radius: 8px;
        cursor: pointer;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Authentication and File Upload")

# Header for the section
st.header("View As")

# Layout columns for buttons
col1, col2 = st.columns(2)

# Admin button handling
with col1:
    if st.button("ADMIN"):
        st.session_state.pop("timenow", None)
        st.session_state.clear()  # Clear session state to reset
        st.session_state["timenow"] = str(int(datetime.timestamp(datetime.now())))

        st.write("Loading Admin Interface...")
        st.session_state["type"] = "Admin"
        st.query_params['page']="admin"
        st.switch_page(os.path.dirname(__file__)+"/admin.py")

# User button handling
with col2:
    if st.button("USER"):
        st.session_state.clear()  # Clear session state to reset
        st.session_state["file_uploaded"] = "user"
        st.write("User session initialized")
        st.session_state["type"] = "User"
        st.query_params['page']="main"
        st.switch_page(os.getcwd()+"/main.py")

# Optional: Footer or additional decorations
st.markdown("---")
st.markdown("**Admin** - Empower your team with admin privileges to upload and manage documents.")
st.markdown("**User** - Explore and test the bot’s capabilities without admin credentials.")

# Page navigation handling
query_params = st.query_params
if "page" in query_params:
    if query_params["page"] == ["admin"]:
        st.experimental_rerun()
    elif query_params["page"] == ["main"]:
        st.experimental_rerun()
