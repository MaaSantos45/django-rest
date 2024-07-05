import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_DIR = Path(__file__).resolve().parent.parent
CHROMEDRIVER_NAME = 'chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_DIR / 'bin' / CHROMEDRIVER_NAME


def make_browser(*args):
    chrome_options = webdriver.ChromeOptions()
    chrome_service = Service(executable_path=str(CHROMEDRIVER_PATH))

    if args:
        for arg in args:
            chrome_options.add_argument(arg)

    return webdriver.Chrome(service=chrome_service, options=chrome_options)
