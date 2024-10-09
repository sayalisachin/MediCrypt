# Import necessary libraries
import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3

# Initialize OpenAI API key directly in the script
openai.api_key = "your-openai-api-key"  # Replace with your OpenAI API key

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

# Function to query OpenAI API using ChatCompletion
def ask_openai(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use the GPT-4 model if available
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": question},
            ],
            temperature=0.7,
            max_tokens=150,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Function to recognize speech input
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("Listening... Please speak into the microphone.")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand the audio.")
        return None
    except sr.RequestError:
        st.error("Could not request results; check your network connection.")
        return None

# Function for text-to-speech (TTS)
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Streamlit UI setup
st.title("Voice-Enabled Medical Chatbot")
st.write("Ask any medical-related questions using your voice or by typing, and the chatbot will provide answers.")

# Use a session state to store the user input
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Voice or text input selection
input_method = st.radio("Choose input method:", ("Type your question", "Use voice input"))

# Capture user input
if input_method == "Type your question":
    user_input = st.text_input("Enter your medical question:")
    if st.button("Ask with text"):
        st.session_state["user_input"] = user_input
elif input_method == "Use voice input":
    if st.button("Click to Speak"):
        voice_input = recognize_speech()
        if voice_input:
            st.session_state["user_input"] = voice_input

# Only proceed if user input is available
if st.session_state["user_input"]:
    with st.spinner("Generating response..."):
        answer = ask_openai(st.session_state["user_input"])
        st.write(f"**Chatbot:** {answer}")
        speak_text(answer)  # Use TTS to speak the response
    # Clear the input after the response is generated
    st.session_state["user_input"] = ""

# Display some example questions
st.subheader("Example Questions")
st.write("""
- What are the symptoms of COVID-19?
- How does hypertension affect the body?
- What is the treatment for diabetes?
- What are the side effects of ibuprofen?
""")
