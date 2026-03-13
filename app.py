# import streamlit as st
# import os
# import sys
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# from models.llm import get_chatgroq_model


# def get_chat_response(chat_model, messages, system_prompt):
#     """Get response from the chat model"""
#     try:
#         # Prepare messages for the model
#         formatted_messages = [SystemMessage(content=system_prompt)]
        
#         # Add conversation history
#         for msg in messages:
#             if msg["role"] == "user":
#                 formatted_messages.append(HumanMessage(content=msg["content"]))
#             else:
#                 formatted_messages.append(AIMessage(content=msg["content"]))
        
#         # Get response from model
#         response = chat_model.invoke(formatted_messages)
#         return response.content
    
#     except Exception as e:
#         return f"Error getting response: {str(e)}"

# def instructions_page():
#     """Instructions and setup page"""
#     st.title("The Chatbot Blueprint")
#     st.markdown("Welcome! Follow these instructions to set up and use the chatbot.")
    
#     st.markdown("""
#     ## 🔧 Installation
                
    
#     First, install the required dependencies: (Add Additional Libraries base don your needs)
    
#     ```bash
#     pip install -r requirements.txt
#     ```
    
#     ## API Key Setup
    
#     You'll need API keys from your chosen provider. Get them from:
    
#     ### OpenAI
#     - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
#     - Create a new API key
#     - Set the variables in config
    
#     ### Groq
#     - Visit [Groq Console](https://console.groq.com/keys)
#     - Create a new API key
#     - Set the variables in config
    
#     ### Google Gemini
#     - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
#     - Create a new API key
#     - Set the variables in config
    
#     ## 📝 Available Models
    
#     ### OpenAI Models
#     Check [OpenAI Models Documentation](https://platform.openai.com/docs/models) for the latest available models.
#     Popular models include:
#     - `gpt-4o` - Latest GPT-4 Omni model
#     - `gpt-4o-mini` - Faster, cost-effective version
#     - `gpt-3.5-turbo` - Fast and affordable
    
#     ### Groq Models
#     Check [Groq Models Documentation](https://console.groq.com/docs/models) for available models.
#     Popular models include:
#     - `llama-3.1-70b-versatile` - Large, powerful model
#     - `llama-3.1-8b-instant` - Fast, smaller model
#     - `mixtral-8x7b-32768` - Good balance of speed and capability
    
#     ### Google Gemini Models
#     Check [Gemini Models Documentation](https://ai.google.dev/gemini-api/docs/models/gemini) for available models.
#     Popular models include:
#     - `gemini-1.5-pro` - Most capable model
#     - `gemini-1.5-flash` - Fast and efficient
#     - `gemini-pro` - Standard model
    
#     ## How to Use
    
#     1. **Go to the Chat page** (use the navigation in the sidebar)
#     2. **Start chatting** once everything is configured!
    
#     ## Tips
    
#     - **System Prompts**: Customize the AI's personality and behavior
#     - **Model Selection**: Different models have different capabilities and costs
#     - **API Keys**: Can be entered in the app or set as environment variables
#     - **Chat History**: Persists during your session but resets when you refresh
    
#     ## Troubleshooting
    
#     - **API Key Issues**: Make sure your API key is valid and has sufficient credits
#     - **Model Not Found**: Check the provider's documentation for correct model names
#     - **Connection Errors**: Verify your internet connection and API service status
    
#     ---
    
#     Ready to start chatting? Navigate to the **Chat** page using the sidebar! 
#     """)

# def chat_page():
#     """Main chat interface page"""
#     st.title("🤖 AI ChatBot")
    
#     # Get configuration from environment variables or session state
#     # Default system prompt
#     system_prompt = ""
    
    
#     # Determine which provider to use based on available API keys
#     chat_model = get_chatgroq_model()
    
#     # Initialize chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
    
#     # Display chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
    
#     # Chat input
#     # if chat_model:
#     if prompt := st.chat_input("Type your message here..."):
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})
        
