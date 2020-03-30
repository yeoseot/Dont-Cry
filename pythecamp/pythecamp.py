import json
import logging

import requests

logger = logging.getLogger('pythecamp')


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/76.0.3809.132 Safari/537.36"
    })
    session.hooks = {
        'response': [
            lambda r, *args, **kwargs: print(f'RESPONSE {r.status_code} {r.text}'),
            lambda r, *args, **kwargs: r.raise_for_status(),
        ]
    }

    return session


class TheCampRequestError(Exception):
    pass


class TheCampClient:
    API_HOST = 'https://www.thecamp.or.kr'

    def __init__(self):
        self.session = build_session()

    def _request(self, endpoint: str, data: dict) -> dict:
        res = self.session.post(f'{self.API_HOST}{endpoint}', json=data)

        if res.json()['resultCode'] != 200:
            raise TheCampRequestError(f'TheCamp 응답 코드가 예상 응답 코드와 다릅니다. {res.text}')

        return res.json()

    def login(self, email: str, password: str) -> None:
        print(f'로그인을 시도합니다. email: {email}')
        self._request('/login/loginA.do', {
            'state': 'email-login',
            'autoLoginYn': 'N',
            'userId': email,
            'userPwd': password,
        })
        print('로그인에 성공하였습니다.')

    def write_letter(
        self,
        title: str,
        content: str,
        trainee_mgr_seq: str,
    ) -> None:

        print(f'편지를 씁니다.')
        self._request('/consolLetter/insertConsolLetterA.do', {
            'boardDiv': 'sympathyLetter',
            'tempSaveYn': 'N',
            'traineeMgrSeq': trainee_mgr_seq,
            'sympathyLetterSubject': title,
            'sympathyLetterContent': content,
        })
        print('편지 쓰기 완료!')

    def logout(self) -> None:
        print('로그아웃을 시도합니다.')
        self.session.get(f'{self.API_HOST}/logout.do', allow_redirects=False)
        print('로그아웃 성공!')
