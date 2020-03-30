from flask import Flask, request, render_template

from letter import chunk_and_send_message

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        content = request.form['content']
        content = f'[{name}] {content}'

        trainee_mgr_seq = request.form['trainee_mgr_seq']

        chunk_and_send_message(title, content, trainee_mgr_seq)

        return render_template('success.html')

    return render_template('index.html')