#         # Display user message
#         with st.chat_message("user"):
#             st.markdown(prompt)
        
#         # Generate and display bot response
#         with st.chat_message("assistant"):
#             with st.spinner("Getting response..."):
#                 response = get_chat_response(chat_model, st.session_state.messages, system_prompt)
#                 st.markdown(response)
        
#         # Add bot response to chat history
#         st.session_state.messages.append({"role": "assistant", "content": response})
#     else:
#         st.info("🔧 No API keys found in environment variables. Please check the Instructions page to set up your API keys.")

# def main():
#     st.set_page_config(
#         page_title="LangChain Multi-Provider ChatBot",
#         page_icon="🤖",
#         layout="wide",
#         initial_sidebar_state="expanded"
#     )
    
#     # Navigation
#     with st.sidebar:
#         st.title("Navigation")
#         page = st.radio(
#             "Go to:",
#             ["Chat", "Instructions"],
#             index=0
#         )
        
#         # Add clear chat button in sidebar for chat page
#         if page == "Chat":
#             st.divider()
#             if st.button("🗑️ Clear Chat History", use_container_width=True):
#                 st.session_state.messages = []
#                 st.rerun()
    
#     # Route to appropriate page
#     if page == "Instructions":
#         instructions_page()
#     if page == "Chat":
#         chat_page()

# if __name__ == "__main__":
#     main()  












import streamlit as st
import os
import sys
import tempfile
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from models.llm import get_chatgroq_model
from utils.rag import load_and_split_document, create_vectorstore, retrieve_relevant_chunks
from utils.web_search import get_web_search_results

# Load environment variables from .env file
load_dotenv()

# ── Response Mode Prompts ─────────────────────────────
CONCISE_PROMPT = """You are InsightBot, a helpful research assistant. 
Give short, clear, and summarized answers in 2-3 sentences maximum.
If context is provided, use it to answer. Be direct and to the point."""

DETAILED_PROMPT = """You are InsightBot, a helpful research assistant.
Give comprehensive, well-structured, and in-depth answers.
If context is provided, use it to answer thoroughly.
Explain concepts clearly with examples where needed."""

def get_chat_response(chat_model, messages, system_prompt, context=""):
    """Get response from the chat model"""
    try:
        full_prompt = system_prompt
        if context:
            full_prompt += f"\n\nRelevant Context:\n{context}"

        # Prepare messages for the model
        formatted_messages = [SystemMessage(content=full_prompt)]
        
        # Add conversation history
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))
        
        # Get response from model
        response = chat_model.invoke(formatted_messages)
        return response.content
    
    except Exception as e:
        return f"Error getting response: {str(e)}"

def instructions_page():
    """Instructions and setup page"""
    st.title("📘 InsightBot — Research Assistant")
    st.markdown("Welcome! InsightBot helps you research smarter using RAG and live web search.")
    
    st.markdown("""
    ## 🔧 Installation
    
    First, install the required dependencies:
```bash
    pip install -r requirements.txt
```
    
    ## 🔑 API Key Setup
    
    You'll need API keys from your chosen provider. Get them from:
    
    ### Groq
    - Visit [Groq Console](https://console.groq.com/keys)
    - Create a new API key
    - Set the variables in config/config.py
    
    ### Google Gemini
    - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
    - Create a new API key
    - Set the variables in config/config.py

    ### Tavily
    - Visit [Tavily](https://app.tavily.com)
    - Create a new API key
    - Set the variables in config/config.py
    
    ## 📝 Available Models
    
    ### Groq Models
    - `llama-3.1-70b-versatile` - Large, powerful model
    - `llama-3.1-8b-instant` - Fast, smaller model
    - `mixtral-8x7b-32768` - Good balance of speed and capability
    
    ## 🚀 Features
    - 📄 **RAG**: Upload a PDF and ask questions from it
    - 🌐 **Web Search**: Get live results when docs are not enough
    - ⚡ **Response Modes**: Switch between Concise and Detailed answers

    ## How to Use
    
    1. **Go to the Chat page** using the sidebar navigation
    2. **Upload a PDF** document (optional)
    3. **Toggle Web Search** if you need live information
    4. **Choose Response Mode** — Concise or Detailed
    5. **Start chatting!**
    
    ## Tips
    
    - **Concise Mode**: Best for quick answers and summaries
    - **Detailed Mode**: Best for in-depth explanations
    - **RAG**: Upload any PDF to chat with its contents
    - **Web Search**: Enable for real-time information
    - **Chat History**: Persists during your session but resets when you refresh
    
    ## Troubleshooting
    
    - **API Key Issues**: Make sure your API key is valid and has sufficient credits
    - **Model Not Found**: Check the provider's documentation for correct model names
    - **Connection Errors**: Verify your internet connection and API service status
    
    ---
    
    Ready to start chatting? Navigate to the **Chat** page using the sidebar! 
    """)

