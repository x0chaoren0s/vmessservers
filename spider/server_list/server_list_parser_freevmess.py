import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)

from .server_list_parser_base import Server_list_parser_base

from lxml import etree
from tqdm import tqdm

class Server_list_parser_freevmess(Server_list_parser_base):
    name = 'vmess_list_freevmess'

    def __init__(self, server_list_url: str = 'https://www.freevmess.com/server-v2ray',
                 server_provider_url: str = None) -> None:
        super().__init__(server_list_url, server_provider_url)

    def parse(self) -> dict:
        super().parse()

        res = self.session.get(self.server_list_url, timeout=60)
        assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
        html = etree.HTML(res.text)
        server_card_xpath_list = html.xpath('//div[@class="col-sm-4 col-md-3 portfolio-item vlesstcp"]')
        # server_host_list = [x.xpath('ul/li[2]/text()')[0].split(':')[1].strip() for x in server_card_xpath_list]
        server_ip_list = [x.xpath('ul/li[2]/text()')[0].split(':')[1].strip() for x in server_card_xpath_list]
        server_port_list = [int(x.xpath('ul/li[3]/text()')[0].split(':')[1].strip()) for x in server_card_xpath_list]
        # print(region_str_list) # ['Singapore', ..
        server_region_list = [x.xpath('ul/li[1]/text()')[0].strip() for x in server_card_xpath_list]
        # print(region_str_list) # ['Singapore', ..
        server_available_list = [x.xpath('ul/li[5]/text()[2]')[0].strip()=='Server Online' for x in server_card_xpath_list]
        # print(region_str_list) # ['Singapore', ..
        server_url_list = [x.xpath('a/@href')[0] for x in server_card_xpath_list]
        # print(region_url_list) # ['https://www.freevmess.com/singapore-v2ray-server', ..

        ret = dict()
        for ip,port,region,available,url in tqdm(zip(server_ip_list,server_port_list,server_region_list,server_available_list,server_url_list),
                                                 total=len(server_ip_list), desc=f'{self.name} checking ips: '):
            if not available:
                continue
            if not self.check_server(ip, port):
                continue
            ret[url] = {'region': region, 'ip': ip, 'port': port, 'Referer': res.url}
        return ret             


SLP_FREEVMESS = Server_list_parser_freevmess()