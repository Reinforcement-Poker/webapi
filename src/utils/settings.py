from dotenv import dotenv_values

_config = dotenv_values(".env")

TARGET_URL = _config["TARGET_URL"]
TARGET_USR = _config["TARGET_USR"]
TARGET_PSW = _config["TARGET_PSW"]
API_URL = _config["API_URL"]

USERNAME = TARGET_USR.split("@")[0]
