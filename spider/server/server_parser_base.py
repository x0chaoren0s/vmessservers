import time, requests, logging, random, string, json, base64, socket
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from forcediphttpsadapter.adapters import ForcedIPHTTPSAdapter
from playwright.sync_api import sync_playwright
# from lxml import etree
from typing import Tuple, Iterable
from tqdm import tqdm
from pathlib import Path
import os

import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)

from ..server_list.server_list_parser_base import Server_list_parser_base

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

class Server_parser_base:
    name = 'Server_parser_base'
    save_folder = Path(__file__).absolute().parent.parent.parent/'results'

    def __init__(self,
                 server_dict: dict = None,
                 server_list_parser: Server_list_parser_base = None,
                 interval_sec: int = 0,
                 use_selenium: bool = False,
                 change_session: bool = True,
                 ) -> None:
        '''
        server_dict 若为 None, 则使用 server_list_parser.parse()
        
        server_dict 格式: {url:{'host':.., 'port':.., 'region':..}}
        '''
        self.server_dict = server_dict
        self.server_list_parser = server_list_parser
        self.interval_sec = interval_sec
                      
        self.use_selenium = use_selenium
        self.change_session = change_session      
            
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

        # self.yesCaptcha_clientKey = os.environ.get('API_KEY', 'empty') # clientKey：在个人中心获取
        self.yesCaptcha_clientKey = "ddd1cf72d9955a0e8ca7d05597fea5eb1dce33de5331"


    def run(self) -> dict:
        '''包括init以外的初始化以及parse'''

        if self.server_dict is None:
            self.server_dict = self.server_list_parser.run()
            self.browser = self.server_list_parser.browser
            self.host = self.server_list_parser.host
            self.server_provider_url = 'https://'+self.host
            self.ip   = self.get_ip(self.host)
        else:
            playwright = sync_playwright().start() # 其实没关
            self.browser = playwright.chromium.launch(headless=False)
            self.host = urlparse(list(self.server_dict.keys())[0]).netloc
            self.server_provider_url = 'https://'+self.host
            self.ip   = self.get_ip(self.host)
        

        self.logger.info(f'num of servers: {len(self.server_dict)}')

        self.session = self.new_session()
        self.session.mount(self.server_provider_url, ForcedIPHTTPSAdapter(
                            dest_ip=self.ip, # type the desired ip
                            max_retries=3))
        self.headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            }
        return self.parse()


    def parse(self, save=True, init_index=0) -> dict:
        if self.use_selenium:
            return self.parse_by_selenium(save, init_index)
        else:
            return self.parse_by_requests(save, init_index)

    def parse_by_requests(self, save=True, init_index=0) -> dict:
        ret = self.server_dict.copy()
        registered_hosts = set()
        for i, url in tqdm(enumerate(self.server_dict.keys()), desc=f'{self.name} parsing servers(tot{len(self.server_dict)}): '):
            if 'host' in self.server_dict[url]:
                if self.server_dict[url]['host'] in registered_hosts:
                    self.logger.warn(f"already registered: {self.server_dict[url]['host']}")
                    ret[url]['error_info'] = "already registered"
                    continue
            if self.change_session:
                self.session = self.new_session()
            self.headers['Referer'] = self.server_dict[url]['Referer']
            if i<init_index:
                continue
            self.logger.info(url)
            if i>0:
                time.sleep(self.interval_sec)
            try:
                res = self.session.get(url, headers=self.headers, allow_redirects=False, timeout=3)
            except:
                ret[url]['error_info'] = 'get timeout'
                self.logger.error(f"{ret[url]['region']}, {url} , {ret[url]['error_info']}")
                continue
            if res.status_code not in [200]:
                ret[url]['error_info'] = f'status_code: {res.status_code}'
                self.logger.error(f"{ret[url]['region']}, {url} , {ret[url]['error_info']}")
                continue
            post_url, form_data = self.filling_form(res)
            if 'error_info' in form_data:
                ret[url]['error_info'] = form_data['error_info']
                self.logger.error(f"{ret[url]['region']}, {url} , {ret[url]['error_info']}")
                continue
            self.headers['Referer'] = res.url
            try:
                res = self.session.post(post_url, data=form_data, headers=self.headers, allow_redirects=False, timeout=60)
                res = self.post_redirect(res)
            except:
                ret[url]['error_info'] = 'post timeout'
                self.logger.error(f"{ret[url]['region']}, {url} , {ret[url]['error_info']}")
                continue
            info_dict = self.after_filling_form(res) # keys: user, pass, host, [ip], port, config
            ret[url].update(info_dict)
            if 'error_info' in ret[url]:
                self.logger.error(f"{ret[url]['region']}, {url} , {ret[url]['error_info']}")
            else:
                ret[url]['config'] = self.adjust_config(ret[url], ret[url]['region'])
                ret[url]['date_span'] = f"{ret[url]['date_create']} - {ret[url]['date_expire']}"
                self.logger.info(f"{ret[url]['region']}, {ret[url]['config']}")
                # print(ret[url])
            registered_hosts.add(ret[url]['host'])

        num_tried = len(ret)
        num_succeed = len([v for v in list(ret.values()) if 'error_info' not in v])
        self.logger.info(f'finished. succeed: {num_succeed} / {num_tried}')
        if save:
            json_file = self.save_folder/f'{self.name}.json'
            with open(json_file, 'w') as fout:
                json.dump(ret, fout, indent=4)
            config_file = self.save_folder/f'{self.name}.conf'
            with open(config_file, 'w') as fout:
                if num_succeed>0:
                    data_span_printed = False
                    for server_info in ret.values():
                        if 'error_info' in server_info:
                            continue
                        if not data_span_printed:
                            print(f"# {server_info['date_span']}", file=fout)
                            data_span_printed = True
                        if 'config' in server_info:
                            print(server_info['config'], file=fout)
                else:
                    print(self.null_config(), file=fout)
        return ret
    def post_redirect(self, res_before) -> requests.Response:
        return res_before

    def parse_by_selenium(self, save=True, init_index=0) -> dict:
        ret = self.server_dict.copy()
        for i, url in tqdm(enumerate(self.server_dict.keys()), desc=f'{self.name} parsing servers: '):
            if i<init_index:
                continue
            self.logger.info(url)
            if i>0:
                time.sleep(self.interval_sec)
            options = Options() # 定义一个option对象
            options.add_argument("headless")
            driver = webdriver.Edge(options = options)  # Edge浏览器无头模式
            try:
                driver.get(url)
                info_dict = self.filling_form_via_selenium(driver) # keys: user, pass, host, [ip], port, config
                driver.close()
            except:
                info_dict = dict()
                info_dict['error_info'] = 'net::ERR_CONNECTION_TIMED_OUT'
            ret[url].update(info_dict)
            if 'error_info' in ret[url]:
                self.logger.error(f"{ret[url]['region']}, {url} , {ret[url]['error_info']}")
            else:
                ret[url]['config'] = self.adjust_config(ret[url], ret[url]['region'])
                ret[url]['date_span'] = f"{ret[url]['date_create']} - {ret[url]['date_expire']}"
                self.logger.info(f"{ret[url]['region']}, {ret[url]['config']}")
                
        num_tried = len(ret)
        num_succeed = len([v for v in list(ret.values()) if 'error_info' not in v])
        self.logger.info(f'finished. succeed: {num_succeed} / {num_tried}')
        if save:
            json_file = self.save_folder/f'{self.name}.json'
            with open(json_file, 'w') as fout:
                json.dump(ret, fout, indent=4)
            config_file = self.save_folder/f'{self.name}.conf'
            with open(config_file, 'w') as fout:
                if num_succeed>0:
                    data_span_printed = False
                    for server_info in ret.values():
                        if 'error_info' in server_info:
                            continue
                        if not data_span_printed:
                            print(f"# {server_info['date_span']}", file=fout)
                            data_span_printed = True
                        if 'config' in server_info:
                            print(server_info['config'], file=fout)
                else:
                    print(self.null_config(), file=fout)
        return ret

    def filling_form(self, res) -> Tuple[str, dict]:
        raise Exception('未实现 filling_form 方法')
    
    def after_filling_form(self, res) -> dict:
        ''' keys: user, pass, host, [ip], port, config '''
        raise Exception('未实现 after_filling_form 方法')
    
    def filling_form_via_selenium(self, driver_in_form_page) -> dict:
        ''' keys: config, date_create, date_expire '''
        raise Exception('未实现 filling_form_via_selenium 方法')


    def solve_recaptcha_v2(self, websiteURL: str, websiteKey: str) -> str:
        sleep_sec = 4 # 循环请求识别结果，sleep_sec 秒请求一次
        max_sec = 180  # 最多等待 max_sec 秒
        clientKey = self.yesCaptcha_clientKey # clientKey：在个人中心获取

        # 第一步，创建验证码任务 
        self.logger.info(f'getting yescaptcha taskID for recaptcha_v2...')
        url = "https://cn.yescaptcha.com/createTask"
        data = {
            "clientKey": clientKey,
            "task": {
                "websiteURL": websiteURL,
                "websiteKey": websiteKey,
                "type": "NoCaptchaTaskProxyless"
            }
        }
        try:
            # 发送JSON格式的数据
            res_dict = self.session.post(url, json=data, timeout=60).json()
            taskID = res_dict.get('taskId')
            self.logger.info(f'yescaptcha taskID for recaptcha_v2: {taskID}')
            if taskID is None:
                self.logger.error(res_dict)
                return 'solve failed. failed to get taskID.'
            
        except Exception as e:
            self.logger.error(e)
            return 'solve failed.'

        # 第二步：使用taskId获取response 
        self.logger.info(f'getting yescaptcha result for recaptcha_v2...')
        sec = 0
        while sec < max_sec:
            try:
                url = f"https://cn.yescaptcha.com/getTaskResult"
                data = {
                    "clientKey": clientKey,
                    "taskId": taskID
                }
            
                result = self.session.post(url, json=data, timeout=60).json()
                solution = result.get('solution', {})
                if solution:
                    gRecaptchaResponse = solution.get('gRecaptchaResponse')
                    if gRecaptchaResponse:
                        return gRecaptchaResponse
            except Exception as e:
                self.logger.error(e)
                return 'solve failed.'

            sec += sleep_sec
            self.logger.info(f'spent {sec}s in getting...')
            time.sleep(sleep_sec)
    
    def solve_hcaptcha(self, websiteURL: str, websiteKey: str) -> str:
        sleep_sec = 4 # 循环请求识别结果，sleep_sec 秒请求一次
        max_sec = 180  # 最多等待 max_sec 秒
        clientKey = self.yesCaptcha_clientKey

        # 第一步，创建验证码任务 
        self.logger.info(f'getting yescaptcha taskID for hcaptcha...')
        url = "https://china.yescaptcha.com/createTask"
        url = "https://cn.yescaptcha.com/createTask"
        data = {
            "clientKey": clientKey,
            "task": {
                "websiteURL": websiteURL,
                "websiteKey": websiteKey,
                "type": "HCaptchaTaskProxyless"
            }
        }
        try:
            # 发送JSON格式的数据
            res_dict = self.session.post(url, json=data, timeout=60).json()
            taskID = res_dict.get('taskId')
            self.logger.info(f'yescaptcha taskID for recaptcha_v2: {taskID}')
            if taskID is None:
                self.logger.error(res_dict)
                return 'solve failed. failed to get taskID.'
            
        except Exception as e:
            self.logger.error(e)
            return 'solve failed.'

        # 第二步：使用taskId获取response 
        self.logger.info(f'getting yescaptcha result for hcaptcha...')
        sec = 0
        while sec < max_sec:
            try:
                url = f"https://china.yescaptcha.com/getTaskResult"
                url = f"https://cn.yescaptcha.com/getTaskResult"
                data = {
                    "clientKey": clientKey,
                    "taskId": taskID
                }
            
                result = self.session.post(url, json=data, timeout=60).json()
                solution = result.get('solution', {})
                if solution:
                    gRecaptchaResponse = solution.get('gRecaptchaResponse')
                    if gRecaptchaResponse:
                        return gRecaptchaResponse
            except Exception as e:
                self.logger.error(e)
                return 'solve failed.'

            sec += sleep_sec
            self.logger.info(f'spent {sec}s in getting...')
            time.sleep(sleep_sec)
    
    def solve_turnstile(self, websiteURL: str, websiteKey: str) -> str:
        '''cloudflare的真人确认，人类通过只需要点击“确认您是真人”无需答题'''
        sleep_sec = 4 # 循环请求识别结果，sleep_sec 秒请求一次
        max_sec = 180  # 最多等待 max_sec 秒
        clientKey = self.yesCaptcha_clientKey

        # 第一步，创建验证码任务 
        self.logger.info(f'getting yescaptcha taskID for turnstile...')
        url = "https://china.yescaptcha.com/createTask"
        url = "https://cn.yescaptcha.com/createTask"
        data = {
            "clientKey": clientKey,
            "task": {
                "websiteURL": websiteURL,
                "websiteKey": websiteKey,
                "type": "TurnstileTaskProxyless"
            }
        }
        try:
            # 发送JSON格式的数据
            res_dict = self.session.post(url, json=data, timeout=60).json()
            taskID = res_dict.get('taskId')
            self.logger.info(f'yescaptcha taskID for turnstile: {taskID}')
            if taskID is None:
                self.logger.error(res_dict)
                return 'solve failed. failed to get taskID.'
            
        except Exception as e:
            self.logger.error(e)
            return 'solve failed.'

        # 第二步：使用taskId获取response 
        self.logger.info(f'getting yescaptcha result for turnstile...')
        sec = 0
        while sec < max_sec:
            try:
                url = f"https://china.yescaptcha.com/getTaskResult"
                url = f"https://cn.yescaptcha.com/getTaskResult"
                data = {
                    "clientKey": clientKey,
                    "taskId": taskID
                }
            
                result = self.session.post(url, json=data, timeout=60).json()
                solution = result.get('solution', {})
                if solution:
                    token = solution.get('token')
                    # userAgent = solution.get('userAgent')
                    if token:
                        # return token, userAgent
                        return token
            except Exception as e:
                self.logger.error(e)
                return 'solve failed.'

            sec += sleep_sec
            self.logger.info(f'spent {sec}s in getting...')
            time.sleep(sleep_sec)

    def new_session(self) -> requests.Session:
        ''' 每创建一个账号都使用新 session 可直接绕过网站设置的创建账户时间间隔限制 '''
        new_session = requests.Session()
        new_session.mount('http://', HTTPAdapter(max_retries=10))
        new_session.mount('https://', HTTPAdapter(max_retries=10))
        if 'session' in dir(self) and self.session is not None:
            new_session.adapters = self.session.adapters.copy()
            # self.session.adapters = OrderedDict()
            self.session.close()
            del self.session
        return new_session

    def adjust_config(self, server_info: dict, region='', host='cn.bing.com', sni='cn.bing.com') -> str:
        config = server_info['config']
        try:
            ret = ''
            if server_info.get('type', 'vmess')=='vmess':
                config_dict = json.loads(base64.b64decode(config.split('vmess://')[1]).decode())
                if 'ip' in server_info and server_info.get('use_ip', True):
                    # config = self.config_using_ip(config, server_info['ip'])
                    config_dict['add'] = server_info['ip']
                if 'ip' not in server_info:
                    ip = self.get_ip(server_info['host'])
                    config_dict['add'] = ip
                if 'cloudflare_host' in server_info and server_info.get('use_cloudflare', False):
                    # config = self.config_using_ip(config, server_info['ip'])
                    config_dict['add'] = server_info['cloudflare_host']
                if 'uuid' in server_info and server_info.get('use_uuid', False):
                    config_dict['id'] = server_info['uuid']
                config_dict['ps'] = f"{server_info['date_expire']} {self.name}: {server_info['region']}"
                if server_info.get('change_host', True):
                    config_dict['host'] = host
                if server_info.get('change_sni', True):
                    config_dict['sni'] = sni
                ret = 'vmess://'+base64.b64encode(json.dumps(config_dict).encode()).decode()
            elif server_info.get('type', 'vmess')=='vless':
                # ntls: vless://66726565-7670-4e2e-b573-2d6e6e656e6e@hkc-s89.v2sv.xyz:80?   # 此处add是真实add
                #               uuid@add:port?
                #           encryption=none&
                #           security=none&
                #           type=ws&
                #           host=hkc-s89.v2sv.xyz&      # 很离谱，同一个提供商的连接有时候要用ip，有时候要用host
                #           path=%2Ffreevpn%2Ffreevpn.us-nnennenne%2FHK
                #           #%5BHK%5D freevpn.us-nnennenne
                                #ps
                # tls:  vless://66726565-7670-4e2e-b573-2d6e6e656e6e@cn.bing.com:443?       # 此处add是错误的（提供商就填错了）要改成真实add
                #           encryption=none&
                #           security=tls&
                #           sni=hkc-s89.v2sv.xyz&
                #           fp=randomized&
                #           type=ws&
                #           host=hkc-s89.v2sv.xyz&
                #           path=%2Ffreevpn%2Ffreevpn.us-nnennenne%2FHK
                #           #%5BHK%5D freevpn.us-nnennenne
                ps = f"{server_info['date_expire']} {self.name}: {region}"
                sep1 = config.split('@')[0]
                # sep2 = config.split('@')[1].split('?')[0]
                sep3 = config.split('?')[1].split('#')[0]
                # sep4 = config.split('#')[1]
                ret = f"{sep1}@{server_info['host']}:{server_info['port']}?{sep3}#{ps}"
        except Exception as e:
            self.logger.error(e)
            self.logger.error(server_info)
        finally:
            return ret

    @staticmethod
    def null_config() -> str:
        '''
        返回一个无效的用于提示的空config。可用于避免生产的config文件为空文件
        '''
        config_dict = {
            "v": "2",
            "ps": f"{Server_parser_base.normalized_local_date()} null config",
            "add": "127.0.0.1",
            "port": "80",
            "id": "84b5956b-530d-4955-8bf6-061ed1cc3850",
            "aid": "0",
            "scy": "auto",
            "net": "ws",
            "type": "none",
            "host": "127.0.0.1",
            "path": "/vmess",
            "tls": "none",
            "sni": "127.0.0.1",
            "alpn": ""
        }
        return 'vmess://'+base64.b64encode(json.dumps(config_dict).encode()).decode()

    @staticmethod
    def config_using_ip(config_using_host, ip) -> str:
        config_dict = json.loads(base64.b64decode(config_using_host.split('vmess://')[1]).decode())
        config_dict['add'] = ip
        return 'vmess://'+base64.b64encode(json.dumps(config_dict).encode()).decode()


    @staticmethod
    def getRandStr(strLen = -1) -> str:
        ''' strLen：随机字符串的长度，默认为 -1，代表闭区间 [4,12] 内的随机长度 '''
        if strLen == -1:
            strLen = random.randint(4,12)
        l = []
        #sample = '0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()-+=.'
        sample = random.sample(string.ascii_letters + string.digits, 62)## 从a-zA-Z0-9生成指定数量的随机字符： list类型
        # sample = sample + list('!@#$%^&*()-+=.')#原基础上加入一些符号元素
        for i in range(strLen):
            char = random.choice(sample)#从sample中选择一个字符
            l.append(char)
        return ''.join(l)#返回字符串
    
    @staticmethod
    def normalize_date(datestr: str, date_pattern: 'str | Iterable[str]', normalizing_pattern: str="%Y-%m-%d") -> str:
        """
        #### 可将网站给的时间日期格式转换成本项目采用的标准日期格式 "%Y-%m-%d"
        如把 ' 17-07-2022' 标准化成 '2022-07-17'

        %a Locale’s abbreviated weekday name.

        %A Locale’s full weekday name.

        %b Locale’s abbreviated month name.

        %B Locale’s full month name.

        %c Locale’s appropriate date and time representation.

        %d Day of the month as a decimal number [01,31].

        %H Hour (24-hour clock) as a decimal number [00,23].

        %I Hour (12-hour clock) as a decimal number [01,12].

        %j Day of the year as a decimal number [001,366].

        %m Month as a decimal number [01,12].

        %M Minute as a decimal number [00,59].

        %p Locale’s equivalent of either AM or PM.

        %S Second as a decimal number [00,61].

        %U Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0.

        %w Weekday as a decimal number [0(Sunday),6].

        %W Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0.

        %x Locale’s appropriate date representation.

        %X Locale’s appropriate time representation.

        %y Year without century as a decimal number [00,99].

        %Y Year with century as a decimal number.

        %z Time zone offset indicating a positive or negative time difference from UTC/GMT of the form +HHMM or -HHMM, where H represents decimal hour digits and M represents decimal minute digits [-23:59, +23:59]. 1

        %Z Time zone name (no characters if no time zone exists). Deprecated. 1

        %% A literal '%' character.
        """
        for pattern in [date_pattern] if isinstance(date_pattern, str) else date_pattern:
            try:
                return time.strftime(normalizing_pattern, time.strptime(datestr,pattern))
            except:
                pass
        raise ValueError(f"time data '{datestr}' does not match any format in {[date_pattern] if isinstance(date_pattern, str) else date_pattern}")

    @staticmethod
    def normalized_local_date() -> str:
        '''
        #### 输出标准化的当前日期，如 '2022-07-28'
        可用于不显示账户的注册时间的网站，所以自己填。但其实不太准确，因为不知道网站的显示的到期时间是用什么时区
        '''
        return time.strftime("%Y-%m-%d",time.localtime())

    def get_ip(self, hostname) -> str:
        '''目标网站的可用ip，主要目的是用于绕过dns封锁'''
        # page = self.browser.new_page()
        # page.goto("https://tool.chinaz.com/speedworld/"+hostname)
        # page.wait_for_load_state('load')
        # ips = [e.get_attribute('title') for e in page.locator('xpath=//div[@name="ip"]/a').all()]
        # page.close()
        # for ip in ips:
        #     test_session = requests.Session()
        #     test_session.mount(self.server_provider_url, ForcedIPHTTPSAdapter(dest_ip=ip,max_retries=3))
        #     try:
        #         r = test_session.get(self.server_provider_url)
        #         if r.status_code==200:
        #             return ip
        #     except:
        #         continue
        # return socket.gethostbyname(hostname)
        return self.server_list_parser.get_ip()

if __name__ == '__main__':
    spb = Server_parser_base()
    print(spb.normalize_date('6 Apr 2023', '%d %b %Y'))