from flask import Flask, render_template, request, redirect, send_file
from so import get_jobs as so_get_jobs
from indeed import get_jobs as indeed_get_jobs
from save import save_to_file, load_from_file

app = Flask("SuperScrapper")

db = load_from_file()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        if not db.get(word): db[word] = so_get_jobs(word) + indeed_get_jobs(word)
        jobs = db[word]
    else:
        return redirect("/")
    return render_template("report.html", resultsNumber=len(jobs), searchingBy=word, jobs=jobs)

@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs, word)
        return send_file(f'files/{word}_jobs.csv')
    except:
        return redirect("/")

app.run(host="0.0.0.0")
