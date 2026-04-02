import streamlit as st
import pymupdf

st.title("Job Search AI Assistant")
st.sidebar.title("Choose a Tool")

tool = st.sidebar.selectbox(
    "Select Tool:",
    ["Job Search", "Resume Parser", "Company Research", "Job Matching"]
)

# ---------------- JOB SEARCH ----------------
if tool == "Job Search":
    st.header("Job Search Tool")
    user_input = st.text_input("What kind of job?")
    location = st.text_input("Which city?")

    if st.button("Search Jobs"):
        if user_input and location:
            jobs = [
                {"title": "Python Developer", "company": "Infosys", "salary": "4-6 LPA"},
                {"title": "Software Engineer", "company": "TCS", "salary": "3-5 LPA"},
                {"title": "Backend Developer", "company": "Wipro", "salary": "5-8 LPA"},
            ]

            st.success(f"Found {len(jobs)} jobs!")

            for job in jobs:
                st.write(f"**{job['title']}** - {job['company']}")
                st.write(f"💰 {job['salary']}")
                st.write("---")
        else:
            st.warning("Please enter both job role and city!")

# ---------------- RESUME PARSER ----------------
elif tool == "Resume Parser":
    st.header("Resume Parser Tool")
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

    if uploaded_file:
        doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""

        for page in doc:
            text += page.get_text("text")

        if text.strip():
            st.success("Resume parsed successfully!")
            st.text_area("Resume Content:", text, height=300)
        else:
            st.warning("PDF has no readable text!")
            st.info("Try a different PDF file!")

# ---------------- COMPANY RESEARCH ----------------
elif tool == "Company Research":
    st.header("Company Research Tool")
    company = st.text_input("Enter Company Name:")

    if st.button("Research Company"):
        if company:
            st.success(f"Company Info for {company}")
            st.write(f"**Company:** {company}")
            st.write("**Industry:** IT/Software")
            st.write("**Location:** Bangalore, India")
            st.write("**Employees:** 10,000+")
            st.write("**Rating:** 4.2/5")
        else:
            st.warning("Please enter a company name!")

# ---------------- JOB MATCHING ----------------
elif tool == "Job Matching":
    st.header("Job Matching by Skills")

    skills = st.text_input("Enter your skills (e.g. Python, HTML, CSS):")
    experience = st.selectbox("Experience:", ["Fresher", "1-3 years", "3-5 years", "5+ years"])

    if st.button("Find Matching Jobs"):
        if skills:
            skill_list = [s.strip().lower() for s in skills.split(",")]

            jobs = [
                {"title": "Python Developer", "company": "Infosys", "salary": "4-6 LPA", "skills": ["python"]},
                {"title": "Web Developer", "company": "TCS", "salary": "3-5 LPA", "skills": ["html", "css"]},
                {"title": "Backend Engineer", "company": "Wipro", "salary": "5-8 LPA", "skills": ["python", "css"]},
                {"title": "Frontend Developer", "company": "Flipkart", "salary": "6-10 LPA", "skills": ["html", "css", "javascript"]},
            ]

            matched = []

            for job in jobs:
                if any(skill in skill_list for skill in job["skills"]):
                    matched.append(job)

            if matched:
                st.success(f"Found {len(matched)} matching jobs!")

                for job in matched:
                    st.write(f"**{job['title']}** - {job['company']}")
                    st.write(f"💰 {job['salary']}")
                    st.write(f"🛠 Skills Needed: {', '.join(job['skills'])}")
                    st.write("---")
            else:
                st.warning("No matching jobs found! Try different skills!")
        else:
            st.warning("Please enter at least one skill!")