def chat_page():
    """Main chat interface page"""
    st.title("🤖 InsightBot")
    st.caption("Your AI-powered Research Assistant")

    # ── Sidebar Controls ──────────────────────────────
    with st.sidebar:
        st.subheader("⚙️ Settings")

        # Response Mode Toggle
        response_mode = st.radio(
            "Response Mode:",
            ["Concise", "Detailed"],
            index=0
        )

        st.divider()

        # Web Search Toggle
        use_web_search = st.toggle("🌐 Enable Web Search", value=False)

        st.divider()

        # PDF Upload
        st.subheader("📄 Upload Document")
        uploaded_file = st.file_uploader(
            "Upload a PDF",
            type=["pdf"],
            help="Upload a PDF to chat with its contents"
        )

        if uploaded_file:
            if "vectorstore" not in st.session_state or st.session_state.get("uploaded_filename") != uploaded_file.name:
                with st.spinner("Processing document..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_file.write(uploaded_file.read())
                            tmp_path = tmp_file.name

                        chunks = load_and_split_document(tmp_path)
                        st.session_state.vectorstore = create_vectorstore(chunks)
                        st.session_state.uploaded_filename = uploaded_file.name
                        os.unlink(tmp_path)
                        st.success(f"✅ {uploaded_file.name} processed!")
                    except Exception as e:
                        st.error(f"Error processing document: {str(e)}")
        else:
            if "vectorstore" in st.session_state:
                del st.session_state.vectorstore
            if "uploaded_filename" in st.session_state:
                del st.session_state.uploaded_filename

        st.divider()

        # Clear Chat
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # ── Chat Interface ────────────────────────────────
    system_prompt = CONCISE_PROMPT if response_mode == "Concise" else DETAILED_PROMPT

    chat_model = get_chatgroq_model()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                context = ""

                # RAG retrieval
                if "vectorstore" in st.session_state:
                    try:
                        rag_context = retrieve_relevant_chunks(
                            st.session_state.vectorstore, prompt
                        )
                        context += f"📄 From Document:\n{rag_context}\n\n"
                    except Exception as e:
                        st.warning(f"RAG error: {str(e)}")

                # Web search
                if use_web_search:
                    try:
                        web_context = get_web_search_results(prompt)
                        context += f"🌐 From Web:\n{web_context}\n\n"
                    except Exception as e:
                        st.warning(f"Web search error: {str(e)}")

                response = get_chat_response(
                    chat_model,
                    st.session_state.messages,
                    system_prompt,
                    context
                )
                st.markdown(response)

        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    st.set_page_config(
        page_title="InsightBot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Navigation
    with st.sidebar:
        st.title("🔍 InsightBot")
        st.divider()
        page = st.radio(
            "Navigation",
            ["Chat", "Instructions"],
            index=0
        )
        st.divider()
    
    # Route to appropriate page
    if page == "Instructions":
        instructions_page()
    if page == "Chat":
        chat_page()

if __name__ == "__main__":
    main()