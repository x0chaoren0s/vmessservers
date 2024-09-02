from urllib.parse import urlparse
import logging, socket
import requests
# from requests.adapters import HTTPAdapter
from lxml.etree import HTML
from forcediphttpsadapter.adapters import ForcedIPHTTPSAdapter
from playwright.sync_api import sync_playwright
from tqdm import tqdm

class Server_list_parser_base:
    name = 'Server_list_parser_base'

    def __init__(self,
                 server_list_url: str = None,
                 server_provider_url: str = None) -> None:
        # self.server_list_url = server_list_url[:-1] if server_list_url.endswith('/') \
        #                         else server_list_url
        self.server_list_url = server_list_url
        if server_provider_url:
            self.server_provider_url = server_provider_url[:-1] if server_provider_url.endswith('/') \
                else server_provider_url
        else:
            urlp = urlparse(server_list_url)
            self.server_provider_url = f'{urlp.scheme}://{urlp.netloc}'
        self.host = urlparse(self.server_list_url).netloc

        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.INFO)
        streamHandler.setFormatter(formatter)
        fileHandler = logging.FileHandler('parsing_log.txt', encoding='UTF-8')
        fileHandler.setLevel(logging.INFO)
        fileHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)
        logger.addHandler(fileHandler)
        self.logger = logger
        
        self.session = requests.Session()
        self.proxies = {
            'http': 'http://127.0.0.1:7602',
            'https': 'http://127.0.0.1:7602'
        }
        self.use_proxy = False

    def run(self) -> dict:
        '''包括init以外的初始化以及parse'''
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)

        
        if not self.use_proxy:
            self.ip = self.get_ip()

            # self.session.mount('http://', HTTPAdapter(max_retries=10))
            # self.session.mount('https://', HTTPAdapter(max_retries=10))
            self.session.mount(self.server_provider_url, ForcedIPHTTPSAdapter(
                                dest_ip=self.ip, # type the desired ip
                                max_retries=3))      
        

        self.headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
            }
            
        return self.parse()

    def parse(self) -> dict:
        self.logger.info(f'[{self.server_provider_url}], {self.server_list_url}')
        ''' 子类重载该方法：先执行本父类方法，再做子类自己的事 '''
    
    @staticmethod
    def check_server(host, port=22):
        # ref: https://cloud.tencent.com/developer/article/1570645
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((host,port))
            return True
        except socket.error as e:
            return False
        finally:
            sock.close()

    def get_ip(self) -> str:
        '''返回当前网站的可用ip，主要目的是用于绕过dns封锁'''
        url = f'https://ip.900cha.com/{self.host}.html'
        # html = HTML(self.session.get(url).text)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 Edg/124.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            # 添加更多默认请求头...
        }     
        with self.session.request('GET', url, headers=headers, proxies=None) as response:
            html = response.content.decode()
        html = HTML(html)
        ip = html.xpath('//h1/small/text()')[0].split('IP:')[1]
        # page = self.browser.new_page()
        # page.goto(url)
        # page.wait_for_load_state('load',timeout=0)
        # page.wait_for_selector(f'xpath=//h1/small')
        # ip = page.locator(f'xpath=//h1/small').inner_text().split('IP:')[1]
        # page.close()
        return ip

    def get_ip_bak(self) -> str:
        '''返回当前网站的可用ip，主要目的是用于绕过dns封锁'''
        page = self.browser.new_page()
        page.goto("https://tool.chinaz.com/speedworld/"+self.host)
        page.wait_for_load_state('load',timeout=0)
        # [page.wait_for_selector(f'xpath=//div[@class="row listw clearfix"][{row}]/div/div[@name="ip"]/a')
        #     for row in range(1,len(page.locator('xpath=//div[@class="row listw clearfix"]').all())+1)] # 保证所有监测点都加载好
        # ips = [e.get_attribute('title') for e in page.locator('xpath=//div[@name="ip"]/a').all()]
        # page.close()
        tested_ip = set()
        found_ip = False
        ip = ''
        for row in tqdm(range(1,len(page.locator('xpath=//div[@class="row listw clearfix"]').all())+1),desc=f'testing ip for {self.host}'):
        # for ip in tqdm(ips,desc=f'testing ip for {self.host}'):
            page.wait_for_selector(f'xpath=//div[@class="row listw clearfix"][{row}]/div/div[@name="ip"]/a')
            ip = page.locator(f'xpath=//div[@class="row listw clearfix"][{row}]/div/div[@name="ip"]/a').get_attribute('title')
            if ip in tested_ip:
                continue
            tested_ip.add(ip)
            test_session = requests.Session()
            test_session.mount(self.server_provider_url, ForcedIPHTTPSAdapter(dest_ip=ip,max_retries=3,))
            try:
                r = test_session.get(self.server_provider_url,timeout=2)
                if r.status_code==200:
                    self.logger.info(f'{self.host} - {ip}')
                    found_ip = True
            except:
                pass
            finally:
                test_session.close()
            if found_ip:
                break
        if found_ip:
            print(f'{self.host} - {ip}')
            return ip
        else:
            print(f'{self.host} - no valid ip')
            return socket.gethostbyname(self.host)





if __name__ == '__main__':
    # FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
    # logging.basicConfig(format=FORMAT)
    slp = Server_list_parser_base('https://sshocean.com/ssh7days/')
    slp.parse()