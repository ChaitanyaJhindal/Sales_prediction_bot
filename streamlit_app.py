import streamlit as st
import os
from sales_chatbot import SalesPredictionChatbot
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Streamlit page configuration
st.set_page_config(
    page_title="Sales Prediction Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for the new UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    body {
        font-family: 'Inter', sans-serif;
    }

    /* Main container styling */
    .stApp {
        background-color: #f3f4f6; /* gray-100 */
    }

    /* Hide default streamlit elements */
    #MainMenu, footer, .stDeployButton, .stHeader {
        display: none;
    }
    
    /* Force remove top padding from Streamlit's main container */
    .block-container {
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Target the specific element that adds the top margin */
    div[data-testid="stVerticalBlock"] > [style*="gap: 1rem;"] {
        gap: 0 !important;
    }

    /* New App Header at the top of the page */
    .app-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        padding: 2rem;
        text-align: center;
        border-radius: 1rem 1rem 0 0; /* Rounded top corners only */
        margin-bottom: 0; /* REMOVED margin to connect to chat wrapper */
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .app-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .app-header p {
        font-size: 1rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }

    /* Chat container styling (no header inside) */
    .chat-wrapper {
        background: white;
        border-radius: 0 0 1rem 1rem; /* Rounded bottom corners only */
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        max-width: 800px;
        margin: 0 auto; /* REMOVED top margin */
        height: 70vh;
        display: flex;
        flex-direction: column;
    }

    .chat-history {
        flex-grow: 1;
        padding: 1.5rem;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .chat-message {
        display: flex;
        width: 100%;
    }

    .chat-bubble {
        max-width: 75%;
        padding: 0.75rem 1rem;
        border-radius: 1.25rem;
        word-wrap: break-word;
    }

    .user-message {
        justify-content: flex-end;
    }
    
    .user-bubble {
        background-color: #3b82f6; /* blue-500 */
        color: white;
        border-bottom-right-radius: 0.25rem;
    }

    .bot-message {
        justify-content: flex-start;
    }

    .bot-bubble {
        background-color: #e5e7eb; /* gray-200 */
        color: #1f2937; /* gray-800 */
        border-bottom-left-radius: 0.25rem;
    }
    
    /* Input area styling */
    .input-section {
        padding: 1rem 1.5rem;
        border-top: 1px solid #e5e7eb;
    }

    .stTextInput > div > div > input {
        border-radius: 9999px;
        border: 1px solid #d1d5db;
        padding: 0.75rem 1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
    }
    
    .stButton > button {
        border-radius: 9999px;
        border: none;
        background-color: #4f46e5;
        color: white;
        padding: 0.75rem 1.5rem;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #4338ca;
    }
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Initialize the chatbot with API key"""
    api_key = st.session_state.get('api_key', '') or os.getenv('OPENAI_API_KEY')
    if not api_key:
        return None
    try:
        return SalesPredictionChatbot(api_key)
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")
        return None

def main():
    """Main Streamlit application with custom UI"""

    # Sidebar for API key and settings
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        api_key = st.text_input(
            "OpenAI API Key", type="password", value=st.session_state.get('api_key', ''),
            help="Enter your OpenAI API key."
        )
        if api_key:
            st.session_state['api_key'] = api_key
        st.markdown("---")
        st.markdown("### 📖 Help")
        st.info("""
**I can help you with:**

🔮 **Sales Predictions:**
- 'Predict sales for item 3 on 2024-05-01'
- 'Sales for item 2 on 4-5-2024'



🏆 **Top Performers:**
- 'Most sold item in May 2024'

**Date formats:** YYYY-MM-DD, DD-MM-YYYY, 'whole May', etc.
        """)
        if st.button("🗑️ Clear Chat History"):
            st.session_state['messages'] = []
            st.rerun()

    # --- Main Page UI ---

    # Header at the top of the page
    st.markdown("""
        <div class="app-header">
            <h1>AI Sales Agent</h1>
            <p>Powered by RAG and OpenAI</p>
        </div>
    """, unsafe_allow_html=True)

    # Chat container below the header
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

    # Chat History Container
    with st.container():
        st.markdown('<div class="chat-history">', unsafe_allow_html=True)
        
        # Initialize chat history
        if 'messages' not in st.session_state:
            st.session_state['messages'] = [{"role": "bot", "content": "Hello! I'm your AI Sales Agent. I can help you with sales predictions, analyze historical data, and find top-performing items. What would you like to know?"}]

        # Display chat messages from history
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><div class="chat-bubble user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
            elif message["role"] == "bot":
                st.markdown(f'<div class="chat-message bot-message"><div class="chat-bubble bot-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # --- Input Section ---
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    chatbot = initialize_chatbot()
    if not chatbot:
        st.warning("Please enter your OpenAI API key in the sidebar to begin.")
    else:
        # Use st.chat_input for a cleaner chat interface
        if user_input := st.chat_input("Ask for sales predictions, analysis, or find top performers..."):
            # Add user message to session state
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get bot response
            with st.spinner("🤖 Thinking..."):
                try:
                    bot_response = chatbot.handle_query(user_input)
                    st.session_state.messages.append({"role": "bot", "content": bot_response})
                except Exception as e:
                    error_message = f"Sorry, an error occurred: {e}"
                    st.session_state.messages.append({"role": "bot", "content": error_message})
            
            # Rerun to update the chat display
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True) # Close input-section
    st.markdown('</div>', unsafe_allow_html=True) # Close chat-wrapper

if __name__ == "__main__":
    main()
