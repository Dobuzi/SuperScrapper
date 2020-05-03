import requests
from bs4 import BeautifulSoup

def extract_pages(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    links = soup.find("div",  {"class": "s-pagination"}).find_all('a')
    pages = [int(link.span.string) for link in links[:-1]]
    return pages[-1]

def extract_jobs(last_page, URL):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping SO page {page+1}')
        html = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(html.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            jobs.append(extract_job(result))
    return jobs

def extract_job(html):
    title = html.find("a", {"class": "s-link"})["title"]
    company, location = [s.get_text(strip=True) for s in html.find("h3", {"class": "fc-black-700"}).find_all("span", recursive=False)]
    job_id = html['data-jobid']
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f'https://stackoverflow.com/jobs/{job_id}'
        }

def get_jobs(word):
    SO_URL = f"https://stackoverflow.com/jobs?q={word}"
    return extract_jobs(extract_pages(SO_URL), SO_URL)
