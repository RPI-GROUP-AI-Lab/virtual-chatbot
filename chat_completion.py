# import os
# from langchain_groq import ChatGroq
# from langchain.prompts import (
#     SystemMessagePromptTemplate,
#     HumanMessagePromptTemplate,
#     ChatPromptTemplate,
#     MessagesPlaceholder
# )
# from langchain.chains import ConversationChain
# from langchain.chains.conversation.memory import ConversationBufferWindowMemory
# from dotenv import load_dotenv
# import streamlit as st
# import asyncio
# # Load environment variables
# load_dotenv()
# groq_api_key = os.getenv('GROQ_API_KEY')

# class ChatCompletion:
#     def __init__(self, db, file_path=None):

#         self.__llm = ChatGroq(
#             groq_api_key=groq_api_key, 
#             # model_name="Llama3-8b-8192",  
#             model_name =  "Llama-3.1-70b-versatile",
#             # model_name = "llama3-groq-70b-8192-tool-use-preview",
#             temperature=0.7,
#             max_tokens=1024
#         )
#         self.db = db 

#     async def get_answer(self, query):
#         return await self.chat_completion(query.strip())

#     async def find_match(self, input):
#         results = self.db.similarity_search(input, k=5)
#         return "\n".join(result.page_content for result in results)

#     async def chat_completion(self, query):
#         if 'buffer_memory' not in st.session_state:
#             st.session_state.buffer_memory = ConversationBufferWindowMemory(k=1, return_messages=True)
#             # k=<past_conversation_number>

#         @st.cache_resource
#         def setup_template():
#             self.__llm = ChatGroq(
#                 groq_api_key=groq_api_key, 
#                 # model_name="Llama3-8b-8192",
#                 model_name =  "Llama-3.1-70b-versatile",
#                 # model_name = "llama3-groq-70b-8192-tool-use-preview",

#                 temperature=0.7,
#                 max_tokens=1024,


#             )
#             system_msg_template = SystemMessagePromptTemplate.from_template(
#                 template=""" Answer the following questions using only the provided context. Provide the most accurate and relevant response possible, responding in a professional and courteous manner. If the context does not contain the information needed to answer the question, please indicate that you do not know the answer based on the available information. \n"""
#             )
#             human_msg_template = HumanMessagePromptTemplate.from_template(template="\n{input}")
#             prompt_template = ChatPromptTemplate.from_messages(
#                 [system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template]
#             )
#             return prompt_template

#         conversation = ConversationChain(
#             memory=st.session_state.buffer_memory, 
#             prompt=setup_template(), 
#             llm=self.__llm, 
#             verbose=True
#         )
        
#         print("Started finding query match....")
#         context = await self.find_match(query)
#         context = context.replace("\n"," ")
#         print("Ended finding query match....")

#         print("Started Predicting the output...")
#         try:
#             response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")            
#             print("Ended Predicting the output...")
#             return response
#         except Exception as e:
#             print(e)
#             return f"Some Error occured! Please try again!"


import os
from dotenv import load_dotenv
import streamlit as st
from groq import AsyncGroq

# Load environment variables
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')


class ChatCompletion:
    def __init__(self, db, file_path=None):

        self.db = db 

    def get_answer(self,query):
        return self.chat_completion(query)

    def find_match(self, input):
        results = self.db.similarity_search(input, k=5)
        return "\n".join(result.page_content for result in results)

    def chat_completion(self,query):
        
        print("Started finding query match....")
        context = self.find_match(query)
        context = context.replace("\n"," ")
        print("Ended finding query match....")
        return context
        

