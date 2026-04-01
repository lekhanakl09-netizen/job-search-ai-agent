import streamlit as st

st.title("Job Search AI Assistant")
st.write("Find jobs across India!")

user_input = st.text_input("What kind of job are you looking for?")
location = st.text_input("Which city?")

jobs = [
    {"title": "Python Developer", "company": "Infosys", "salary": "4-6 LPA", "location": "Bangalore"},
    {"title": "Python Engineer", "company": "TCS", "salary": "3-5 LPA", "location": "Bangalore"},
    {"title": "Software Developer", "company": "Wipro", "salary": "5-8 LPA", "location": "Bangalore"},
    {"title": "Backend Developer", "company": "Flipkart", "salary": "8-12 LPA", "location": "Bangalore"},
    {"title": "Junior Developer", "company": "Accenture", "salary": "3-4 LPA", "location": "Bangalore"},
]

if st.button("Search Jobs"):
    if user_input and location:
        st.success(f"Found {len(jobs)} jobs!")
        for job in jobs:
            st.write(f"**{job['title']}** - {job['company']}")
            st.write(f"📍 {job['location']} | 💰 {job['salary']}")
            st.write("---")
    else:
        st.warning("Please enter job title and location!")