import os

from flask import Flask, request, render_template

from dotenv import load_dotenv, find_dotenv
from pythecamp import TheCampClient

app = Flask(__name__)

load_dotenv(find_dotenv(), encoding='utf-8')


def get_env_variable(var_name, default=None):
    try:
        return os.environ[var_name]

    except KeyError:
        if default is None:
            error_msg = '필수 환경 변수 {}가 설정되지 않았습니다.'.format(var_name)
            raise ValueError(error_msg)

        return default


def send_message(title: str, content: str) -> None:
    client = TheCampClient()
    email = get_env_variable('DONTCRY_EMAIL')
    pw = get_env_variable('DONTCRY_PW')
    client.login(email, pw)
    groups = client.get_group_list()
    trainees = client.get_trainee(groups[0]['group_id'])
    client.write_letter(
        title=title,
        content=content,
        unit_code=groups[0]['unit_code'],
        group_id=groups[0]['group_id'],
        name=trainees['trainee_name'],
        birth_date=trainees['birth'],
        relationship=trainees['relationship'])
    client.logout()


def chunk_and_send_message(title: str, content: str) -> None:
    content = content.replace('\r\n', '\n')
    content = content.replace('\r', '\n')
    content = content.replace('\n', '#')

    print('##############\n', content)

    if len(title) > 15:
        title = title[:15] + '..'

    for index, chunk in enumerate(range(0, len(content), 1600)):
        msg_chunked = content[chunk:chunk + 1600]
        msg_chunked = msg_chunked
        title_chunked = f'{title}({index + 1})'
        print(f'타이틀: {title_chunked}\n메세지: {msg_chunked}\n메세지를 전송합니다. {index}')

        # send_message(title_chunked, msg_chunked)


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        content = request.form['content']
        content = name + '\n' + content
        print(title)
        print(content)

        chunk_and_send_message(title, content)

        return render_template('success.html')

    return render_template('index.html')
