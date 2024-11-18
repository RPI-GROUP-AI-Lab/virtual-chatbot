import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import os 
st.set_page_config(
    page_title="User Guide",
    page_icon="📖",
    layout="wide"
)
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.image("assets/RPI_BLUE.png") 

st.sidebar.page_link("pages/about.py",label="HOME",icon="🏠")

# st.markdown(
#     """
#     <style>
#     .stButton>button {
#         background-color: #EED2FF;
#         color: black;
#         padding: 6px 12px;
#         font-size: 18px;
#         border: solid white 2px;
#         border-radius: 8px;
#         cursor: pointer;
#         box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
st.markdown("""
    <style>
        .user-guide-container{
            background-color: #D1E3F8;
            color: #1F3A57;
            border: solid 3px black;
            border-radius: 5px;
            padding:10px;
            margin-bottom:10px;
        }
        
            
        </style><div class="user-guide-container">
## 📖 **User Guide: Getting Started with Your GPS Log Book Assistant**

### Welcome, Explorer! 🌍
This app is your personal assistant, ready to help you navigate and understand the **GPS Log Book**. Whether you're a seasoned pro or just getting started, we've got you covered.

### What Can You Do Here? 🤔
As a user, you have access to the following features:

1. **Ask Questions** ❓:
   Need help with something specific? Simply ask your question, and our assistant will provide answers based on the GPS Log Book. Whether it's a quick reference or detailed information, your assistant is here to help.

2. **Explore the Manual** 🔍:
   Dive deeper into the **GPS Log Book** by exploring the user manual. You can read through it at your own pace, searching for specific sections or just getting an overview.

### Why Use This Assistant? 💼
This tool is designed to make your life easier by providing instant access to the information you need. It's like having a knowledgeable guide by your side, ready to assist with any questions you may have about your GPS Log Book.

### Getting Started 🛠️
No need to upload anything—everything you need is already loaded and ready to go. Simply type your question into the chat, and start exploring!

---

<div class="quick-tip">
            🌟 **Quick Tip**: If you want to get the most out of your GPS Log Book, don't hesitate to ask detailed questions.<br>
            The more specific you are, the better the answers will be!
</div>

<div class="disclaimer">
            📌 **Disclaimer**: The model has been trained on a PDF document containing information about the GPS Log Book. To better understand the context and structure of the data, we recommend downloading the same PDF.<br>
            This will help you ask more targeted and effective questions based on the document.<br><br>
            <strong>Feel free to explore and experiment after reviewing the PDF!</strong>
</div></div>""",unsafe_allow_html=True)

with open("manual.pdf", "rb") as pdf_file:
    pdf_bytes = pdf_file.read()
    
    # Provide a download button for the PDF
    st.download_button(
        label="Download the PDF",
        data=pdf_bytes,
        file_name="your_file.pdf",
        mime="application/octet-stream"
    )
    

button = st.button("Proceed")
if button:
    st.switch_page(os.path.dirname(__file__)+"/main.py")


