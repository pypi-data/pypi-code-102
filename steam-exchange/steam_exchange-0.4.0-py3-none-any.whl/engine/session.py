import json


class Session:
    @staticmethod
    def load_from_file(filename: str):
        with open(filename, "r") as f:
            jobj = json.load(f)
        return Session(**jobj)

    def __init__(
        self, session_id, client_session_id, steam_login, steam_login_secure
    ):
        self._session_id = session_id
        self._client_session_id = client_session_id
        self._steam_login = steam_login
        self._steam_login_secure = steam_login_secure

    @property
    def session_id(self):
        return self._session_id

    @property
    def client_session_id(self):
        return self._client_session_id

    @property
    def steam_login(self):
        return self._steam_login

    @property
    def steam_login_secure(self):
        return self._steam_login_secure

    def build_cookie(self):
        return "; ".join(
            [
                f"{key}:{value}"
                for key, value in {
                    "sessionid": self.session_id,
                    "clientsessionid": self.client_session_id,
                    "steamLogin": self.steam_login,
                    "steamLoginSecure": self.steam_login_secure,
                }.items()
            ]
        )
