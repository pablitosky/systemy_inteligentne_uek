import streamlit as st
import requests
import os
from agent import call_agent, response_stream
from vectordb import client

st.set_page_config(
    page_title="Agent App",
    page_icon=":robot:",
    layout="wide",
)
st.title("Agent App")
# --- strona ---

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        config = {"configurable": {"thread_id": "55"}}
        response = call_agent(prompt, config=config)
        gen = response_stream(response)
        st.write_stream(gen)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})