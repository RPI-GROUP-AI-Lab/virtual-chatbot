# %%
# from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import os 

# load_dotenv()
# os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")

file_type=".pdf"
directory_path = "uploads/adminuser/"
loaders = {
        '.pdf': PyPDFLoader,
        '.txt' : TextLoader
        }
loader_pdf = DirectoryLoader(
            path=directory_path,
            glob=f"**/*{'.pdf'}",
            loader_cls=loaders['.pdf'],
            show_progress=True
            ) 
loader_txt = DirectoryLoader(
            path=directory_path,
            glob=f"**/*{'.txt'}",
            loader_cls=loaders['.txt'],
            show_progress=True
            ) 
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=300)
chunks = text_splitter.split_documents(loader_pdf.load())
chunks.append(text_splitter.split_documents(loader_txt.load()))
print(chunks)

# %%
