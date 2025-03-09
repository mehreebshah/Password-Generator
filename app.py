import streamlit as st
import random
import string
from io import BytesIO
import base64
import time

def generate_password(length=12, use_symbols=True, use_numbers=True, use_uppercase=True):
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    
    return ''.join(random.choice(characters) for _ in range(length))


def analyze_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Increase password length to at least 8 characters.")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Include at least one lowercase letter.")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Include at least one uppercase letter.")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Include at least one digit (0-9).")
    
    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")
    
    strength = "Weak" if score <= 2 else "Moderate" if score <= 4 else "Strong"
    
    return strength, feedback

st.set_page_config(page_title="Password Generator & Strength Meter", page_icon="🔐", layout="centered")



st.title("🔐 Unique Password Generator & Strength Meter")
st.header("🔍 Check Your Password Strength")
user_password = st.text_input("Enter your password to check strength", type="password")
if st.button("Check Strength"):
    if user_password:
        strength, feedback = analyze_strength(user_password)
        st.write(f"Password Strength: **{strength}**")
        if strength == "Weak":
            st.warning("Improve your password with the following suggestions:")
            for tip in feedback:
                st.write(f"- {tip}")
        elif strength == "Strong":
            st.success("Your password is strong and secure!")
    else:
        st.error("Please enter a password to check.")

password_history = st.session_state.get("password_history", [])
length = st.slider("Password Length", 8, 32, 12)
use_symbols = st.checkbox("Include Symbols", True)
use_numbers = st.checkbox("Include Numbers", True)
use_uppercase = st.checkbox("Include Uppercase", True)

if st.button("Generate Password"):
    with st.spinner("Generating password..."):
        time.sleep(1)
        password = generate_password(length, use_symbols, use_numbers, use_uppercase)
        strength, feedback = analyze_strength(password)
        password_history.append(password)
        st.session_state["password_history"] = password_history
        st.success(f"Generated Password: `{password}`")
        st.write(f"Password Strength: **{strength}**")
    
    if strength == "Weak":
        st.warning("Improve your password with the following suggestions:")
        for tip in feedback:
            st.write(f"- {tip}")
    elif strength == "Strong":
        st.success("Your password is strong and secure!")
   
st.header("📜 Password History")
if password_history:
    st.write("Recent Passwords:")
    for pwd in password_history[-5:]:
        st.code(pwd)


st.write('Build with ❤️ by [Areeba Shah](https://github.com/mehreebshah?tab=repositories)')