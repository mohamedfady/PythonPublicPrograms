from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import random


def get_proxies():
    with open('socks5.txt', "r") as f:
        proxies = f.readlines()
        proxies = [proxy.strip() for proxy in proxies if proxy.strip()]
        return proxies


class OwnBrowser:
    def __init__(self):
        self.proxies = get_proxies()
        self.proxy = random.choice(self.proxies)

        self.chrome_options = Options()
        self.chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--disable-translate")
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        self.chrome_options.add_argument(f'--proxy-server={self.proxy}')

        # Setting up Chrome driver
        self.driver = webdriver.Chrome(
            options=self.chrome_options)

    def open_site(self, site_url):
        self.driver.get(site_url)
        print(f"Opened {site_url}")

    def refresh_site(self):
        try:
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.refresh()
            print("Site refreshed")
        except Exception as e:
            print(f"Error refreshing site: {e}")

    def close_browser(self):
        self.driver.quit()
        print("Browser closed")

    def run(self, site_url):
        try:
            self.open_site(site_url)
            while True:
                self.refresh_site()
                sleep(20)
        except Exception as e:
            print(f"Error running browser: {e}")
        finally:
            self.close_browser()


if __name__ == "__main__":
    browser = OwnBrowser()
    browser.run("https://whoer.net")
