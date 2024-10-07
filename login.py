import random
import streamlit as st

# Function to generate and store CAPTCHA in session state
def generate_captcha():
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    captcha_solution = num1 + num2
    # Store the CAPTCHA solution in session state
    st.session_state.captcha_solution = captcha_solution
    return num1, num2

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.sidebar.success("You are logged in!")
    else:
        st.sidebar.error("You are not logged in")

    st.title("Hospital Login")

    # Dummy credentials
    username = "user"
    password = "pass123"

    if "captcha_solution" not in st.session_state:
        # Generate a CAPTCHA if not already done
        num1, num2 = generate_captcha()
    else:
        # Use the existing CAPTCHA from session state
        num1 = random.randint(1, 9)
        num2 = st.session_state.captcha_solution - num1

    with st.form(key="login_form"):
        st.write("Please log in:")
        user_input = st.text_input("Username")
        pass_input = st.text_input("Password", type="password")

        # Display CAPTCHA
        st.write(f"Solve the CAPTCHA: What is {num1} + {num2}?")
        captcha_input = st.text_input("Your answer to the CAPTCHA")

        submit_button = st.form_submit_button(label="Login")

        # Check credentials and CAPTCHA
        if submit_button:
            if user_input == username and pass_input == password:
                try:
                    # Check if the CAPTCHA input is correct
                    if captcha_input and int(captcha_input) == st.session_state.captcha_solution:
                        st.session_state.logged_in = True
                        st.success("Logged in successfully!")
                        st.session_state.login_attempts = 0  # Reset any previous state
                        # Trigger a rerun by modifying session state
                        st.session_state.page_reloaded = True
                    else:
                        st.error("CAPTCHA is incorrect. Please try again.")
                        # Regenerate CAPTCHA on incorrect answer
                        num1, num2 = generate_captcha()
                except ValueError:
                    st.error("Please enter a valid number for the CAPTCHA.")
            else:
                st.error("Username or password is incorrect.")
