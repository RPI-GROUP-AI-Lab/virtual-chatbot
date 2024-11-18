import streamlit as st
import os 
st.set_page_config(
    page_title="Admin Guide",
    page_icon="📕",
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
st.markdown("""<style>
            .admin-guide-container{
    background-color: #f1e3d3;
    color: black;
    border: solid 3px black;
    border-radius: 5px;
    padding:10px;
    margin-bottom:10px;
}
            
            </style><div class="admin-guide-container">
## 🛠️ **Admin Access: The Power User's Guide**

### Who Can Use Admin? 👑
If you hold the **Admin Credentials**, congratulations—you’ve unlocked the gateway to ultimate control! The **Admin Site** is your command center, where you can manage, upload, and interact with your data like a pro.

### What Can You Do as an Admin? 🚀
As an admin, you have exclusive access to a range of powerful features:

1. **Upload New Files** 📂:
   Feed the model with fresh data by uploading your own files. Whether it’s documents, notes, or any other text, the admin portal is where you start the process. Just drag and drop your files, and watch the magic happen.

2. **Start Chatting** 🗣️:
   Once your files are uploaded, dive into an interactive Q&A session. The model is ready to assist you with answers based on the newly uploaded content. Think of it as having a supercharged, personalized assistant at your fingertips.

### Why Choose Admin? 💡
The **Admin** role isn’t just about having access—it’s about having the **power** to shape the model’s knowledge base. By uploading specific documents, you’re not just interacting with the AI; you’re teaching it, making it smarter and more relevant to your needs.

### How to Access Admin 🛡️
Simply log in with your **Admin Credentials**, and you’ll be transported to the admin site. From there, the controls are in your hands. Manage, upload, and chat with confidence!

---

🌟 **Remember**: With great power comes great responsibility. Make sure to use your admin powers wisely, and happy data wrangling! 

</div>
""" ,unsafe_allow_html=True)

button = st.button("Proceed")
if button:
    st.switch_page(os.path.dirname(__file__)+"/admin.py")


