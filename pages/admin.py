import pickle
from pathlib import Path
import os
import re
import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
st.set_page_config(
    page_title="Admin",
    page_icon="🛡️",
    layout="wide"
)
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #EED2FF;
        color: black;
        width:10%;
        padding: 6px 12px;
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
st.sidebar.image("assets/RPI_BLUE.png") 
st.sidebar.page_link("pages/about.py",label="HOME",icon="📖")
st.sidebar.page_link("pages/admin_guide.py",label="ADMIN GUIDE",icon="📚")
st.sidebar.page_link("pages/user_guide.py",label="USER GUIDE",icon="📖")

# Define paths and variables
names = ["Ayan Acharyya"]
usernames = ["admin"]
file_path = Path(__file__).parent / "hashed_pw.pkl"

# Load hashed passwords from file
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {
    "usernames": {
        usernames[0]: {
            "name": names[0],
            "password": hashed_passwords[0]
        }
    }
}

def save_uploaded_file(uploaded_files,username="Ayan"):
    """Saves the uploaded files to the 'uploads' directory."""
    upload_dir = os.path.join(os.getcwd(), f'uploads/{username}')
    
    # Create the directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # List to hold the paths of the saved files
    saved_file_paths = []
    
    # Save each file
    for uploaded_file in uploaded_files:
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        saved_file_paths.append(file_path)
    
    return saved_file_paths

# Initialize authenticator
authenticator = stauth.Authenticate(credentials, "ragbot", "abcdef", cookie_expiry_days=0)

# Login logic
name, authentication_status, username = authenticator.login('main', fields={'Form name': 'Admin Credentials'})
# Handle authentication status
if authentication_status is False:
    st.error("User/Password incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
elif authentication_status:
    st.session_state["timenow"] = str(int(datetime.timestamp(datetime.now())))


    st.markdown(
    """
    <div class="upload-container">
        <h1>UPLOAD A PDF OR TEXT FILE</h1>
        <p class="bold">Welcome, brave soul!</p>
        <p>Help our model become a master of knowledge by uploading your precious files here.</p>
        <p>Think of it as feeding your virtual assistant some tasty data snacks!</p>
    </div>
    """,
    unsafe_allow_html=True)
    files = st.file_uploader(label=" ",type=["pdf", "txt"], accept_multiple_files=True)
    submit_button = st.button(label='Submit')
   
    if submit_button:
        if files:
            file_path = save_uploaded_file(files,re.sub(r'[^a-zA-Z0-9]', "", f'admin{st.session_state["timenow"]}'))
            st.success("File Uploaded Successfully")

            st.session_state["file_uploaded"] = re.sub(r'[^a-zA-Z0-9]',"",st.session_state["timenow"])
            st.query_params['page']="main"
            st.session_state["type"] = "Admin"
            st.switch_page("pages/main.py")   
        else:
            st.warning("Please upload a File!")  
    authenticator.logout("Logout", "main")

else:
    # Display the login form if not authenticated
    name, authentication_status, username = authenticator.login('main', fields={'Form name': 'Login'})

# Check query parameters and redirect if needed
query_params = st.query_params
if "page" in query_params and query_params["page"] == ["main"]:
    st.experimental_rerun()

