import os

from dotenv import load_dotenv, find_dotenv
from pythecamp import TheCampClient


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
