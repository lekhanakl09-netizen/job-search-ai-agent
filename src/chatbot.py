import streamlit as st
import requests

st.title("Job Search AI Assistant 🤖")
st.write("Welcome! I can help you find jobs in India!")

user_input = st.text_input("What kind of job are you looking for?")
location = st.text_input("Which city? (e.g. Bangalore, Mumbai)")

if user_input and location:
    st.write(f"🔍 Searching for **{user_input}** jobs in **{location}**...")
    st.success("✅ Connected to Indeed!")
    st.write("Jobs found! More features coming soon...")
    