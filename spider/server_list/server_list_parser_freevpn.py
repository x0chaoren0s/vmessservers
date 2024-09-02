import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)

from .server_list_parser_base import Server_list_parser_base

from lxml import etree
from tqdm import tqdm

class Server_list_parser_freevpn(Server_list_parser_base):
    name = 'vless_list_freevpn'

    def __init__(self, server_list_url: str = 'https://www.freevpn.us/v2ray-vless/',
                 server_provider_url: str = None) -> None:
        super().__init__(server_list_url, server_provider_url)
        self.use_proxy = True

    def parse(self) -> dict:
        super().parse()
        res = self.session.get(self.server_list_url, proxies=self.proxies)
        assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
        html = etree.HTML(res.text)
        region_card_xpath_list = html.xpath('//div[@class="col-md-3 my-2"]')
        region_urls_list = [self.server_provider_url+x.xpath('div/a[@class="btn btn-success btn-sm waves-effect waves-light"]/@href')[0].strip() 
                            for x in region_card_xpath_list]
        server_host_list,server_region_list,server_available_list,server_url_list = [], [], [], []
        for region_server_list_url in tqdm(region_urls_list, desc=f'{self.name} parsing regions:'):
            # res = self.session.get('https://www.freevpn.us/v2ray-vless/hk/')
            res = self.session.get(region_server_list_url, proxies=self.proxies)
            assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
            html = etree.HTML(res.text)
            server_card_xpath_list = html.xpath('//div[@class="col-lg-3 mb-5 mb-lg-4"]')
            # print(server_card_xpath_list) # ['Singapore', ..
            server_host_list += [x.xpath('div/div/ul/li[1]/text()[3]')[0].strip() for x in server_card_xpath_list]
            # print(server_host_list) # ['Singapore', ..
            server_region_list += [f"{x.xpath('div/div/div[2]/span[1]/text()')[0].strip()}, "+
                                f"{x.xpath('div/div/div[2]/span[2]/text()')[0].strip()}" for x in server_card_xpath_list]
            # print(server_region_list) # ['Singapore', ..
            server_available_list += [len(x.xpath('div/div/div[2]/span[@class="status status-green"]'))>0 for x in server_card_xpath_list]
            # print(server_available_list) # [True, ..
            server_url_list += ['https://www.freevpn.us'+x.xpath('div/div/div/a/@href')[0] for x in server_card_xpath_list]
            # print(server_url_list) # ['https://freevpn.net/v2ray-vmess-server/create-v2ray-vmess-7-ae-account', ..

        ret = dict()
        for host,region,available,url in tqdm(zip(server_host_list,server_region_list,server_available_list,server_url_list),
                                            total=len(server_host_list), desc=f'{self.name} checking hosts: '):
            if not available:
                continue
            if not self.check_server(host, 8880):
                continue
            ret[url] = {'region': region, 'host': host, 'port': 8880, 'Referer': res.url}
        return ret             


SLP_FREEVPN = Server_list_parser_freevpn()