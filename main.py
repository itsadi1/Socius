import subprocess
import streamlit as st
from langchain_ollama import OllamaLLM
import requests
from pyngrok import ngrok, conf

# Global variable for ngrok tunnel
public_url = None

# Run Ollama server
def run_ollama_serve():
    try:
        process = subprocess.Popen(["ollama", "serve"])
        return process
    except FileNotFoundError:
        st.error("`ollama` command not found")
    except Exception as e:
        st.error(f"Start failed: {e}")
    return None

# Stop Ollama server
def stop_ollama_serve():
    process = st.session_state.get("ollama_process")
    if process:
        try:
            process.terminate()
            process.wait()
            st.session_state.ollama_process = None
        except Exception as e:
            st.error(f"Stop failed: {e}")

# Check server status
def check_ollama_status():
    try:
        response = requests.get("http://localhost:11434")
        return response.status_code == 200
    except requests.ConnectionError:
        return False

# Initialize LLM model
def stop_ollama_model(model_name):
    try:
        # Run the stop command for the specified model
        subprocess.run(["ollama", "stop", model_name], check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to stop model {model_name}: {e}")
    except Exception as e:
        st.error(f"Error stopping model {model_name}: {e}")

def init_llm_model(selected_model):
    if st.session_state.get("llm_model_name") != selected_model:
        # Stop the currently running model (if any)
        if "llm_model_name" in st.session_state:
            stop_ollama_model(st.session_state.llm_model_name)
        # Switch to the new model
        st.session_state.llm_model_name = selected_model
        st.session_state.llm = OllamaLLM(model=selected_model, temperature=0.1, verbose=True)

def main():
    global public_url
    
    st.set_page_config(page_title="Ollama Control", layout="centered", page_icon="🧠")
    
    # Initialize ngrok tunnel only once
    if 'ngrok_initialized' not in st.session_state:
        # Set ngrok auth token for public access
        conf.get_default().auth_token = os.environ.get('ngrok_auth_key')
        public_url = ngrok.connect(8501, "http").public_url
        st.session_state.ngrok_initialized = True
        st.session_state.public_url = public_url
    
    # Initialize session state
    if "ollama_process" not in st.session_state:
        st.session_state.ollama_process = None
    if "llm_model_name" not in st.session_state:
        st.session_state.llm_model_name = "yi"
    if "llm" not in st.session_state:
        st.session_state.llm = OllamaLLM(model="yi")
    if "history" not in st.session_state:
        st.session_state.history = ""
    if "user1" not in st.session_state:
        st.session_state.user1 = ""
    if "need_clear" not in st.session_state:
        st.session_state.need_clear = False

    # Clear input if needed (must be before widget instantiation)
    if st.session_state.need_clear:
        st.session_state.user1 = ""
        st.session_state.need_clear = False
        st.rerun()

    # Header with status indicator
    is_running = check_ollama_status()
    status_text = "Running" if is_running else "Stopped"
    status_color = "green" if is_running else "red"

    # Render status in header using markdown with color
    st.markdown(f"### Server Status: <span style='color:{status_color}'>{status_text}</span>", unsafe_allow_html=True)
    
    # Show public URL if available
    if 'public_url' in st.session_state:
        st.markdown(f"**Public URL:** `{st.session_state.public_url}`")

    # Server controls and model selection
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        if st.button("▶️ Start", use_container_width=True):
            if st.session_state.ollama_process is None:
                process = run_ollama_serve()
                if process:
                    st.session_state.ollama_process = process
    with col2:
        if st.button("⏹️ Stop", use_container_width=True):
            stop_ollama_serve()
    with col3:
        selected_model = st.selectbox("Model", ["Yi", "Mistral","Llama3.2","Tinyllama"], label_visibility="collapsed")
        init_llm_model(selected_model.lower())

    # Conversation history as text area
    st.text_area(
        "History",
        value=st.session_state.history,
        height=350,
        label_visibility="collapsed",
        key="history_area"
    )
    # Query input and send button
    with st.form("chat_form"):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "Your message",
                key="user1",
                label_visibility="collapsed",
                placeholder="Type your message..."
            )
        with col2:
            submitted = st.form_submit_button("Send", use_container_width=True)
        
        if submitted and user_input:
            try:
                # Get response from LLM
                response = st.session_state.llm(f"Answer concisely: {user_input}")
                
                # Update history
                st.session_state.history = f"AI: {response}\nYou: {user_input}\n\n" + st.session_state.history
                
                # Set flag to clear input on next run
                st.session_state.need_clear = True
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
