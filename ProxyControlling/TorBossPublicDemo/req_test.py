from httpx import Client
from rich import print
import threading
import random
import sys


def get_proxies():
    with open('socks5.txt', "r") as f:
        proxies = f.readlines()
        proxies = [proxy.strip() for proxy in proxies]
        return proxies


def main():
    proxies = get_proxies()
    proxy = random.choice(proxies).replace("\n", "")
    if proxy == "":
        return
    try:
        client = Client(proxies=proxy)
        response = client.get("http://ip-api.com/json")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(
                f"Request failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    ips = []
    while True:
        ip = main()
        if ip and ip not in ips:
            ips.append(ip)
            print(
                f'Unique IPs rotated: {len(ips)} | Last IP: {ip["query"]} || {ip["country"]}')
        threading.Timer(10, lambda: None).start()  # 10 second delay
