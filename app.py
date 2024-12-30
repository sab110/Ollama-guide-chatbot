import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Set up OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key is missing. Please set it in the .env file.")
else:

    client = OpenAI(api_key=api_key)

# Function to reset the chat
def reset_chat():
    st.session_state.messages = []

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# List of valid models with descriptions
models_info = {
    "codellama": "A model optimized for code generation and understanding.",
    "gemma": "A general-purpose language model for various NLP tasks.",
    "llava": "A vision-language model capable of image and text processing.",
    "llama2": "An advanced conversational AI model.",
    "qwen": "A multilingual model with extensive language support.",
    "bakllava": "A multimodal model for image reasoning.",
    "wizardcoder": "A model designed for code generation and debugging."
}

# Function to generate response using OpenAI's GPT-4
def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "I'm sorry, I couldn't process your request at the moment. Please try again."

# Streamlit app layout
st.title("Ollama Installation Assistant")
st.subheader("Your guide to installing Ollama and exploring models")

# Sidebar for model selection
st.sidebar.header("Available Models")
selected_model = st.sidebar.selectbox("Select a model to learn more", [""] + list(models_info.keys()))
if selected_model:
    st.sidebar.write(f"**{selected_model.capitalize()}**: {models_info[selected_model]}")

st.sidebar.info(
    """
    - [Ollama Setup](https://ollama.com/download)
    - [Ollama GitHub](https://github.com/ollama/ollama)
    - [Ollama Models](https://ollama.com/library)
    """
)

# Reset button
if st.button("Reset Chat"):
    reset_chat()
    st.experimental_rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if user_input := st.chat_input("How can I assist you today?"):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare prompt for the model
    prompt = st.session_state.messages.copy()
    prompt.insert(0, {"role": "system", "content": (
        "You are an AI assistant specializing in guiding users through the installation of Ollama on various operating systems. "
        "Provide clear, step-by-step instructions tailored to the user's platform and the specific model they are interested in. "
        "Ensure your instructions are concise, actionable, and easy to follow. "
        "Here are useful resources: [Ollama Setup](https://ollama.com/download), "
        "[GitHub](https://github.com/ollama/ollama), [Models Page](https://ollama.com/library)."
    )})

    # Generate and display assistant's response
    assistant_response = generate_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
