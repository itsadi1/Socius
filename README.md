# Socius: Multi LLM Web Interface
A sleek and intuitive Streamlit-based web application for managing and interacting with Ollama's language models. This application allows users to start/stop the Ollama server, select different models, and engage in conversations with a clean, user-friendly interface, enhanced by ngrok for public access.
Features

Server Management: Start and stop the Ollama server with a single click.
Model Selection: Seamlessly switch between supported models (Yi, Mistral, Llama3.2, Tinyllama).
Chat Interface: Engage in conversations with the selected model, with a persistent conversation history.
Public Access: Expose the application to the internet using ngrok for easy sharing.
Real-Time Status: Monitor the server's status with a color-coded indicator (green for running, red for stopped).
Responsive Design: Centered layout with a clean, modern look, optimized for ease of use.

Prerequisites
To run this application, ensure you have the following installed:

Python 3.8+
Ollama: Install Ollama to manage language models locally. Ollama Installation Guide
ngrok: Required for creating a public URL. Sign up for an account and obtain an auth token at ngrok.
Required Python packages:pip install streamlit langchain-ollama requests pyngrok



## Installation

Clone the Repository:
```
git clone https://github.com/itsadi1/socius.git
cd socius
```

### Install Dependencies:
  > For Linux: `bash requirements.bash`
Installs Ollama along with all libraries <br>


For Others: Follow the guide 👇<br>
`pip install -r requirements.txt`


### Install Ollama:

Follow the instructions on the Ollama website to install and set up Ollama on your system.
If you are on Linux, installation package is already installed with requirements.bash 


### Set Up ngrok:

Obtain your ngrok auth token from the ngrok dashboard.
Set the token as an environment variable: <br>
`export ngrok_auth_key="your-ngrok-auth-token"`


## Usage

> **Note: You may first need to install all models manually before running the script.**


```bash
  ollama serve
  ollama pull yi:latest
  ollama pull mistral:latest
  ollama pull llama3.2
  ollama pull tinyllama
```

### Run the Application:
```streamlit run app.py```


Access the Interface:

The application will open in your default browser at http://localhost:8501.
A public URL will be generated via ngrok and displayed in the interface for external access.

On Linux the public url can also be accessed by: `bash url.bash`


### Interact with the App:

Start/Stop Server: Use the "Start" and "Stop" buttons to control the Ollama server.
Select Model: Choose a model from the dropdown menu to switch between available language models.
Chat: Type your message in the input field, click "Send," and view the conversation history in the text area.



### Code Structure

app.py: The main application script containing the Streamlit interface and logic for server management and model interaction.
Key Functions:
run_ollama_serve(): Starts the Ollama server.
stop_ollama_serve(): Stops the Ollama server.
check_ollama_status(): Checks if the Ollama server is running.
init_llm_model(): Initializes or switches the language model.
main(): Orchestrates the Streamlit interface and application logic.



### Notes

Environment Variables: Ensure the ngrok_auth_key environment variable is set before running the app to enable public access.
Model Availability: The application assumes the selected models (Yi, Mistral, Llama3.2, Tinyllama) are available in your Ollama installation. Install them using ollama pull <model_name> if needed.
Session State: The application uses Streamlit's session state to maintain the server process, model selection, and conversation history.
Error Handling: The app includes basic error handling for server and model operations, displaying errors in the UI.

## Troubleshooting

Ollama Command Not Found: Ensure Ollama is installed and accessible in your system's PATH.
ngrok Errors: Verify your auth token and internet connection. Check ngrok's documentation for additional help.
Model Switching Issues: If a model fails to load, ensure it is installed via ollama pull <model_name> and the server is running.

Contributing
Contributions are welcome! Please open an issue or submit a pull request on the GitHub repository with your improvements or bug fixes.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Built with Streamlit for the web interface.
Powered by Ollama for local language model management.
Enabled for public access with ngrok.


Happy chatting with your local AI models! 🚀
