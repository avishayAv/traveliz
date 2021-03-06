from pathlib import Path


def choose_root(*paths):
    for path in paths:
        path = Path(path)
        if path.exists():
            return path


REPOSITORY_ROOT = choose_root(r'C:\Users\Y\PycharmProjects\traveliz', r'C:\Users\avishaya\PycharmProjects\traveliz',
                              '/home/runner/work/traveliz/traveliz/',r'C:\Users\rohi2\PycharmProjects\traveliz')
DRIVER_PATH = choose_root(REPOSITORY_ROOT / 'chromedriver.exe')
CHROME_PROFILE = choose_root(r'C:\Users\Y\AppData\Local\Google\Chrome\User Data\Default',
                             r'C:\Users\avishaya\AppData\Local\Google\Chrome\User Data\Default',
                             r'C:\Users\rohi2\AppData\Local\Google\Chrome\User Data\Default')

FACEBOOK_DATA_PATH = 'data/facebook/'
WHATSAPP_DATA_PATH = 'data/whatsapp/'
AIRBNB_DATA_PATH = 'data/airbnb/'