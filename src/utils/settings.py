import os

from dotenv import load_dotenv

load_dotenv()

TARGET_URL = str(os.getenv("TARGET_URL"))
TARGET_USR = str(os.getenv("TARGET_USR"))
TARGET_PSW = str(os.getenv("TARGET_PSW"))
API_URL = str(os.getenv("API_URL"))

USERNAME = TARGET_USR.split("@")[0]
