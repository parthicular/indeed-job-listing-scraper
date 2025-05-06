import os
import csv
import json
import time
import random
from datetime import datetime
from tqdm import tqdm
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# -------- CONFIG v1.1 --------
# search_keywords = ["Journalist", "Reporter", "Editor", "Writer", "SEO"]
search_keywords = [ 
    "News Editor",
    "Freelance Writer",
    "Technical Content Writer",
    "Data Analyst"
]
locations = [""]  # Empty location = search all
max_pages = 5

scrape_date = datetime.now().strftime("%Y-%m-%d")
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Filenames for full and split outputs
csv_filename    = os.path.join(output_dir, f"jobs_scraped_{timestamp}.csv")
json_filename   = os.path.join(output_dir, f"jobs_scraped_{timestamp}.json")
easy_csv        = os.path.join(output_dir, f"easy_apply_{timestamp}.csv")
manual_csv      = os.path.join(output_dir, f"manual_apply_{timestamp}.csv")

seen_job_ids = set()
all_jobs = []

# Selenium
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0")
# Check Specify Chrome version 
driver = uc.Chrome(version_main=135, options=options)

# Scraper
def scrape_jobs():
    for keyword in tqdm(search_keywords, desc="Searching", unit="kw"):
        for location in locations:
            query = keyword.replace(" ", "+")
            base_url = f"https://uk.indeed.com/jobs?q={query}"
            if location.strip():
                base_url += f"&l={location.replace(' ', '+')}"

            for page in range(max_pages):
                url = f"{base_url}&start={page * 10}"
                print(f"\n🌍 Fetching: {url}")
                try:
                    driver.get(url)
                except Exception as e:
                    print(f"⚠️ Failed to load page: {e}")
                    continue
                time.sleep(random.uniform(5, 8))

                cards = driver.find_elements(By.CLASS_NAME, "cardOutline")
                print(f"🔎 Found {len(cards)} job cards on page {page+1}")

                for card in cards:
                    try:
                        # Extract title
                        try:
                            title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle").text.strip()
                        except NoSuchElementException:
                            title = "Unknown"

                        # Extract link & job_id
                        try:
                            link = card.find_element(By.CLASS_NAME, "jcs-JobTitle").get_attribute("href")
                        except NoSuchElementException:
                            link = ""
                        job_id = link.split("jk=")[-1].split("&")[0] if "jk=" in link else f"unknown_{random.randint(100000,999999)}"
                        if job_id in seen_job_ids:
                            continue
                        seen_job_ids.add(job_id)

                        # Easy Apply
                        easy_apply = "Yes" if "Easily apply" in card.text else "No"

                        # Click to open details for company & description
                        card.click()
                        time.sleep(random.uniform(1.5, 3))

                        # Extract company
                        try:
                            company = driver.find_element(By.CSS_SELECTOR, "#jobsearch-ViewjobPaneWrapper a").text.strip()
                        except NoSuchElementException:
                            company = "Unknown"

                        # Extract job description text
                        try:
                            description = driver.find_element(By.ID, "jobDescriptionText").text.strip()
                        except NoSuchElementException:
                            description = ""

                        # Assemble job data
                        job_data = {
                            "job_title": title,
                            "company": company,
                            "job_link": link,
                            "easy_apply": easy_apply,
                            "description": description,
                            "job_id": job_id,
                            "source_keyword": keyword,
                            "scrape_date": scrape_date
                        }
                        all_jobs.append(job_data)
                        print(f"Saved job: {title} | Company: {company}")

                    except Exception as err:
                        print(f"Error scraping job card: {err}")
                        continue

# -------- SAVE UTILITIES --------
def save_csv(data, filename):
    if not data:
        print(f"No data to save for {filename}")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"CSV saved: {filename}")


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"JSON saved: {filename}")

# main
if __name__ == "__main__":
    try:
        scrape_jobs()
        if all_jobs:
            # Save complete datasets
            save_csv(all_jobs, csv_filename)
            save_json(all_jobs, json_filename)

            # Split into easy & manual apply lists
            easy    = [job for job in all_jobs if job.get("easy_apply") == "Yes"]
            manual  = [job for job in all_jobs if job.get("easy_apply") != "Yes"]

            save_csv(easy, easy_csv)
            save_csv(manual, manual_csv)
            print(f"Easy-apply CSV: {easy_csv}")
            print(f"Manual-apply CSV: {manual_csv}")
        else:
            print("No jobs scraped.")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        driver.quit()
        print("Done. Chrome closed.")
