import csv
import os

def save_to_file(jobs, word):
    with open(f"files/{word}_jobs.csv", mode="w") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Company", "Location", "Link"])
        for job in jobs:
            writer.writerow(list(job.values()))
    
    return

def load_from_file():
    jobs = list()
    db = dict()
    for _, _, files in os.walk('files/'):
        for file in files:
            jobs = []
            with open(f'files/{file}', mode='r') as f:
                reader = csv.reader(f)
                i = 0
                for [title, company, location, link] in reader:
                    i += 1
                    if i == 1: continue
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "link": link
                    })
                db[file.split('_')[0]] = jobs

    return db