import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import smtplib
from email.message import EmailMessage

# Load the categorized companies CSV file
file_path = "categorized_companies.csv"
df = pd.read_csv(file_path)

# Function to fetch job listings from Indeed using Selenium
def get_indeed_jobs(query, location="Massachusetts"):
    URL = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l={location}"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    time.sleep(3)  # Allow page to load
    
    jobs = []
    job_elements = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

    for job_card in job_elements[:10]:  # Get first 10 jobs
        try:
            title = job_card.find_element(By.CLASS_NAME, "jobTitle").text
            company = job_card.find_element(By.CLASS_NAME, "companyName").text
            link = job_card.find_element(By.TAG_NAME, "a").get_attribute("href")

            jobs.append({
                "title": title.strip(),
                "company": company.strip(),
                "link": link
            })
        except:
            continue

    driver.quit()
    return jobs

# Function to filter jobs based on categorized companies
def filter_jobs(jobs, category):
    company_list = df[df["Category"] == category]["Company Name"].tolist()
    return [job for job in jobs if any(company.lower() in job['company'].lower() for company in company_list)]

# Function to send job alerts via email
def send_email(subject, body):
    sender_email = "soumyabrata11411@gmail.com"
    receiver_email = "soumyabrataofficial02@gmail.com"
    password = "azvm hzyx llea mfoa"
    
    if not body.strip():
        print("No job updates to send.")
        return
    
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email sending failed: {e}")

# Main function to track jobs for each category
def daily_job_tracker():
    print("\n🔥 Daily Job Updates 🔥\n")
    job_results = ""
    
    for category in df["Category"].unique():
        print(f"📌 {category} Jobs:")
        jobs = get_indeed_jobs("insurance jobs")  # Broader search term
        filtered_jobs = filter_jobs(jobs, category)
        
        if not filtered_jobs:
            print("   No jobs found.")
            continue
        
        for job in filtered_jobs[:3]:  # Show 3 jobs per category
            job_entry = f"🔹 {job['title']} at {job['company']}\n   Apply: {job['link']}\n"
            print(job_entry)
            job_results += job_entry + "\n"
    
    # Send email notification (Optional)
    send_email("Daily Job Alert 🚀", job_results)
    
# Run the job tracker daily
daily_job_tracker()