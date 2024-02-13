import streamlit as st
import langchain
from langchain_community.chat_models import ChatOllama
from langchain.cache import InMemoryCache
from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings
import os
from PIL import Image
from chroma_main import answer_no_retriever

langchain.cache =  InMemoryCache()

load_dotenv()

CHROMA_DB = "./chroma_db"
MODEL = os.getenv("MODEL", "llama2")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
llm = ChatOllama(base_url=OLLAMA_BASE_URL, model=MODEL, temperature=0.0)
ollama_embeddings = OllamaEmbeddings(base_url=OLLAMA_BASE_URL, model="codellama")



st.button("clear history", type="primary")    
if st.button:
        st.session_state.messages = []


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is your query?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)    
    
    response = answer_no_retriever(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # message_placeholder.markdown(response + "▌")
        message_placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
