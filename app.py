import os
import requests
import zlib
import zipfile
import nltk
import re

from newspaper import Article
from newspaper import Config
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from transformers import pipeline
from gensim.utils import deaccent
from collections import Counter

from bertinfer import *
from utility import *

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
#Load the model
bt = bertInference()
summarizer = pipeline("summarization")

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

proximityLevelDic = {
    "Competitors in other markets":1,
    "Prospects":1,
    "Potential partners":1,
    "State/Federal Regulations":2,
    "Common Law":2,
    "International Treaties":2,
    "Channel Partners":3,
    "Competitors":3,
    "Investors":3
}

def info(proximityLevel, severityLevel):
    if proximityLevel == 1:
        if severityLevel == 'Severity level 1':
            return "Risk_level_1"
        if severityLevel == 'Severity level 2':
            return "Risk_level_2"
        if severityLevel == 'Severity level 3':
            return "Risk_level_2"
    if proximityLevel == 2:
        if severityLevel == 'Severity level 1':
            return "Risk_level_2"
        if severityLevel == 'Severity level 2':
            return "Risk_level_2"
        if severityLevel == 'Severity level 3':
            return "Risk_level_3"
    if proximityLevel == 3:
        if severityLevel == 'Severity level 1':
            return "Risk_level_2"
        if severityLevel == 'Severity level 2':
            return "Risk_level_3"
        if severityLevel == 'Severity level 3':
            return "Risk_level_3"
    if proximityLevel == 4:
        if severityLevel == 'Severity level 1':
            return "Risk_level_3"
        if severityLevel == 'Severity level 2':
            return "Risk_level_3"
        if severityLevel == 'Severity level 3':
            return "Risk_level_4"
    if proximityLevel == 5:
        if severityLevel == 'Severity level 1':
            return "Risk_level_3"
        if severityLevel == 'Severity level 2':
            return "Risk_level_4"
        if severityLevel == 'Severity level 3':
            return "Risk_level_4"

@app.route('/', methods=['GET', 'POST'])
def index():
    dangerLevel = ''
    nextCompany = ''
    with open("companyName.txt") as fp1: 
        companyName = fp1.read() 

    companyName = companyName.split("\n")
    if request.method == 'POST':
        try:
            companyName = request.form.get('companyName')  # access the data inside 
            proximityLevel = request.form.get('proximityLevel')
            proximityLevel = proximityLevelDic[proximityLevel]
            articleLink = request.form.get('articleLink')
            article = extract_article(articleLink)
            summarizerText = summarizer(article, do_sample=False)[0]
            summary = summarizerText['summary_text']
            businessClass = bt(summary)
            
            article = article.split()
            article = clean_text(article)
            dangerLevel = info(int(proximityLevel), businessClass)
            for word in article:
                if word == companyName:
                    print("Company Name present in the article",companyName)
            
        except Exception as ex:
            print(ex)
    
    return render_template('index.html', message = dangerLevel)

def extract_article(link):
    article = Article(url)
    article.download()
    article.html
    article.parse()
    return article.text

def clean_text(word):
    word = clean_contractions(word)
    word = to_lower(word)
    return word

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)