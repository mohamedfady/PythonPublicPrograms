# TorBoss (DEMO)

TorBoss is a powerful program that helps you to set up your own rotating proxies pool. It quickly and efficiently starts multiple instances of Tor SOCKS5 proxies, each rotating every few seconds as per your configuration.

## Features

- Start multiple Tor instances with unique configurations
- Rotate IP addresses every few seconds as per your preference
- Support for using proxies from specific countries
- Save the SOCKS5 proxies in a text file
- Efficiently manage Tor instances with thread pooling
- Respond to user commands to restart Tor instances
- Supports both IPv4 and IPv6

## Using Proxies

Once you have the SOCKS5 proxies saved in a text file, you can use them in any application that supports SOCKS5 proxies. The proxies will rotate their IP addresses based on the configured interval.



## Dependencies
TorBoss requires the following Python packages:

1. stem
2. requests
3. rich
4. concurrent.futures
Please make sure to install these packages before running the script.



## Installation
```
pip install rich
pip install requests
pip install futures
pip install stem
pip install PySocks
```

## Usage

This is an example of how to use TorBoss:

1. Run the script.
2. Answer the prompts to configure the number of SOCKS proxies, countries to use, rotation interval, and output file name.
3. The script will find available ports, start the Tor instances, and save the SOCKS5 proxies in the specified file.

