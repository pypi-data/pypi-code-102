import configparser
import enum
import json
import os
import requests
import types
import typing as tp
from pathlib import Path


CONFIG = types.SimpleNamespace(
    BIONLP_API_URL='https://bionlp.aws.science.io/v1',
    HELP_EMAIL="api-help@science.io",
    SETTINGS_DIR=Path.home() / ".scienceio",
    SETTINGS_FILE_PATH=Path.home() / ".scienceio" / "config",
)


class ScienceIOError(Exception):
    """Base class for all exceptions that are raised by the ScienceIO SDK."""


class TimeoutError(ScienceIOError):
    """Raised when a call to the ScienceIO API times out."""

    def __init__(self, msg):
        self.msg = msg


class ResponseFormat(str, enum.Enum):
    JSON = 'application/json'

    def format_response(self, response):
        if self is ResponseFormat.JSON:
            return response.json()
        else:
            raise NotImplementedError('Unknown response format')

    def create_headers(self, api_id: str, api_secret: str) -> tp.Dict:
        return {
            'Content-Type': self.value,
            'x-api-id': api_id,
            'x-api-secret': api_secret,
        }


class ScienceIO(object):
    def __init__(self,
                 response_format: ResponseFormat = ResponseFormat.JSON,
                 timeout: tp.Optional[tp.Union[int, float]] = 1200,
                 ):
        """Initializer for the ScienceIO client. The client will attempt to
        configure itself by trying to read from environment variables, if set.
        If unable to, the config values will be read from the ScienceIO config
        file.

        Args:
            email:
                The user's login/email address.
            response_format:
                Format to use for responses (default: `ResponseFormat.JSON`).
            timeout:
                Amount of time to wait before timing out network calls, in seconds.
                If `None`, timeouts will be disabled. (default: 1200)
        """

        self.response_format = response_format
        self.timeout = timeout

        # Create a persistent session across requests.
        # https://docs.python-requests.org/en/master/user/advanced/
        self.session = requests.Session()
        self.session.params = {}

        # Lazy loading of configuration (no need to try and load the settings
        # if the user specifies their own API ID and secret). Also, this
        # prevents breakage when in envs with no settings file, such as test
        # environments or hosted Jupyter notebooks.
        config = None

        def get_config_value(key: str) -> str:
            nonlocal config
            if config is None:
                config = configparser.RawConfigParser()
                config.read(CONFIG.SETTINGS_FILE_PATH)

            return config['SETTINGS'][key]

        # Handles config values from user arguments, config file, and user
        # input, in that order from most to least preferred.
        write_out_conf = False

        def get_value(initial: tp.Optional[str], key: str, human_name: str) -> str:
            nonlocal write_out_conf
            if initial is None:
                try:
                    return get_config_value(key)
                except KeyError:
                    user_input = str(input(f'Please provide your ScienceIO API key {human_name}: '))

                    # User input was collected, flag the config file for rewriting.
                    write_out_conf = True
                    return user_input

            return initial

        # API endpoints to use.
        self.bionlp_url = os.environ.get('SCIENCEIO_API_URL', CONFIG.BIONLP_API_URL)

        # API key and secret (with extra handling for env vars, config file, and user prompts).
        self.api_id = get_value(os.environ.get('SCIENCEIO_KEY_ID'), 'KEY_ID', 'id')
        self.api_secret = get_value(os.environ.get('SCIENCEIO_KEY_SECRET'), 'KEY_SECRET', 'secret')

        # Write out the API key ID and secret if either or both of those values
        # needed user input.
        if write_out_conf:
            # Create a new `ConfigParser` to hold the configuration we want to
            # write to the config file.
            new_conf = configparser.ConfigParser()
            new_conf['SETTINGS'] = {
                'KEY_ID': self.api_id,
                'KEY_SECRET': self.api_secret,
            }

            # Create the config directory (and any parents) if it does not
            # already exist.
            CONFIG.SETTINGS_DIR.mkdir(parents=True, exist_ok=True)

            # Write out the new config.
            with open(CONFIG.SETTINGS_FILE_PATH, 'w') as fp:
                new_conf.write(fp)

    def annotate(self, text: str) -> tp.Dict:
        """Annotates a block of text using the ScienceIO API.

        Args:
            text (str): The text to annotate.

        Raises:
            ValueError: Raised if the input text is not a `str`.
            TimeoutError: Raised if the annotation request exceeds the timeout
                limit.

        Returns:
            tp.Dict: The annotation data, as a Python dictionary.
        """
        if not isinstance(text, str):
            raise ValueError("annotate argument must be a string.")

        payload = json.dumps({
            "text": text,
        })

        # Headers for API key support.
        headers = self.response_format.create_headers(
            api_id=self.api_id,
            api_secret=self.api_secret,
        )
        target_url = f'{self.bionlp_url}/annotate'

        try:
            response = self.session.post(
                target_url,
                data=payload,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.Timeout:
            raise TimeoutError('annotation timed out, please try again') from None

        result = self.response_format.format_response(response)

        return result
