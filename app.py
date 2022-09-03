from flask import Flask, render_template, request
import cv2
import numpy as np
# from ISR.models import RDN, RRDN
from flask import send_file
import os
import glob
from analyse import *

percent = 10

app = Flask(__name__)


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test2.html')


@app.route('/analyse')
def analyse():
    form = ""
    if request.method == 'POST':
        form = request.form
        transcriptResult = request.form.getlist('ans')
        clockResult = request.form.getlist('time')
        print(transcriptResult, clockResult ,"here")
        print(form, "made a req")
    return render_template('analyse/analyse.html', form = form)

@app.route('/get_results', methods = ['GET','POST'])
def get_results():
    form = request.form
    transcriptResult = request.form.getlist('ans')[0]
    clockResult = int(request.form.getlist('time')[0])
    confidenceResult = request.form.getlist('confidence')[0]

    
    paceResult = pace(transcriptResult, clockResult)
    grammarResult = grammar_check(transcriptResult)
    vocab = get_common_words(transcriptResult)
    fillerList = get_filler(transcriptResult)
    bannedLen= banned_words(transcriptResult)
    fillerLen = len(fillerList)
    tone = get_sentiment(transcriptResult)
    print(tone, "tone")
    frequent = most_frequently_words(transcriptResult)
    synonyms = []
    for word in frequent:
        w = word[0]
        synonym = getsynonyms(w)

        synonyms.append(synonym)
        print(synonym, w)
    print(frequent, "fr")


    return render_template('analyse/analyse_results.html', fillerList = fillerList, synonyms = synonyms ,confidence = str(round(float(confidenceResult), 2)), paceResult = str(round(float(paceResult), 2)), grammarList =grammarResult, grammarLen =len(grammarResult), fillerLen = fillerLen, vocab =str(round(float(vocab), 2)),bannedLen = bannedLen, frequent = frequent ,names=['a','b','c','d','e'], score = round(((float(vocab)*20)+float(confidenceResult))/2, 2), sentiment = str(tone))





@app.route('/analyse_results')
def analyse_results():
    
    return render_template('analyse/analyse_results.html')









@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    
    app.run(debug=True)


