import os

from flask import Flask, request, render_template

from dotenv import load_dotenv, find_dotenv
from pythecamp import TheCampClient

from letter import chunk_and_send_message

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        content = request.form['content']
        content = f'[{name}] {content}'

        chunk_and_send_message(title, content)

        return render_template('success.html')

    return render_template('index.html')
