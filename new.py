import streamlit as st
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

st.set_page_config(
    page_title='Yare Yare',
    page_icon=':brain:',
    layout='centered',
)

# Get the API key from environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Initialize the ChatGroq model
llm = ChatGroq(
    temperature=0,
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
)

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize a simple document store
if 'document_store' not in st.session_state:
    st.session_state.document_store = []

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f0f2f5;
            font-family: 'Arial', sans-serif;
        }
        .stChatMessage {
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
            max-width: 250%;  /* Limit width for better mobile view */
        }
        .user {
            background-color: #d1e7dd;
            text-align: left;
            margin-left: auto;  /* Align user messages to the right */
        }
        .assistant {
            background-color: #cfe2ff;
            text-align: left;
            margin-right: auto;  /* Align assistant messages to the left */
        }
        .stButton {
            background-color: #0d6efd;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
            width: 100%;  /* Full width for buttons */
            font-size: 16px;  /* Increase font size for better readability */
        }
        .stButton:hover {
            background-color: #0056b3;
        }
        .stChatInput {
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #ced4da;
            width: 100%;  /* Full width for input */
            font-size: 16px;  /* Increase font size for better readability */
        }
        @media (max-width: 600px) {
            .stChatMessage {
                font-size: 14px;  /* Adjust font size for smaller screens */
            }
            .stButton {
                font-size: 14px;  /* Adjust button font size for smaller screens */
            }
            .stChatInput {
                font-size: 14px;  /* Adjust input font size for smaller screens */
            }
        }s 
    </style>
""", unsafe_allow_html=True)


st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=150)  # Adjusted width

st.title('🤖Aizen ChatBot🧠')


for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['text'], unsafe_allow_html=True)

# User input for the chat
user_input = st.chat_input("💬 Ask To Aizen:")
if user_input:
    st.chat_message('user').markdown(user_input)

    relevant_context = "\n".join(st.session_state.document_store[-10:])  # Get the last 10 messages as context

    
    combined_input = f"Context:\n{relevant_context}\nUser Input:\n{user_input}"
    response = llm.invoke(combined_input)  


    st.chat_message('assistant').markdown(response.content)

   
    st.session_state.chat_history.append({'role': 'user', 'text': user_input})
    st.session_state.chat_history.append({'role': 'assistant', 'text': response.content})

    st.session_state.document_store.append(user_input)
    st.session_state.document_store.append(response.content)


if st.button("🗑️ Clear Chat History"):
    st.session_state.chat_history.clear() 
    st.session_state.document_store.clear() 
