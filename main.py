import streamlit as st
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import pysqlite3
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    temperature=0.7, 
    model_name="groq/llama-3.1-70b-versatile", 
    api_key=GROQ_API_KEY,
    provider="Meta"
)

def create_agent(role, goal, backstory):
    return Agent(
        llm=llm,
        role=role,
        goal=goal,
        backstory=backstory,
        allow_delegation=False,
        verbose=True,
    )

# Refined prompts to ensure responses are tailored strictly to the user's query
support_agent = create_agent(
    role="Mental Health Support Agent",
    goal=(
        "Provide a response tailored to the user's concern: {input}. "
        "Offer advice, coping mechanisms, and tips directly related to the specific concern mentioned by the user, without assuming additional context. "
        "For example, if the user mentions depression, provide advice on managing depression such as seeking support, self-care techniques, or grounding exercises. "
        "Be empathetic, practical, and provide suggestions that are appropriate for the specific issue raised in the user's query."
    ),
    backstory=(
        "You are a mental health support agent trained to offer advice based on the specific context provided by the user. "
        "Your goal is to address the user's concern directly, providing relevant strategies and tips that align with the specific issue mentioned (e.g., depression, anxiety, stress). "
        "Avoid assuming context unless explicitly stated, and ensure your response is practical and supportive."
    ),
)

def create_task(description, expected_output, agent):
    return Task(description=description, expected_output=expected_output, agent=agent)

# Updated task description to focus on the user's specific concern
support_task = create_task(
    description=(
        "Engage with the user based on their specific concern: {input}. "
        "Acknowledge the specific issue they mention and provide tailored advice, strategies, and coping mechanisms related to it. "
        "Offer practical steps such as self-care techniques, reaching out to a support network, or exploring relaxation exercises, depending on the user's stated concern."
    ),
    expected_output=(
        "A response that directly addresses the user's concern, provides targeted advice, and suggests coping strategies relevant to the specific context provided by the user."
    ),
    agent=support_agent,
)

crew = Crew(agents=[support_agent], tasks=[support_task], verbose=True)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# To track the current ongoing chat session
if 'current_chat' not in st.session_state:
    st.session_state['current_chat'] = []

def main():
    st.title("AI-Powered Mental Health Support Chatbot")

    # Sidebar to display chat history and additional buttons
    st.sidebar.title("Chat History")
    if st.sidebar.button("Start New Chat"):
        # Clear the current chat if the user wants to start a new one
        st.session_state['current_chat'] = []

    if st.sidebar.button("Save Chat History"):
        # Save the current chat history to the session's overall chat history
        if st.session_state['current_chat']:
            st.session_state['chat_history'].append(list(st.session_state['current_chat']))  # Save a copy of the current chat
            st.sidebar.success("Chat history saved successfully!")

    # Display saved chat histories and add a selectbox for choosing a specific chat
    chat_options = [f"Chat History {i+1}" for i in range(len(st.session_state['chat_history']))]
    selected_chat = st.sidebar.selectbox("Select a chat to delete:", chat_options if chat_options else ["No saved chats"])

    if st.sidebar.button("Delete Selected Chat"):
        # Delete the selected chat history
        if chat_options:
            selected_index = chat_options.index(selected_chat)
            st.session_state['chat_history'].pop(selected_index)
            st.sidebar.success(f"{selected_chat} deleted successfully!")

    if st.sidebar.button("Delete Entire Chat History"):
        # Clear all saved chat histories
        st.session_state['chat_history'] = []
        st.sidebar.success("All chat histories have been deleted!")

    # Display saved chat histories
    for i, chat_session in enumerate(st.session_state['chat_history']):
        with st.sidebar.expander(f"Chat History {i+1}"):
            for entry in chat_session:
                st.write(f"**You:** {entry['topic']}")
                st.write(f"**Bot:** {entry['response']}")

    # Display current chat in the main interface
    for entry in st.session_state['current_chat']:
        st.write(f"**You:** {entry['topic']}")
        st.write(f"**Bot:** {entry['response']}")

    topic = st.text_input("Enter your concern or topic for support")

    if st.button("Submit Query"):
        if topic:
            with st.spinner("Connecting to support agent..."):
                # Incorporate the user's input into the task description and agent's goal for dynamic responses
                result = crew.kickoff(inputs={"input": topic})
            
            # Extract the necessary outputs and format them
            try:
                support_output = result.tasks_output[0].raw

                # Display the outputs in a readable format
                st.subheader("Support Response")
                st.markdown(support_output)

                # Store the query and response in the current chat session
                chat_summary = {
                    "topic": topic,
                    "response": support_output,
                }
                st.session_state['current_chat'].append(chat_summary)

            except Exception as e:
                st.error(f"An error occurred while extracting the output: {e}")

if __name__ == "__main__":
    main()
