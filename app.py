import os
import requests
import zlib
import zipfile
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from bertinfer import *

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
#Load the model
bt = bertInference()



@app.route('/', methods=['GET', 'POST'])
def index():
    businessClass = ''
    if request.method == 'POST':
        try:
            companyName = request.form.get('companyName')  # access the data inside 
            severityLevel = request.form.get('severityLevel')
            summary = request.form.get('summary')
            businessClass = bt(summary)

        except Exception as ex:
            print(ex)
    
    return render_template('index.html', message = businessClass)


if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)