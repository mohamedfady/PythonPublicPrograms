# Proxy-Scraper-and-Checker

A Python script that scrapes various online sources for proxies and checks them to determine if they are good or bad proxies.

## Installation

1. Clone the repository or download the ZIP file.
2. Install the required packages using `pip install -r requirements.txt`
3. Run the script using `python proxy_checker.py`

## How It Works

1. The script first downloads a CSV file that contains links to various proxy lists.
2. It scrapes those proxy lists to extract a list of proxies.
3. The script then checks each proxy to determine if it is a good or bad proxy. A good proxy is defined as a proxy that can be connected to and that returns a valid IP address.
4. The script saves the good proxies to a CSV file and displays the total number of good proxies found for each type (HTTP, SOCKS4, and SOCKS5).

## Classes and Functions

### ProxyConnector

This class takes a single argument, a string that represents a proxy in the format `PROXYTYPE:IP:PORT`. It creates an instance of the class that has the following properties:

- `status`: A Boolean value that represents whether the proxy is a good proxy (`True`) or a bad proxy (`False`).
- `ip`: A string that represents the IP address of the proxy. If the proxy is a bad proxy or cannot be connected to, this value will be `'0.0.0.0'`.
- `p_type`: A string that represents the type of proxy (`HTTP`, `SOCKS4`, or `SOCKS5`).
- `p_host`: A string that represents the IP address of the proxy.
- `p_port`: An integer that represents the port number of the proxy.

This class has the following methods:

- `set_proxy(self,connection_func)`: This method takes a single argument, a function that attempts to connect to the proxy. If the connection is successful, this method sets the `status` and `ip` properties of the instance to `True` and the IP address of the proxy, respectively. If the connection is unsuccessful, this method sets the `status` property of the instance to `False`.
- `get_ip(self)`: This method attempts to connect to the proxy and retrieve the IP address of the proxy. If successful, it returns the IP address. If unsuccessful, it returns `False`.
- `connect_p(self,p_type)`: This method attempts to connect to the proxy using the specified proxy type. If successful, it returns `True`. If unsuccessful, it returns `False`.

### Functions

The script also contains the following functions:

- `save_text(pt,nm,tp,ln)`: This function saves a line of text to a CSV file with the specified path, name, and type (extension).
- `create_folder(new_dir_name)`: This function creates a new directory with the specified name.
- `get_main_websites()`: This function downloads the CSV file that contains links to various proxy lists and extracts the URLs and types of the proxy lists.
- `get_proxies_list(counter=0)`: This function scrapes the proxy lists to extract a list of proxies and adds them to a dictionary (`PROXIES_LIST`) that is keyed by proxy type (`HTTP`, `SOCKS4`, or `SOCKS5`).
- `check_single_proxy(proxy)`: This function takes a single argument, a string that represents a proxy in the format `PROXYTYPE:IP:PORT`. It creates an instance of the `ProxyConnector` class and checks whether the proxy is a good proxy or a bad
- `check_proxies_list()`: This function checks each proxy in the PROXIES_LIST dictionary and saves the good proxies to a CSV file.
- `main()`: This function is the entry point of the script. It initializes some global variables and executes the functions in the following order: create_folder(), get_main_websites(), get_proxies_list(), check_proxies_list(), and display_results().
###Usage
To use the script, simply run the proxy_checker.py file using python proxy_checker.py. The script will then download the proxy lists, check the proxies, and save the good proxies to a CSV file.

###Conclusion
This script is a useful tool for anyone who needs to scrape proxies and check them to determine if they are good or bad proxies. It uses a simple yet effective approach that can be easily customized to suit the user's needs.
