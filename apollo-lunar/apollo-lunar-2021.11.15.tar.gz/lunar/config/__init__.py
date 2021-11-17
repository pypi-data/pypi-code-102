import requests

CONFIG = {
    "LOCAL": {
        "LOCAL": {
            "TEST_URL": "http://127.0.0.1:8080",
            "LUNAR_REC_URL": "http://127.0.0.1:8080",
            "LUNAR_DATA_URL": "http://127.0.0.1:8081",
        },
    },
    "DEV": {
        "LOCAL": {
            "TEST_URL": "https://rec.dev.apollo-lunar.com",
            "LUNAR_REC_URL": "https://rec.dev.apollo-lunar.com",
            "LUNAR_DATA_URL": "https://data.dev.apollo-lunar.com",
        },
        "LUNAR": {
            "TEST_URL": "https://2mqu0rhpsc-vpce-0ea0f0c470612df61.execute-api.ap-northeast-2.amazonaws.com",
            "LUNAR_REC_URL": "https://2mqu0rhpsc-vpce-0ea0f0c470612df61.execute-api.ap-northeast-2.amazonaws.com",
            "LUNAR_DATA_URL": "https://qu8pnrfq8c-vpce-0ea0f0c470612df61.execute-api.ap-northeast-2.amazonaws.com",
        },
    },
    "STG": {
        "EDD": {
            "TEST_URL": "http://150.6.13.63:8081",
            "LUNAR_REC_URL": "https://gm05du691j-vpce-0fa38c61f2c3a311b.execute-api.ap-northeast-2.amazonaws.com",
            "LUNAR_DATA_URL": "https://cp71v3ev9g-vpce-0fa38c61f2c3a311b.execute-api.ap-northeast-2.amazonaws.com",
            "COPY_DATABASE_URL": "http://150.6.13.9:31771/edd_to_lunar/copy_database",
            "COPY_FILES_URL": "http://150.6.13.9:31771/edd_to_lunar/copy_files",
            "JOB_STATUS_URL": "http://150.6.13.9:31771/edd_to_lunar/job_status",
        },
        "LOCAL": {
            "TEST_URL": "https://rec.stg.apollo-lunar.com",
            "LUNAR_REC_URL": "https://rec.stg.apollo-lunar.com",
            "LUNAR_DATA_URL": "https://data.stg.apollo-lunar.com",
        },
        "LUNAR": {
            "TEST_URL": "https://gm05du691j-vpce-0fa38c61f2c3a311b.execute-api.ap-northeast-2.amazonaws.com",
            "LUNAR_REC_URL": "https://gm05du691j-vpce-0fa38c61f2c3a311b.execute-api.ap-northeast-2.amazonaws.com",
            "LUNAR_DATA_URL": "https://cp71v3ev9g-vpce-0fa38c61f2c3a311b.execute-api.ap-northeast-2.amazonaws.com",
        },
    },
    "PRD": {
        "EDD": {
            "TEST_URL": "http://150.6.13.63:8081",
            "LUNAR_REC_URL": "https://6mxcp1mx6j-vpce-0831759639ca45cb4.execute-api.ap-northeast-2.amazonaws.com",
            "LUNAR_DATA_URL": "https://qrnczr2pc3-vpce-0831759639ca45cb4.execute-api.ap-northeast-2.amazonaws.com",
            "COPY_DATABASE_URL": "http://150.6.13.9:31771/edd_to_lunar/copy_database",
            "COPY_FILES_URL": "http://150.6.13.9:31771/edd_to_lunar/copy_files",
            "JOB_STATUS_URL": "http://150.6.13.9:31771/edd_to_lunar/job_status",
        },
        "LOCAL": {
            "TEST_URL": "https://rec.apollo-lunar.com",
            "LUNAR_REC_URL": "https://rec.apollo-lunar.com",
            "LUNAR_DATA_URL": "https://data.apollo-lunar.com",
        },
        "LUNAR": {
            "TEST_URL": "https://6mxcp1mx6j-vpce-0831759639ca45cb4.execute-api.ap-northeast-2.amazonaws.com",
            "LUNAR_REC_URL": "https://6mxcp1mx6j-vpce-0831759639ca45cb4.execute-api.ap-northeast-2.amazonaws.com",
            "LUNAR_DATA_URL": "https://qrnczr2pc3-vpce-0831759639ca45cb4.execute-api.ap-northeast-2.amazonaws.com",
        },
    },
}


class Config:
    def __init__(self, env: str, apikey: str):
        assert env in CONFIG.keys(), f"`env` must be in {CONFIG.keys()}"

        setattr(self, "ENV", env)
        setattr(self, "APIKEY", apikey)

        if env == "LOCAL":
            setattr(self, "RUNTIME_ENV", "LOCAL")
            for key, url in CONFIG[env]["LOCAL"].items():
                setattr(self, key, url)
            return

        for runtime_env, urls in CONFIG[env].items():
            try:
                requests.get(url=urls["TEST_URL"], timeout=0.1)
                setattr(self, "RUNTIME_ENV", runtime_env)
                for key, url in urls.items():
                    setattr(self, key, url)
                break
            except Exception:
                continue

        if not hasattr(self, "RUNTIME_ENV"):
            raise Exception(f"Lunar {env} does not support this runtime environment.")
