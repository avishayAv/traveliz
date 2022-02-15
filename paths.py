from pathlib import Path


def choose_root(*paths):
    for path in paths:
        path = Path(path)
        if path.exists():
            return path
    raise Warning('No appropriate root found.')


REPOSITORY_ROOT = choose_root(r'C:\Users\Y\PycharmProjects\traveliz', '/home/runner/work/traveliz/traveliz/')
DRIVER_PATH = choose_root(REPOSITORY_ROOT / 'chromedriver.exe')
CHROME_PROFILE = choose_root(r'C:\Users\Y\AppData\Local\Google\Chrome\User Data\Default')
