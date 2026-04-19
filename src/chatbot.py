import streamlit as st
import pymupdf
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
 
st.set_page_config(page_title="Job Search AI Assistant", page_icon="💼", layout="wide")
 
# Professional Header
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .job-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2a5298;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)
 
st.markdown('<div class="main-header"><h1>💼 Job Search AI Assistant</h1><p>Your Career Partner for Indian Job Market</p></div>', unsafe_allow_html=True)
 
st.sidebar.title("🛠️ Choose a Tool")
tool = st.sidebar.selectbox("Select Tool:",
    ["Job Search", "Resume Parser", "Company Research", "Job Matching", "Multiple Job Platforms", "Saved Jobs", "Export Jobs"])
 
# Database setup
conn = sqlite3.connect("jobs.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS saved_jobs
             (id INTEGER PRIMARY KEY, title TEXT, company TEXT, salary TEXT, location TEXT, platform TEXT, date TEXT)''')
conn.commit()
 
ALL_JOBS = [
    # Bangalore - Naukri
    {"title": "Python Developer", "company": "Infosys", "salary": "4-6 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["python"], "wfh": "Yes", "notice": "30 days", "city": "Bangalore"},
    {"title": "Backend Developer", "company": "Wipro", "salary": "5-8 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["python", "css"], "wfh": "No", "notice": "30 days", "city": "Bangalore"},
    {"title": "Java Developer", "company": "HCL", "salary": "5-8 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["java"], "wfh": "Yes", "notice": "30 days", "city": "Bangalore"},
    {"title": "Android Developer", "company": "Swiggy", "salary": "6-10 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["android", "java"], "wfh": "No", "notice": "30 days", "city": "Bangalore"},
    {"title": "Software Engineer", "company": "TCS", "salary": "3-5 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["java", "python"], "wfh": "Yes", "notice": "60 days", "city": "Bangalore"},
    {"title": "DevOps Engineer", "company": "Microsoft", "salary": "10-15 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["devops", "linux"], "wfh": "Yes", "notice": "60 days", "city": "Bangalore"},
    {"title": "Full Stack Developer", "company": "Ola", "salary": "8-14 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["python", "javascript"], "wfh": "Yes", "notice": "60 days", "city": "Bangalore"},
    {"title": "Data Scientist", "company": "Flipkart", "salary": "10-18 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "ml"], "wfh": "Yes", "notice": "60 days", "city": "Bangalore"},
    {"title": "ML Engineer", "company": "Google", "salary": "15-25 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "ml"], "wfh": "Yes", "notice": "90 days", "city": "Bangalore"},
    {"title": "DevOps Engineer", "company": "Amazon", "salary": "10-15 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["devops", "linux"], "wfh": "Yes", "notice": "60 days", "city": "Bangalore"},
    {"title": "React Developer", "company": "Razorpay", "salary": "6-10 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["react", "javascript"], "wfh": "Yes", "notice": "30 days", "city": "Bangalore"},
    {"title": "Frontend Intern", "company": "Flipkart", "salary": "15,000/month", "platform": "Internshala", "apply": "https://internshala.com", "skills": ["html", "css"], "wfh": "Yes", "notice": "15 days", "city": "Bangalore"},
    # Mumbai
    {"title": "Finance Analyst", "company": "HDFC Bank", "salary": "5-10 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["finance", "excel"], "wfh": "No", "notice": "60 days", "city": "Mumbai"},
    {"title": "Cloud Engineer", "company": "Accenture", "salary": "8-14 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["cloud", "aws"], "wfh": "Yes", "notice": "60 days", "city": "Mumbai"},
    {"title": "Java Developer", "company": "IBM", "salary": "5-8 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["java"], "wfh": "Yes", "notice": "30 days", "city": "Mumbai"},
    {"title": "Data Analyst", "company": "Reliance", "salary": "6-10 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["python", "sql"], "wfh": "No", "notice": "30 days", "city": "Mumbai"},
    {"title": "ML Engineer", "company": "Tata", "salary": "12-20 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "ml"], "wfh": "Yes", "notice": "90 days", "city": "Mumbai"},
    {"title": "Python Developer", "company": "Capgemini", "salary": "4-7 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["python"], "wfh": "Yes", "notice": "30 days", "city": "Mumbai"},
    # Delhi
    {"title": "Digital Marketing", "company": "Razorpay", "salary": "4-7 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["marketing", "seo"], "wfh": "Yes", "notice": "30 days", "city": "Delhi"},
    {"title": "Network Engineer", "company": "HCL", "salary": "4-8 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["networking", "security"], "wfh": "No", "notice": "30 days", "city": "Delhi"},
    {"title": "Full Stack Developer", "company": "Tech Mahindra", "salary": "8-14 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "javascript"], "wfh": "Yes", "notice": "60 days", "city": "Delhi"},
    {"title": "Data Analyst", "company": "Microsoft", "salary": "8-12 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["python", "sql"], "wfh": "Yes", "notice": "60 days", "city": "Delhi"},
    {"title": "Android Developer", "company": "Samsung", "salary": "6-10 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["android", "java"], "wfh": "Yes", "notice": "30 days", "city": "Delhi"},
    {"title": "React Developer", "company": "Infosys", "salary": "5-8 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["react", "javascript"], "wfh": "Yes", "notice": "30 days", "city": "Delhi"},
    # Pune
    {"title": "Software Engineer", "company": "Infosys", "salary": "3-6 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["java", "python"], "wfh": "Yes", "notice": "30 days", "city": "Pune"},
    {"title": "iOS Developer", "company": "Zomato", "salary": "8-12 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["ios", "swift"], "wfh": "Yes", "notice": "60 days", "city": "Pune"},
    {"title": "DevOps Engineer", "company": "Capgemini", "salary": "8-14 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["devops", "linux"], "wfh": "No", "notice": "60 days", "city": "Pune"},
    {"title": "React Developer", "company": "Cognizant", "salary": "5-9 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["react", "javascript"], "wfh": "Yes", "notice": "30 days", "city": "Pune"},
    {"title": "Cloud Engineer", "company": "TCS", "salary": "7-12 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["cloud", "aws"], "wfh": "Yes", "notice": "60 days", "city": "Pune"},
    # Hyderabad
    {"title": "ML Engineer", "company": "Google", "salary": "15-25 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "ml"], "wfh": "Yes", "notice": "90 days", "city": "Hyderabad"},
    {"title": "Cybersecurity Analyst", "company": "Deloitte", "salary": "6-12 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["security", "networking"], "wfh": "No", "notice": "30 days", "city": "Hyderabad"},
    {"title": "Java Developer", "company": "Oracle", "salary": "6-10 LPA", "platform": "Naukri", "apply": "https://www.naukri.com", "skills": ["java"], "wfh": "Yes", "notice": "30 days", "city": "Hyderabad"},
    {"title": "Data Scientist", "company": "Amazon", "salary": "12-20 LPA", "platform": "LinkedIn", "apply": "https://www.linkedin.com", "skills": ["python", "ml", "sql"], "wfh": "Yes", "notice": "60 days", "city": "Hyderabad"},
    {"title": "Full Stack Developer", "company": "Microsoft", "salary": "10-16 LPA", "platform": "TimesJobs", "apply": "https://www.timesjobs.com", "skills": ["python", "javascript"], "wfh": "Yes", "notice": "60 days", "city": "Hyderabad"},
    {"title": "UI/UX Designer", "company": "Apple", "salary": "8-14 LPA", "platform": "Indeed", "apply": "https://www.indeed.com", "skills": ["design", "figma"], "wfh": "Yes", "notice": "30 days", "city": "Hyderabad"},
]
 
if tool == "Job Search":
    st.header("🔍 Job Search Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        user_input = st.text_input("🔍 What kind of job?")
        location = st.selectbox("📍 Select City:", ["Bangalore", "Mumbai", "Delhi", "Pune", "Hyderabad"])
    with col2:
        platform = st.selectbox("🌐 Select Platform:", ["All", "Naukri", "TimesJobs", "LinkedIn", "Indeed", "Internshala"])
        wfh = st.selectbox("🏠 Work From Home:", ["Any", "Yes", "No"])
 
    if st.button("🔍 Search Jobs", use_container_width=True):
        if user_input:
            filtered = [j for j in ALL_JOBS if j["city"] == location]
            if platform != "All":
                filtered = [j for j in filtered if j["platform"] == platform]
            if wfh != "Any":
                filtered = [j for j in filtered if j["wfh"] == wfh]
            if filtered:
                st.success(f"✅ Found {len(filtered)} jobs in {location}!")
                for job in filtered:
                    st.markdown(f"""
                    <div class="job-card">
                        <h3>{job['title']} - {job['company']}</h3>
                        <p>💰 {job['salary']} | 🌐 {job['platform']} | 📍 {location}</p>
                        <p>🏠 WFH: {job['wfh']} | ⏰ Notice: {job['notice']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"[🔗 Apply Here]({job['apply']})")
                    with col2:
                        if st.button(f"💾 Save", key=job["title"]+location+job["platform"]):
                            c.execute("INSERT INTO saved_jobs VALUES (NULL,?,?,?,?,?,?)",
                                (job['title'], job['company'], job['salary'], location, job['platform'], datetime.now().strftime("%Y-%m-%d")))
                            conn.commit()
                            st.success("Saved!")
                    st.write("---")
            else:
                st.error("❌ No jobs found! Try different filters!")
        else:
            st.warning("⚠️ Please enter job title!")
 
elif tool == "Resume Parser":
    st.header("📄 Resume Parser & Analysis")
    uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type="pdf")
    if uploaded_file:
        if uploaded_file.type != "application/pdf":
            st.error("❌ Please upload PDF files only!")
        else:
            doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text("text")
            if text.strip():
                st.success("✅ Resume parsed successfully!")
                st.text_area("📄 Resume Content:", text, height=300)
                st.info(f"📊 Total Characters: {len(text)} | Total Pages: {len(doc)}")
            else:
                st.error("❌ PDF has no readable text! Try a different PDF!")
 
elif tool == "Company Research":
    st.header("🏢 Company Research & Insights")
    company = st.text_input("Enter Company Name:")
    if not company:
        st.warning("⚠️ Please enter a company name!")
    if st.button("🔍 Research Company"):
        if company:
            st.success(f"✅ Company Info for {company}")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**🏢 Company:** {company}")
                st.write("**🏭 Industry:** IT/Software")
                st.write("**📍 Location:** Bangalore, India")
                st.write("**👥 Employees:** 10,000+")
            with col2:
                st.write("**⭐ Rating:** 4.2/5")
                st.write("**🌟 Culture:** Work life balance")
                st.write("**⏰ Notice Period:** 60 days")
                st.write("**🏠 Work From Home:** Available")
 
elif tool == "Job Matching":
    st.header("🎯 Job Matching by Skills")
    col1, col2 = st.columns(2)
    with col1:
        skills = st.text_input("🛠️ Enter your skills (e.g. python, html, css):")
        experience = st.selectbox("💼 Experience:", ["Fresher", "1-3 years", "3-5 years", "5+ years"])
    with col2:
        location = st.selectbox("📍 Preferred City:", ["Bangalore", "Mumbai", "Delhi", "Pune", "Hyderabad"])
        wfh = st.selectbox("🏠 Work From Home:", ["Any", "Yes", "No"])
 
    if st.button("🎯 Find Matching Jobs", use_container_width=True):
        if skills:
            skill_list = [s.strip().lower() for s in skills.split(",")]
            matched = [j for j in ALL_JOBS if j["city"] == location and
                      any(skill in skill_list for skill in j["skills"]) and
                      (wfh == "Any" or j["wfh"] == wfh)]
            if matched:
                st.success(f"✅ Found {len(matched)} matching jobs in {location}!")
                for job in matched:
                    st.markdown(f"""
                    <div class="job-card">
                        <h3>{job['title']} - {job['company']}</h3>
                        <p>💰 {job['salary']} | 🌐 {job['platform']} | 🏠 WFH: {job['wfh']}</p>
                        <p>⏰ Notice: {job['notice']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"[🔗 Apply Here]({job['apply']})")
                    st.write("---")
            else:
                st.error("❌ No matching jobs! Try different skills or city!")
        else:
            st.warning("⚠️ Please enter at least one skill!")
 
elif tool == "Multiple Job Platforms":
    st.header("🌐 Multiple Job Platforms")
    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("💼 Enter Job Role:")
    with col2:
        city = st.selectbox("📍 Select City:", ["Bangalore", "Mumbai", "Delhi", "Pune", "Hyderabad"])
 
    if st.button("🔍 Show Platform Jobs", use_container_width=True):
        if role:
            platforms = ["Naukri", "TimesJobs", "LinkedIn", "Indeed", "Internshala"]
            for platform in platforms:
                platform_jobs = [j for j in ALL_JOBS if j["platform"] == platform and j["city"] == city]
                if platform_jobs:
                    st.subheader(f"🌐 {platform}")
                    for job in platform_jobs:
                        st.write(f"**{job['title']}** - {job['company']}")
                        st.write(f"💰 {job['salary']} | 🏠 WFH: {job['wfh']} | ⏰ {job['notice']}")
                        st.markdown(f"[🔗 Apply]({job['apply']})")
                    st.write("---")
        else:
            st.warning("⚠️ Please enter job role!")
 
elif tool == "Saved Jobs":
    st.header("💾 Saved Jobs")
    saved = c.execute("SELECT * FROM saved_jobs").fetchall()
    if saved:
        st.success(f"✅ You have {len(saved)} saved jobs!")
        for job in saved:
            st.markdown(f"""
            <div class="job-card">
                <h3>{job[1]} - {job[2]}</h3>
                <p>💰 {job[3]} | 📍 {job[4]} | 🌐 {job[5]}</p>
                <p>📅 Saved on: {job[6]}</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("---")
    else:
        st.warning("⚠️ No saved jobs yet! Search and save jobs!")
 
elif tool == "Export Jobs":
    st.header("📤 Export Job List to PDF")
    city = st.selectbox("📍 Select City:", ["Bangalore", "Mumbai", "Delhi", "Pune", "Hyderabad"])
    platform = st.selectbox("🌐 Select Platform:", ["All", "Naukri", "TimesJobs", "LinkedIn", "Indeed"])
 
    if st.button("📥 Export to PDF", use_container_width=True):
        filtered = [j for j in ALL_JOBS if j["city"] == city]
        if platform != "All":
            filtered = [j for j in filtered if j["platform"] == platform]
 
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(200, 750, "Job Search AI Assistant")
        p.setFont("Helvetica", 12)
        p.drawString(200, 730, f"Jobs in {city} - {platform}")
        p.drawString(200, 710, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        y = 680
        for job in filtered:
            if y < 100:
                p.showPage()
                y = 750
            p.setFont("Helvetica-Bold", 11)
            p.drawString(50, y, f"{job['title']} - {job['company']}")
            p.setFont("Helvetica", 10)
            p.drawString(50, y-15, f"Salary: {job['salary']} | Platform: {job['platform']} | WFH: {job['wfh']}")
            p.drawString(50, y-30, f"Notice Period: {job['notice']}")
            y -= 50
        p.save()
        buffer.seek(0)
        st.download_button(
            label="📥 Download PDF",
            data=buffer,
            file_name=f"jobs_{city}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
        st.success("✅ PDF ready to download!")