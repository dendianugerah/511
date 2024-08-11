import json
import os
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import re

from datetime import datetime, timedelta
import re

# Fungsi untuk mengonversi string waktu menjadi objek datetime
def convert_string_to_datetime(date_str):
    now = datetime.now()

    # Pattern regex untuk menangkap angka dan unit waktu (hari, jam, menit, dll.)
    time_patterns = {
        'hari': r'(\d+)\s*hari',
        'jam': r'(\d+)\s*jam',
        'menit': r'(\d+)\s*menit',
    }

    total_timedelta = timedelta()

    # Memeriksa setiap unit waktu dan menambahkannya ke total_timedelta
    for unit, pattern in time_patterns.items():
        match = re.search(pattern, date_str)
        if match:
            value = int(match.group(1))
            if unit == 'hari':
                total_timedelta += timedelta(days=value)
            elif unit == 'jam':
                total_timedelta += timedelta(hours=value)
            elif unit == 'menit':
                total_timedelta += timedelta(minutes=value)

    return now - total_timedelta

def get_jobs_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Temukan jumlah total pekerjaan
    job_found_count = int(soup.find("span", attrs={'data-automation': 'totalJobsCount'}).text.strip().replace(',', ''))
    
    # Temukan semua card pekerjaan
    job_list_card = soup.find_all("div", class_="_4603vi0 _9l8a1v6m")
    result_count = len(job_list_card)
    
    for job_card in job_list_card:
        content_card = job_card.find("div", class_="_4603vi0")
        article_card = content_card.find("article")
        # test = article_card.find("div", class_="_4603vi0 _9l8a1v5i _9l8a1v0 oq739e0")
        print(article_card)

        # Temukan judul pekerjaan

        
        # Konversi string waktu menjadi objek datetime
        # posted_date = convert_string_to_datetime(date_posted)
        # print(f"Posted date: {posted_date}")
    
    return job_found_count, result_count


def scrape_jobs(base_url, params):
    page_number = 1
    total_jobs = 0

    while True:
        
        if page_number == 1:
            url = f"{base_url}?{params}"
        else :
            url = f"{base_url}?page={page_number}&{params}"

        job_found_count, result_count = get_jobs_from_page(url)

        # Hitung total pekerjaan
        total_jobs += result_count

        print(f"Page {page_number}: Found {result_count} jobs, Total jobs found: {total_jobs}, {job_found_count}")
        print(f"URL: {url}")

        # Cek apakah kita sudah mengambil semua pekerjaan
        # if total_jobs >= job_found_count
        break
        
        page_number += 1

# URL target
base_url = "https://id.jobstreet.com/id/jobs"
params = 'sortmode=ListedDate'

# Mulai proses scraping
scrape_jobs(base_url, params)