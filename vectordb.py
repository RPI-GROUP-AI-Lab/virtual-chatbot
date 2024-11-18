# import os,re
# from dotenv import load_dotenv
# from langchain_community.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# from langchain_community.vectorstores import FAISS
# from sentence_transformers import SentenceTransformer
# import streamlit as st
# import numpy as np

# load_dotenv()
# os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")

# class InvalidFileTypeError(Exception):
#     def __init__(self, message="Not a PDF or DOC type!"):
#         self.message = message
#         super().__init__(self.message)

# class Rag:
#     _instance = None
#     def __init__(self,file):
#         self.file = file
#         self.embedding_model = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
#         # self.embedding_model = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-mpnet-base-v2')
#         # self.embedding_model = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
#         # self.embedding_model = HuggingFaceEmbeddings(model_name = 'sentence-transformers/sentence-t5-large')

#     def get_embeddings_store(self,filename=None):
#         ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        
#         DB_FOLDER_PATH = os.path.join(ROOT_DIR,"database")

#         DB_PATH = os.path.join(DB_FOLDER_PATH,f"{filename}.faiss")

#         if not os.path.exists(DB_PATH):
#             self.vector_store(self.file, filename,DB_FOLDER_PATH)
#         else:
#             print("DB Exists!")
#         db = FAISS.load_local(folder_path=DB_FOLDER_PATH, embeddings=self.embedding_model,allow_dangerous_deserialization=True,index_name=filename)

#         return db

#     ##################################################
#     # (FOR TESTING PURPOSE)
#     def find_match(self,input):
#         results = self.db.similarity_search(input)
#         return results
#     #################################################
    
    
#     def get_extension(self,file_get_extension):
#         return ".txt" if file_get_extension.endswith(".txt") else (".pdf" if file_get_extension.endswith(".pdf") else ".other")
    
#     def get_text(self,loader): 
#         # Extract content from each page
#         for page in loader:
#             re.sub(r'(\.{2,}|)', '', page.page_content)
        
#     def get_content(self,file_get_content):
#         self.extension = self.get_extension(file_get_content)
#         if self.extension==".txt":
#             # return TextLoader(file_get_content).load()
#             return TextLoader(file_get_content).load()
#         elif self.extension==".pdf":
#             # document = PyPDFLoader(file_get_content).load()
#             return PyPDFLoader(file_get_content).load()
#         else:
#             raise InvalidFileTypeError()

#     def get_chunks(self,file_get_chunks):
#         content = self.get_content(file_get_chunks)
#         self.get_text(content)
#         print(f"Content : {content}")
#         text_splitter=RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=300)
#         chunks = text_splitter.split_documents(content)
#         print(len(chunks))
#         return chunks
    
#     def vector_store(self,file_vector_store,filename,folder):
#         self.chunks = self.get_chunks(file_vector_store)
#         print("Creating Embeddings...")
#         faiss_db=FAISS.from_documents(self.chunks,self.embedding_model)
#         print("Embeddings done !")
#         faiss_db.save_local(folder_path=folder,index_name=filename)
        
#         print("Saved to local!")
#         if st.session_state["type"] == "Admin":
#             os.remove(self.file)
#             print("File deleted from local!")

        

# if __name__=="__main__":
#     obj = Rag("data/matrix_content.txt")
#     obj.get_embeddings_store("matrix_content")
#     result = obj.find_match("Who is the president of russia ? ")
#     print(result)


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

load_dotenv()
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")

class InvalidFileTypeError(Exception):
    def __init__(self, message="Not a PDF or DOC type!"):
        self.message = message
        super().__init__(self.message)

class Rag:
    _instance = None
    def __init__(self,file):
        self.file = file
        self.embedding_model = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
        # self.embedding_model = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-mpnet-base-v2')
        # self.embedding_model = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
        # self.embedding_model = HuggingFaceEmbeddings(model_name = 'sentence-transformers/sentence-t5-large')

    def get_embeddings_store(self,filename=None):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        
        DB_FOLDER_PATH = os.path.join(ROOT_DIR,"database")

        DB_PATH = os.path.join(DB_FOLDER_PATH,f"{filename}.faiss")

        if not os.path.exists(DB_PATH):
            self.vector_store(self.file, filename,DB_FOLDER_PATH)
        else:
            print("DB Exists!")
        db = FAISS.load_local(folder_path=DB_FOLDER_PATH, embeddings=self.embedding_model,allow_dangerous_deserialization=True,index_name=filename)

        return db

    ##################################################
    # (FOR TESTING PURPOSE)
    def find_match(self,input):
        self.db = self.get_embeddings_store("matrix_content")
        results = self.db.similarity_search_with_score(input)
        return results
    #################################################
    
    
    def get_extension(self,file_get_extension):
        return ".txt" if file_get_extension.endswith(".txt") else (".pdf" if file_get_extension.endswith(".pdf") else ".other")
    
    def get_text(self,loader): 
        docs = loader.load()
        content = " "
        # Extract content from each page
        for page in range(len(docs)):
            content += re.sub(r'(\.{3,})', '', docs[page].page_content)
        return content
    def get_content(self,file_get_content):
        loader = self.create_directory_loader(".pdf","uploads/")
        return loader.load()
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
    def get_chunks(self,file_get_chunks):
        content = self.get_content(file_get_chunks)
        # content = self.get_text(content)
        print(f"Content : {content}")
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=300)
        chunks = text_splitter.split_documents(content)
        print(len(chunks))
        return chunks
    
    def vector_store(self,file_vector_store,filename,folder):
        self.chunks = self.get_chunks(file_vector_store)
        print("Creating Embeddings...")
        faiss_db=FAISS.from_documents(self.chunks,self.embedding_model)
        print("Embeddings done !")
        faiss_db.save_local(folder_path=folder,index_name=filename)
        
        print("Saved to local!")
        # if st.session_state["type"] == "Admin":
        #     os.remove(self.file)
        #     print("File deleted from local!")

        

if __name__=="__main__":
    obj = Rag("data/matrix_content.txt")
    obj.get_embeddings_store("matrix_content")
    print("Similarioty Search >>>>>>>>>>>>>>>>>>")
    result = obj.find_match("Who is the president of russia ? ")
    print(result)
