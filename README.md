# Indeed Job Listing Scraper

A Python-based web scraper that automates job searches on Indeed and outputs results as CSV and JSON files. Designed for digital journalists, content strategists, and SEO professionals to gather and organize job listings quickly. Can be modified to search for any other role.

## Features

* Searches a customizable list of keywords (e.g., Digital Journalist, Content Strategist, SEO Specialist) across UK‑wide listings
* Scrapes up to 5 pages per keyword
* Extracts key fields: job title, company, link, "Easy Apply" flag, date posted, full description, job ID, source keyword, scrape date
* Deduplicates jobs by unique ID to avoid repeats
* Splits results into two CSVs: easy apply (`easy_apply_<timestamp>.csv`) and manual apply (`manual_apply_<timestamp>.csv`)
* Saves a complete dataset as both timestamped CSV and JSON in an `output/` folder
* Robust error handling with fallback values for missing fields
* Console logging for each saved job entry and a summary of saved files

## Prerequisites

* **Python 3.8+**
* **Google Chrome** (matching major version in the scraper setup)
* **pip** package manager
* **Git** (for repository management)


## Usage

1. **Ensure Chrome is installed and up to date.** Adjust `version_main` in `scrape_indeed.py` to match your Chrome's major version:

2. **Run the scraper script:**

3. **Click to prove you are not human. Do not switch from the window for long periods. Keep checking console logs** 

4. **Inspect outputs** in the `output/` directory:

   * `jobs_scraped_<timestamp>.csv` – complete dataset
   * `jobs_scraped_<timestamp>.json` – structured JSON
   * `easy_apply_<timestamp>.csv` – jobs flagged "Yes" for easy apply
   * `manual_apply_<timestamp>.csv` – other jobs

## License

This project is licensed under the MIT License. Feel free to fork, adapt, and contribute.
