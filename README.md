# AI-Powered Mental Health Support Chatbot

## Overview
The AI-Powered Mental Health Support Chatbot is an intelligent virtual assistant designed to provide empathetic support and practical advice for mental health-related concerns. The chatbot engages with users based on their specific queries, offering tailored responses, coping mechanisms, and relevant strategies. This project leverages natural language processing (NLP) to interact with users and provide responses that are contextually appropriate, helping users manage their mental health more effectively.

## Features
- **Personalized Support:** The chatbot provides responses tailored to the specific concern mentioned by the user, avoiding generic advice.
- **Interactive Chat History:** Users can view, save, and manage chat histories, making it easy to refer back to previous conversations.
- **Clear Interface:** The application is built using Streamlit, providing a simple and interactive web interface for user interaction.
- **Audio Input (Upcoming):** An extension of this project includes audio input using speech-to-text functionality for a more interactive experience.

## Tech Stack
### 1. **Python:** 
   - The core programming language used for implementing the chatbot logic, handling user inputs, and integrating with other libraries.

### 2. **Streamlit:** 
   - A powerful and easy-to-use framework for creating interactive web applications in Python. Streamlit is used for building the user interface of the chatbot, allowing users to enter text inputs, view chat history, and interact with the chatbot seamlessly.
   - It provides components such as `st.text_input`, `st.button`, and `st.sidebar` to facilitate user interaction with the chatbot.

### 3. **LangChain Groq API:**
   - This project uses the `ChatGroq` model from the `langchain_groq` library to handle natural language processing tasks. The `ChatGroq` model is an advanced language model that generates contextual responses based on user input.
   - This is integrated using the API key provided via environment variables for secure access.

### 4. **CrewAI:**
   - `crewai` is utilized to create and manage different agents within the chatbot application. The `Agent` and `Task` classes help define the chatbot's goals and interaction logic, ensuring responses are appropriate for mental health support.
   - The `Crew` class orchestrates the interactions between different tasks and agents to produce the final output.

### 5. **dotenv:**
   - The `dotenv` package is used to load environment variables, including sensitive information like the API key for the Groq model (`GROQ_API_KEY`). This keeps the application secure by avoiding hardcoding sensitive information in the codebase.

## Getting Started
### Prerequisites
- Python 3.8 or above
- Required Python libraries (can be installed using `requirements.txt`):
  - `streamlit`
  - `crewai`
  - `langchain_groq`
  - `python-dotenv`

### Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/mental-health-chatbot.git
   cd mental-health-chatbot

2. Create an .env file to input your Groq Api Key

#Contributions
Hi i welcome anyone to contribute to this project.If you have innovative ideas or new features to add you can raise an issue.
