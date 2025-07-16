import streamlit as st
import re
from datetime import datetime

class InputProcessor:
    def __init__(self, rules):
        self.rules = rules["rules"]
        self.default_response = rules["default_response"]

    def clean_input(self, user_input):
        return user_input.lower().strip()

    def match_pattern(self, user_input):
        cleaned_input = self.clean_input(user_input)
        for rule in self.rules:
            pattern = rule["pattern"]
            response = rule["response"]
            if re.search(pattern, cleaned_input, re.IGNORECASE):
                if "time" in pattern:
                    current_time = datetime.now().strftime("%I:%M %p")
                    response = response.format(time=current_time)
                return response, "bye" in pattern or "quit" in pattern or "exit" in pattern
        return self.default_response, False


class Chatbot:
    def __init__(self, rules):
        self.processor = InputProcessor(rules)
        self.history = []

    def respond(self, user_input):
        response, should_exit = self.processor.match_pattern(user_input)
        self.history.append((user_input, response))
        return response, should_exit

    def save_history(self, file_path):
        with open(file_path, "a") as f:
            for user_input, bot_response in self.history:
                f.write(f"User: {user_input}\nBot: {bot_response}\n---\n")


def main():
    
    if "chatbot" not in st.session_state:
        rules = {
            "rules": [
                {"pattern": "hello|hi|hey", "response": "Hello! How can I assist you today?"},
                {"pattern": "how are you|you doing", "response": "I'm doing great, thanks for asking! How about you?"},
                {"pattern": "name|who are you", "response": "I'm Grok, a simple chatbot created to help you with basic queries!"},
                {"pattern": "time|what time is it", "response": "The current time is {time}."},
                {"pattern": "weather|how's the weather", "response": "I don't have real-time weather data, but it’s probably sunny somewhere! What's the weather like where you are?"},
                {"pattern": "bye|goodbye|quit|exit", "response": "Goodbye! Thanks for chatting with me!"}
            ],
            "default_response": "Sorry, I didn't understand that. Can you try something else?"
        }
        st.session_state.chatbot = Chatbot(rules)
    if "history" not in st.session_state:
        st.session_state.history = []

    
    st.title("Simple Rule-Based Chatbot")
    st.write("Type your message below and press Enter to chat with me! Type 'quit' to save the conversation.")


    st.subheader("Chat History")
    for user_input, bot_response in st.session_state.history:
        st.write(f"**You**: {user_input}")
        st.write(f"**Bot**: {bot_response}")

    
    user_input = st.text_input("Your message:", key="chat_input")
    if user_input:
        response, should_exit = st.session_state.chatbot.respond(user_input)
        st.session_state.history.append((user_input, response))
        st.write(f"**You**: {user_input}")
        st.write(f"**Bot**: {response}")
        if should_exit:
            st.session_state.chatbot.save_history("history.txt")
            st.write("Conversation saved to 'history.txt'. Refresh the page to start a new session.")
            st.stop()

if __name__ == "__main__":
    main()
