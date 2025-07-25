import streamlit as st
import os
from sales_chatbot import SalesPredictionChatbot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple page configuration
st.set_page_config(
    page_title="Sales Prediction Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Minimal CSS
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
        background-color: white;
    }
    
    .chat-message {
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        font-family: 'Arial', sans-serif;
        color: black;
        border: 1px solid #ddd;
    }
    
    .user-message {
        background-color: white;
        text-align: right;
        border-left: 4px solid #007bff;
    }
    
    .bot-message {
        background-color: white;
        text-align: left;
        border-left: 4px solid #28a745;
    }
    
    /* Ensure all text is black */
    .stMarkdown, .stText, p, div, span, h1, h2, h3 {
        color: black !important;
    }
    
    /* Input field styling */
    .stChatInput > div > div > div > div {
        background-color: white !important;
        color: black !important;
        border: 2px solid #ddd !important;
    }
    
    .stChatInput input {
        background-color: white !important;
        color: black !important;
    }
    
    /* Title styling */
    .stTitle {
        color: black !important;
    }
    
    /* Hide Streamlit branding */
    .stDeployButton { display: none; }
    #MainMenu { display: none; }
    footer { display: none; }
    header { display: none; }
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Initialize the chatbot with API key"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your-openai-api-key-here':
        return None
    
    try:
        chatbot = SalesPredictionChatbot(api_key)
        return chatbot
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")
        return None

def main():
    """Simple chatbot interface"""
    
    # Simple title
    st.title("💬 Sales Prediction Chatbot")
    
    # Initialize chatbot
    chatbot = initialize_chatbot()
    
    if not chatbot:
        st.error("Please configure your OpenAI API key in the .env file")
        return
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message"><strong>Bot:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask about sales predictions..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get bot response
        with st.spinner("Thinking..."):
            response = chatbot.handle_query(prompt)
        
        # Add bot response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update display
        st.rerun()

if __name__ == "__main__":
    main()
