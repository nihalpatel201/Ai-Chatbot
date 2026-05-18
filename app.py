import streamlit as st
from google import genai

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 My First AI Chatbot")
st.write("Type a message below to generate responses dynamically via an API.")

# 1. API Authentication Setup
# For security, you would normally hide this, but we'll paste it directly for learning.
API_KEY = "AIzaSyC7xOric6UAdvMNYCxUSW-p7HGIvrFbmWg" 

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("Failed to initialize API client. Check your API key.")

# 2. Managing Chat History using Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handling User Input & Making the API Call
if user_prompt := st.chat_input("Ask me anything..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Call the API dynamically
    try:
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=user_prompt,
            )
            
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"API Error: {e}")
