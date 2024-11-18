import os,re
from langchain_community.document_loaders import DirectoryLoader
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
import streamlit as st
import numpy as np
import shutil
class Rag:
    def __init__(self,username):
        self.username = username
        self.embedding_model = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    def get_embeddings_store(self):
        filename = f"{self.username}.faiss"
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        
        DB_FOLDER_PATH = os.path.join(ROOT_DIR,"database")

        DB_PATH = os.path.join(DB_FOLDER_PATH,filename)

        if not os.path.exists(DB_PATH):
            self.vector_store(os.path.join(os.path.join(ROOT_DIR,"uploads"),f"{self.username}"),DB_FOLDER_PATH)
        else:
            print("DB Exists!")
        db = FAISS.load_local(folder_path=DB_FOLDER_PATH, embeddings=self.embedding_model,allow_dangerous_deserialization=True,index_name=self.username)
    
        return db
    def get_loader(self):
        loader = [self.create_directory_loader(".pdf",f"./uploads/{self.username}/"),self.create_directory_loader(".txt",f"./uploads/{self.username}/")]
        return loader

    def get_chunks(self):
        content = self.get_loader() # content = [pdf_loader,txt_loader]
        # content = self.get_text(content)
        print(f"Content : {content}")
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=300)
        chunks = text_splitter.split_documents(content[0].load())
        try:
            chunks.append(text_splitter.split_documents(content[1].load())[0])
            return chunks
        except:
            return chunks
        # chunks_text = text_splitter.split_documents(content[1].load())
        # chunks.append(chunks_text)
        print(len(chunks))
        return chunks
    def create_directory_loader(self,file_type, directory_path):
        loaders = {
        '.pdf': PyPDFLoader,
        '.txt' : TextLoader
        }
        return DirectoryLoader(
            path=directory_path,
            glob=f"**/*{file_type}",
            loader_cls=loaders[file_type],
            show_progress=True
            ) 
        
    def vector_store(self,filename,DB_FOLDER_PATH,):
        

        self.chunks = self.get_chunks()
        print("Creating Embeddings...")
        faiss_db=FAISS.from_documents(self.chunks,self.embedding_model)
        print("Embeddings done !")
        faiss_db.save_local(folder_path=DB_FOLDER_PATH,index_name=f"{self.username}")
        
        print("Saved to local!")
        if st.session_state["type"] == "Admin":
            shutil.rmtree(filename)
            print("File deleted from local!")