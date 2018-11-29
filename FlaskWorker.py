from flask import Flask, render_template, request
import MainWorker

app = Flask(__name__)

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/search')
def SearchPage():
    jobType = request.args['jobType']
    location = request.args['location']
    job_pages = MainWorker.Scraper(jobType, location)
    frequency_list = MainWorker.LanguageProcessor(job_pages)
    return render_template('search.html',
        frequency_list = frequency_list
    )

if __name__ == '__main__':
    app.run()
