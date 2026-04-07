import streamlit as st
import pymupdf
 
st.set_page_config(page_title="Job Search AI Assistant", page_icon="💼", layout="wide")
st.title("💼 Job Search AI Assistant")
st.write("👋 Welcome! I am your AI Job Search Assistant!")
st.write("🎯 I will help you find your dream job!")
st.write("📌 Choose a tool from the left sidebar to get started!")
st.write("---")
st.sidebar.title("Choose a Tool")
 
tool = st.sidebar.selectbox("Select Tool:",
    ["Job Search", "Resume Parser", "Company Research", "Job Matching", "Multiple Job Platforms"])
 
ALL_JOBS = [
    {"title": "Python Developer", "company": "Infosys", "salary": "4-6 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python"]},
    {"title": "Software Engineer", "company": "TCS", "salary": "3-5 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["java", "python"]},
    {"title": "Backend Developer", "company": "Wipro", "salary": "5-8 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["python", "css"]},
    {"title": "Frontend Intern", "company": "Flipkart", "salary": "15,000/month", "platform": "Internshala", "apply": "https://internshala.com", "skills": ["html", "css"]},
    {"title": "Data Analyst", "company": "Amazon", "salary": "6-10 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "sql"]},
    {"title": "ML Engineer", "company": "Google", "salary": "15-25 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "ml"]},
    {"title": "Java Developer", "company": "IBM", "salary": "5-8 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["java"]},
    {"title": "DevOps Engineer", "company": "Microsoft", "salary": "10-15 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["devops", "linux"]},
    {"title": "Android Developer", "company": "Swiggy", "salary": "6-10 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["android", "java"]},
    {"title": "iOS Developer", "company": "Zomato", "salary": "8-12 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["ios", "swift"]},
    {"title": "UI/UX Designer", "company": "Myntra", "salary": "5-9 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["design", "figma"]},
    {"title": "Graphic Designer", "company": "Byju's", "salary": "3-6 LPA", "platform": "Internshala", "apply": "https://internshala.com", "skills": ["design", "photoshop"]},
    {"title": "Cybersecurity Analyst", "company": "HCL", "salary": "6-12 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["security", "networking"]},
    {"title": "Cloud Engineer", "company": "Accenture", "salary": "8-14 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["cloud", "aws"]},
    {"title": "Digital Marketing", "company": "Razorpay", "salary": "4-7 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["marketing", "seo"]},
    {"title": "Finance Analyst", "company": "HDFC Bank", "salary": "5-10 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["finance", "excel"]},
    {"title": "Data Scientist", "company": "Paytm", "salary": "10-18 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "ml", "sql"]},
    {"title": "React Developer", "company": "Meesho", "salary": "6-10 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["react", "javascript", "html"]},
    {"title": "Full Stack Developer", "company": "Ola", "salary": "8-14 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "javascript", "html"]},
    {"title": "Network Engineer", "company": "Tech Mahindra", "salary": "4-8 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["networking", "security"]},
]
 
if tool == "Job Search":
    st.header("🔍 Job Search Tool")
    user_input = st.text_input("What kind of job?")
    location = st.text_input("Which city?")
    if st.button("Search Jobs"):
        if user_input and location:
            st.success(f"Found {len(ALL_JOBS)} jobs across multiple platforms!")
            for job in ALL_JOBS:
                with st.container():
                    st.subheader(f"{job['title']} - {job['company']}")
                    st.write(f"💰 Salary: {job['salary']}")
                    st.write(f"🌐 Platform: {job['platform']}")
                    st.write(f"📍 Location: {location}")
                    st.markdown(f"[🔗 Apply Here]({job['apply']})")
                    st.write("---")
        else:
            st.warning("Please enter both job role and city!")
 
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
            st.info("Try a different PDF file!")
 
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
        else:
            st.warning("Please enter a company name!")
 
elif tool == "Job Matching":
    st.header("🎯 Job Matching by Skills")
    skills = st.text_input("Enter your skills (e.g. Python, HTML, CSS):")
    experience = st.selectbox("Experience:", ["Fresher", "1-3 years", "3-5 years", "5+ years"])
    if st.button("Find Matching Jobs"):
        if skills:
            skill_list = [s.strip().lower() for s in skills.split(",")]
            matched = []
            for job in ALL_JOBS:
                if any(skill in skill_list for skill in job["skills"]):
                    matched.append(job)
            if matched:
                st.success(f"Found {len(matched)} matching jobs!")
                for job in matched:
                    with st.container():
                        st.subheader(f"{job['title']} - {job['company']}")
                        st.write(f"💰 Salary: {job['salary']}")
                        st.write(f"🌐 Platform: {job['platform']}")
                        st.markdown(f"[🔗 Apply Here]({job['apply']})")
                        st.write("---")
            else:
                st.warning("No matching jobs found! Try different skills!")
        else:
            st.warning("Please enter at least one skill!")
 
elif tool == "Multiple Job Platforms":
    st.header("🌐 Multiple Job Platforms")
    role = st.text_input("Enter Job Role:")
    city = st.text_input("Enter City:")
    if st.button("Show Platform Jobs"):
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
