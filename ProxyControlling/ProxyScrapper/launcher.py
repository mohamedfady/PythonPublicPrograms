import threading, concurrent.futures, csv, requests, colorama, re, sys, socks, socket, pathlib, time, urllib3
from termcolor import colored as cld

FOLDER_PATH = str(pathlib.Path(__file__).parents[0])

class ProxyConnector:
    def __init__(self,_proxy):
        p_elements = _proxy.split(':')
        self.status = False
        self.ip = '0.0.0.0'
        if len(p_elements) == 3:
            self.p_type = p_elements[0]
            self.p_host = p_elements[1]
            self.p_port = int(re.compile(r"\d+").search(p_elements[2]).group())
            self.set_proxy(self.connect_p(self.p_type))
        else:
            print(cld(f'[USER_ERROR] : ({_proxy}) Invalid Proxy Format - Please Use Proxyformat as (PROXYTYPE:IP:PORT) or (PROXYTYPE:IP:PORT:USER:PASS )...','red'))

    def set_proxy(self,connection_func): 
        if connection_func == True:
            self.ip = self.get_ip() # check and return ip if proxy connected
            self.status = True
            return True
        else: return False
    
    def get_ip(self):
        try:
            ip = requests.get("https://api.ipify.org?format=json",timeout=10).json()['ip']
            return ip
        except : return False

        
    def connect_p(self,p_type):
        try: 
            if p_type == "HTTP":
                socks.set_default_proxy(socks.HTTP, self.p_host, int(self.p_port))
                socket.socket = socks.socksocket
                return True
            elif p_type == "SOCKS4":
                socks.set_default_proxy(socks.SOCKS4, self.p_host, int(self.p_port))
                socket.socket = socks.socksocket
                return True
            elif p_type == "SOCKS5":
                socks.set_default_proxy(socks.SOCKS5, self.p_host, int(self.p_port))
                socket.socket = socks.socksocket
                return True
            else:
                print(cld(f'[USER_ERROR] : Proxy Type Incorrect - Please Use Proxyformat as (PROXYTYPE:IP:PORT) or (PROXYTYPE:IP:PORT:USER:PASS) ...','red'))
                return False            
        except : return False


''' FUNCTIONS '''

def save_text(pt,nm,tp,ln):
    original_stdout = sys.stdout 
    with open(f'{FOLDER_PATH}\\{pt}\\{nm}.{tp}', 'a+',encoding='utf-8',errors='ignore') as fn:
        sys.stdout = fn 
        print(ln) 
        sys.stdout = original_stdout 
    return True

def create_folder(new_dir_name):
    return pathlib.Path(f'{FOLDER_PATH}\\{new_dir_name}').mkdir(parents=True, exist_ok=True)

def get_main_websites():
    # Download the CSV file
    response = requests.get(MAIN_SITES_URL)
    # Parse the CSV file
    reader = csv.DictReader(response.text.splitlines(), fieldnames=["PROXYLINK", "PROXYTYPE"])
    for row in reader:
        # do something with the row
        if row['PROXYTYPE'] == 'HTTP' or row['PROXYTYPE'] == 'SOCKS4' or row['PROXYTYPE'] == 'SOCKS5':
            # print(row)
            MAIN_SITES.append(row)
    return print(cld(f'[INFO] : ({len(MAIN_SITES)}) Proxy sources found.','green'))

def get_proxies_list(counter=0):
    global MAIN_SITES
    global ALL_PROXIES_COUNT

    proxy_regex = r'([0-9]+.[0-9]+.[0-9]+.[0-9]+:[0-9])'
    for item in MAIN_SITES:
        response = requests.get(str(item['PROXYLINK']))
        list = response.text.splitlines()
        counter+=1
        # print(counter, len(list))
        for proxy in list:
            if re.match(proxy_regex, proxy):
                p_elements = proxy.split(':')
                ALL_PROXIES_COUNT += 1
                host = p_elements[0]
                port = re.compile(r"\d+").search(p_elements[1]).group()
                

                PROXIES_LIST[item['PROXYTYPE']].append(f'{host}:{port}')
    return print(cld(f'[INFO] : All websites scrapped and ({ALL_PROXIES_COUNT}) proxy found.','green'))


            

