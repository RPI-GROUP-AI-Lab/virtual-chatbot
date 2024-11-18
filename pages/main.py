import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import streamlit as st
from streamlit_chat import message
# from .. import chat_completion
from chat_completion import ChatCompletion
# from ..chat_completion import ChatCompletion
import vectordb_2
import asyncio
from datetime import datetime
from groq import AsyncGroq
import nest_asyncio
nest_asyncio.apply()
st.set_page_config(
    page_title="Virtual Assistant",
    page_icon="🤖",
)

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.image("assets/RPI_BLUE.png") 

st.sidebar.page_link("pages/about.py",label="HOME",icon="🏠")
st.sidebar.page_link("pages/admin.py",label="ADMIN",icon="🛡️")

st.sidebar.page_link("pages/admin_guide.py",label="ADMIN GUIDE",icon="📕")
st.sidebar.page_link("pages/user_guide.py",label="USER GUIDE",icon="📖")


llm_client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])

async def chat():
    stream = await llm_client.chat.completions.create(
        model=  "Llama-3.1-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
            messages=[[{"role": "system",
                       "content": (
            """'You are an assistant that answers questions. Use the
    following pieces of retrieved context to answer the question. Some pieces of context
    may be irrelevant, in which case you should not use them to form the answer."""        )},                        
        {
                            "role": "user",
                            "content": f"Context: {st.session_state.context}"
                        },
                        {
                            "role": m["role"],
                            "content": f"User Query: {st.session_state.messages[-1]}"
                        },
                        {
                            "role": "assistant",
                            "content": "Answer based on the context:"
                        }
                    ] for m in st.session_state.messages][0],
                        stream=True
    )
    async for chunk in stream:
        chunk_text = chunk.choices[0].delta.content
        if chunk_text is not None:
            yield chunk_text
        else:
            yield ""


def async_to_sync(async_gen):
    loop = asyncio.get_event_loop()

    async def async_wrapper():
        async for item in async_gen():
            yield item

    async_gen_instance = async_wrapper()
    while True:
        try:
            yield loop.run_until_complete(async_gen_instance.__anext__())
        except StopAsyncIteration:
            break

async def main():
    
    st.title("VIRTUAL ASSISTANT(CHATBOT)")
    if "model_name" not in st.session_state:
        st.session_state["model_name"] = "Llama-3.1-70b-versatile"

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]


    for message in st.session_state.messages:
        with st.chat_message(message["role"],avatar="🤖" if message["role"]=="assistant" else "🧑🏻‍💻"):
            st.markdown(message["content"])
            

    if "file_uploaded" not in st.session_state:
        st.switch_page("pages/about.py")

    # file_path = f"uploads/{st.session_state['file_uploaded']}"

    @st.cache_resource()
    def initialize_vector_database(username):
        ragpipeline = vectordb_2.Rag(username)
        return ragpipeline.get_embeddings_store()

    # Initialize vector database if not already cached
    if 'vectorstore' not in st.session_state:
        st.session_state.vectorstore = initialize_vector_database(f"admin{st.session_state['file_uploaded']}")
            

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        # print(st.session_state.messages)
        with st.chat_message("user",avatar="🧑🏻‍💻"):
            st.markdown(prompt)
        llm = ChatCompletion(st.session_state.vectorstore)
        st.session_state.context = llm.get_answer(prompt)
        # print(st.session_state.context)
        with st.chat_message("assistant",avatar="🤖"):
            stream = chat

            response = st.write_stream(async_to_sync(stream))
        st.session_state.messages.append({"role": "assistant", "content": response})
    
if __name__ == "__main__":
    asyncio.run(main())


