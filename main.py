import subprocess
import streamlit as st
from langchain_ollama import OllamaLLM
import requests
from pyngrok import ngrok, conf

public_url = None

def start():
    try:
        process = subprocess.Popen(["ollama", "serve"])
        return process
    except FileNotFoundError:
        st.error("`ollama` command not found")
    except Exception as e:
        st.error(f"Start failed: {e}")
    return None

def terminate():
    process = st.session_state.get("ollama_process")
    if process:
        try:
            process.terminate()
            process.wait()
            st.session_state.ollama_process = None
        except Exception as e:
            st.error(f"Stop failed: {e}")

def status():
    try:
        response = requests.get("http://localhost:11434")
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def stop(model_name):
    try:
        # Run the stop command for the specified model
        subprocess.run(["ollama", "stop", model_name], check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to stop model {model_name}: {e}")
    except Exception as e:
        st.error(f"Error stopping model {model_name}: {e}")

def init_model(selected_model):
    if st.session_state.get("llm_model_name") != selected_model:
        if "llm_model_name" in st.session_state:
            stop(st.session_state.llm_model_name)
        st.session_state.llm_model_name = selected_model
        st.session_state.llm = OllamaLLM(model=selected_model, temperature=0.1, verbose=True)

def main():
    global public_url
    
    st.set_page_config(page_title="Ollama Control", layout="centered", page_icon="🧠")
    
    if 'ngrok_initialized' not in st.session_state:
        conf.get_default().auth_token = os.environ.get('ngrok_auth_key')
        public_url = ngrok.connect(8501, "http").public_url
        st.session_state.ngrok_initialized = True
        st.session_state.public_url = public_url
    
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

    if st.session_state.need_clear:
        st.session_state.user1 = ""
        st.session_state.need_clear = False
        st.rerun()

    is_running = status()
    status_text = "Running" if is_running else "Stopped"
    status_color = "green" if is_running else "red"

    st.markdown(f"### Server Status: <span style='color:{status_color}'>{status_text}</span>", unsafe_allow_html=True)
    
    if 'public_url' in st.session_state:
        st.markdown(f"**Public URL:** `{st.session_state.public_url}`")

    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        if st.button("▶️ Start", use_container_width=True):
            if st.session_state.ollama_process is None:
                process = start()
                if process:
                    st.session_state.ollama_process = process
    with col2:
        if st.button("⏹️ Stop", use_container_width=True):
            terminate()
    with col3:
        selected_model = st.selectbox("Model", ["Yi", "Mistral","Llama3.2","Tinyllama"], label_visibility="collapsed")
        init_model(selected_model.lower())

    st.text_area(
        "History",
        value=st.session_state.history,
        height=350,
        label_visibility="collapsed",
        key="history_area"
    )
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
                response = st.session_state.llm(f"Answer concisely: {user_input}")                
                st.session_state.history = f"AI: {response}\nYou: {user_input}\n\n" + st.session_state.history
                st.session_state.need_clear = True
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