def check_single_proxy(proxy):
    global HTTP_GOOD_COUNT
    global SOCKS4_GOOD_COUNT
    global SOCKS5_GOOD_COUNT
    global CH_COUNTER
    

    try:
        proxy_obj = ProxyConnector(proxy)
        CH_COUNTER +=1
        if proxy_obj.ip != '0.0.0.0' and proxy_obj.ip != False and proxy_obj.status == True:
            save_text(REZULT_FOLDER,'GOOD_PROXIES','csv',proxy)
            if proxy_obj.p_type == 'HTTP' :
                HTTP_GOOD_COUNT += 1
                save_text(REZULT_FOLDER,proxy_obj.p_type,'csv',proxy)
            elif proxy_obj.p_type == 'SOCKS4' :
                SOCKS4_GOOD_COUNT += 1
                save_text(REZULT_FOLDER,proxy_obj.p_type,'csv',proxy)
            elif proxy_obj.p_type == 'SOCKS5' :
                SOCKS5_GOOD_COUNT += 1
                save_text(REZULT_FOLDER,proxy_obj.p_type,'csv',proxy)

            return print(cld(f'\n[GOOD] ({CH_COUNTER}) : ({proxy}) || IP = ({proxy_obj.ip}).','green'))
        else:
            return print(cld(f'\n[BAD] ({CH_COUNTER}) : ({proxy}) || IP = ({proxy_obj.ip}).','red'))
    except Exception as e:
        print(cld(f'\n[ERROR] ({CH_COUNTER}) : ({proxy}) - {e}','red'))

def check_proxies_list():
    global FORMATTED_PROXYIES_LIST
    for each_p_type in PROXIES_LIST:
        for proxy in PROXIES_LIST[each_p_type]:
            proxy = f'{each_p_type}:{proxy}'
            FORMATTED_PROXYIES_LIST.append(proxy)
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        rezults = executor.map(check_single_proxy,set(FORMATTED_PROXYIES_LIST))
        for i in rezults:
            pass
    return print(cld(f'[INFO] : Finished.','yellow'))



if __name__ == '__main__':
    colorama.init()
    urllib3.disable_warnings()
    # Prepare proxies sources and counters
    MAIN_SITES_URL = 'https://gist.githubusercontent.com/hassan4u2/93fcd5d1a6314d6716455cd81e9c3f26/raw/e2b18ed4730f20ccd07f10f421b50156a780c896/const_proxy_sites.csv'
    CHECKING_WEBSITES = [
        ['https://google.com','Google']
        ]
    MAIN_SITES = []
    PROXIES_LIST = {
        'HTTP' : [], 
        'SOCKS4' : [], 
        'SOCKS5' : []
        }
    FORMATTED_PROXYIES_LIST = []
    ALL_PROXIES_COUNT = 0
    CHECKED_PROXIES_COUNTER = 0
    HTTP_GOOD_COUNT = 0
    SOCKS4_GOOD_COUNT = 0
    SOCKS5_GOOD_COUNT = 0
    CH_COUNTER = 0

    # STEP 0 
    REZULT_FOLDER = f'rezults_{time.time()}'.split('.')[0]
    create_folder(REZULT_FOLDER)
    # STEP 1
    print(cld(f'[DEBUG] : Getting Proxies Sources ....','yellow'))
    get_main_websites()
    # STEP 2
    print(cld(f'[DEBUG] : Cleaning Proxies ....','yellow'))
    get_proxies_list(counter=0)

    # Monitoring
    sys.stdout.write(' ===> HTTP/S: {} || SOCKS4: {} || SOCKS5: {}\n ===> CHECKED: {}/{}\r'.format(
                len(PROXIES_LIST['HTTP']),
                len(PROXIES_LIST['SOCKS4']), 
                len(PROXIES_LIST['SOCKS5']),
                CHECKED_PROXIES_COUNTER, 
                ALL_PROXIES_COUNT
                )
                )
    sys.stdout.flush()

    # STEP 3
    check_proxies_list()    

    # Monitoring
    sys.stdout.write(' ===> HTTP: {} || SOCKS4: {} || SOCKS5: {}\n ===> HTTP/S_G: {} || SOCKS4_G: {} || SOCKS5_G: {}\n ===> CHECKED: {}/{}\r'.format(
                len(PROXIES_LIST['HTTP']), 
                len(PROXIES_LIST['SOCKS4']), 
                len(PROXIES_LIST['SOCKS5']),
                HTTP_GOOD_COUNT, 
                SOCKS4_GOOD_COUNT, 
                SOCKS5_GOOD_COUNT, 
                CHECKED_PROXIES_COUNTER, 
                ALL_PROXIES_COUNT
                )
                )
    sys.stdout.flush()




    