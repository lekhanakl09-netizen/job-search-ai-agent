import streamlit as st
import pymupdf
import sqlite3
from datetime import datetime
 
st.set_page_config(page_title="Job Search AI Assistant", page_icon="💼", layout="wide")
st.title("💼 Job Search AI Assistant")
st.write("👋 Welcome! I am your AI Job Search Assistant!")
st.write("🎯 I will help you find your dream job!")
st.write("📌 Choose a tool from the left sidebar to get started!")
st.write("---")
st.sidebar.title("Choose a Tool")
 
tool = st.sidebar.selectbox("Select Tool:",
    ["Job Search", "Resume Parser", "Company Research", "Job Matching", "Multiple Job Platforms", "Saved Jobs"])
 
# Database setup
conn = sqlite3.connect("jobs.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS saved_jobs
             (id INTEGER PRIMARY KEY, title TEXT, company TEXT, salary TEXT, location TEXT, platform TEXT, date TEXT)''')
conn.commit()
 
ALL_JOBS = [
    {"title": "Python Developer", "company": "Infosys", "salary": "4-6 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["python"], "wfh": "Yes", "notice": "30 days"},
    {"title": "Software Engineer", "company": "TCS", "salary": "3-5 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["java", "python"], "wfh": "No", "notice": "60 days"},
    {"title": "Backend Developer", "company": "Wipro", "salary": "5-8 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["python", "css"], "wfh": "Yes", "notice": "30 days"},
    {"title": "Frontend Intern", "company": "Flipkart", "salary": "15,000/month", "platform": "Internshala", "apply": "https://internshala.com", "skills": ["html", "css"], "wfh": "Yes", "notice": "15 days"},
    {"title": "Data Analyst", "company": "Amazon", "salary": "6-10 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "sql"], "wfh": "No", "notice": "60 days"},
    {"title": "ML Engineer", "company": "Google", "salary": "15-25 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "ml"], "wfh": "Yes", "notice": "90 days"},
    {"title": "Java Developer", "company": "IBM", "salary": "5-8 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["java"], "wfh": "No", "notice": "30 days"},
    {"title": "DevOps Engineer", "company": "Microsoft", "salary": "10-15 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["devops", "linux"], "wfh": "Yes", "notice": "60 days"},
    {"title": "Android Developer", "company": "Swiggy", "salary": "6-10 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["android", "java"], "wfh": "No", "notice": "30 days"},
    {"title": "iOS Developer", "company": "Zomato", "salary": "8-12 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["ios", "swift"], "wfh": "Yes", "notice": "60 days"},
    {"title": "UI/UX Designer", "company": "Myntra", "salary": "5-9 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["design", "figma"], "wfh": "Yes", "notice": "30 days"},
    {"title": "Data Scientist", "company": "Paytm", "salary": "10-18 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["python", "ml", "sql"], "wfh": "No", "notice": "60 days"},
    {"title": "React Developer", "company": "Meesho", "salary": "6-10 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["react", "javascript", "html"], "wfh": "Yes", "notice": "30 days"},
    {"title": "Full Stack Developer", "company": "Ola", "salary": "8-14 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "javascript", "html"], "wfh": "Yes", "notice": "60 days"},
    {"title": "Network Engineer", "company": "Tech Mahindra", "salary": "4-8 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["networking", "security"], "wfh": "No", "notice": "30 days"},
]
 
if tool == "Job Search":
    st.header("🔍 Job Search Tool")
    user_input = st.text_input("What kind of job?")
    location = st.selectbox("Select City:", ["Bangalore", "Mumbai", "Delhi", "Pune", "Hyderabad"])
    platform = st.selectbox("Select Platform:", ["All", "Naukri", "TimesJobs", "LinkedIn", "Indeed", "Internshala"])
    wfh = st.selectbox("Work From Home:", ["Any", "Yes", "No"])
 
    if st.button("Search Jobs"):
        if user_input:
            filtered = ALL_JOBS
            if platform != "All":
                filtered = [j for j in filtered if j["platform"] == platform]
            if wfh != "Any":
                filtered = [j for j in filtered if j["wfh"] == wfh]
 
            st.success(f"Found {len(filtered)} jobs in {location}!")
            for job in filtered:
                with st.container():
                    st.subheader(f"{job['title']} - {job['company']}")
                    st.write(f"💰 Salary: {job['salary']}")
                    st.write(f"🌐 Platform: {job['platform']}")
                    st.write(f"📍 Location: {location}")
                    st.write(f"🏠 Work From Home: {job['wfh']}")
                    st.write(f"⏰ Notice Period: {job['notice']}")
                    st.markdown(f"[🔗 Apply Here]({job['apply']})")
                    if st.button(f"Save {job['title']}", key=job['title']):
                        c.execute("INSERT INTO saved_jobs VALUES (NULL,?,?,?,?,?,?)",
                            (job['title'], job['company'], job['salary'], location, job['platform'], datetime.now().strftime("%Y-%m-%d")))
                        conn.commit()
                        st.success("Job Saved!")
                    st.write("---")
        else:
            st.warning("Please enter job title!")
 
elif tool == "Resume Parser":
    st.header("📄 Resume Parser Tool")
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
 
elif tool == "Company Research":
    st.header("🏢 Company Research Tool")
    company = st.text_input("Enter Company Name:")
    if st.button("Research Company"):
        if company:
            st.success(f"Company Info for {company}")
            st.write(f"**Company:** {company}")
            st.write("**Industry:** IT/Software")
            st.write("**Location:** Bangalore, India")
            st.write("**Employees:** 10,000+")
            st.write("**Rating:** 4.2/5")
            st.write("**Culture:** Work life balance, Good benefits")
            st.write("**Notice Period:** 60 days")
            st.write("**Work From Home:** Available")
 
elif tool == "Job Matching":
    st.header("🎯 Job Matching by Skills")
    skills = st.text_input("Enter your skills (e.g. python, html, css):")
    experience = st.selectbox("Experience:", ["Fresher", "1-3 years", "3-5 years", "5+ years"])
    location = st.selectbox("Preferred City:", ["Bangalore", "Mumbai", "Delhi", "Pune", "Hyderabad"])
    wfh = st.selectbox("Work From Home:", ["Any", "Yes", "No"])
 
    if st.button("Find Matching Jobs"):
        if skills:
            skill_list = [s.strip().lower() for s in skills.split(",")]
            matched = []
            for job in ALL_JOBS:
                if any(skill in skill_list for skill in job["skills"]):
                    if wfh == "Any" or job["wfh"] == wfh:
                        matched.append(job)
            if matched:
                st.success(f"Found {len(matched)} matching jobs!")
                for job in matched:
                    with st.container():
                        st.subheader(f"{job['title']} - {job['company']}")
                        st.write(f"💰 Salary: {job['salary']}")
                        st.write(f"🌐 Platform: {job['platform']}")
                        st.write(f"🏠 Work From Home: {job['wfh']}")
                        st.write(f"⏰ Notice Period: {job['notice']}")
                        st.markdown(f"[🔗 Apply Here]({job['apply']})")
                        st.write("---")
            else:
                st.warning("No matching jobs found!")
 
elif tool == "Multiple Job Platforms":
    st.header("🌐 Multiple Job Platforms")
    role = st.text_input("Enter Job Role:")
    city = st.selectbox("Select City:", ["Bangalore", "Mumbai", "Delhi", "Pune", "Hyderabad"])
 
    if st.button("Show Platform Jobs"):
<<<<<<< HEAD
        if role:
            st.success(f"Showing jobs for {role} in {city}")
            platforms = ["Naukri", "TimesJobs", "LinkedIn", "Indeed", "Internshala"]
            for platform in platforms:
                platform_jobs = [j for j in ALL_JOBS if j["platform"] == platform]
                st.subheader(f"🌐 {platform}")
                for job in platform_jobs[:2]:
                    st.write(f"**{job['title']}** - {job['company']}")
                    st.write(f"💰 {job['salary']} | 📍 {city}")
                    st.markdown(f"[🔗 Apply]({job['apply']})")
                st.write("---")
 
elif tool == "Saved Jobs":
    st.header("💾 Saved Jobs")
    saved = c.execute("SELECT * FROM saved_jobs").fetchall()
    if saved:
        st.success(f"You have {len(saved)} saved jobs!")
        for job in saved:
            st.write(f"**{job[1]}** - {job[2]}")
            st.write(f"💰 {job[3]} | 📍 {job[4]} | 🌐 {job[5]}")
            st.write(f"📅 Saved on: {job[6]}")
            st.write("---")
    else:
        st.warning("No saved jobs yet! Search and save jobs!")
 
=======
        if role and city:
            st.success(f"Showing {len(ALL_JOBS)} jobs for {role} in {city}")
            for job in ALL_JOBS:
                with st.container():
                    st.subheader(f"{job['title']} - {job['company']}")
                    st.write(f"💰 Salary: {job['salary']}")
                    st.write(f"🌐 Platform: {job['platform']}")
                    st.write(f"📍 Location: {city}")
                    st.markdown(f"[🔗 Apply Here]({job['apply']})")
                    st.write("---")
        else:
            st.warning("Please enter both role and city!")
>>>>>>> 680be0bd4e69bbece7b5fde25a9a503db3ac7bec
