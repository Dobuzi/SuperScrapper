import requests
from bs4 import BeautifulSoup

def extract_pages(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    if soup is not None:
        pagination = soup.find("div",  {"class": "pagination"})
    else:
        return 0

    if pagination is not None:
        links = pagination.find_all('a')
    else:
        return 0
    pages = [int(link.string) for link in links[:-1]]
    return pages[-1]

def extract_jobs(last_page, URL, LIMIT):
    jobs = []
    if last_page == 0:
        print(f'Scrapping Indeed page 1')
        html = requests.get(f"{URL}&start=0")
        soup = BeautifulSoup(html.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            jobs.append(extract_job(result))
        return jobs

    for page in range(last_page):
        print(f'Scrapping Indeed page {page+1}')
        html = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(html.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            jobs.append(extract_job(result))
    return jobs

def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company_html = html.find("span", {"class": "company"})
    if company_html.string is not None:
        company_anchor = company_html.find("a")
        if company_anchor is not None:
            company = company_anchor.string.strip()
        else:
            company = company_html.string.strip()
    else:
        company = None
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f'https://kr.indeed.com/채용보기?jk={job_id}'
        }

def get_jobs(word):
    LIMIT = 50
    INDEED_URL = f"https://kr.indeed.com/jobs?q={word}&l=seoul&limit={LIMIT}"
    return extract_jobs(extract_pages(INDEED_URL), INDEED_URL, LIMIT)
