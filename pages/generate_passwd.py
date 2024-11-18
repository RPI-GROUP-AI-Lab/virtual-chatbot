import pickle 
from pathlib import Path
import streamlit_authenticator as stauth 

names =["Ayan Acharyya"]
username = ["admin"]
passwords = ["Admin@123"]

hashed_passwords = stauth.utilities.hasher.Hasher(passwords).generate()
file_path = Path(__file__).parent / "hashed_pw.pkl"

with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)
