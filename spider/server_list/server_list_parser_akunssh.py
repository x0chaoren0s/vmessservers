import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)

from .server_list_parser_base import Server_list_parser_base

from lxml import etree
from tqdm import tqdm

class Server_list_parser_akunssh(Server_list_parser_base):
    name = 'vmess_list_akunssh'

    def __init__(self, server_list_url: str = 'https://akunssh.net/v2ray-vmess-server',
                 server_provider_url: str = None) -> None:
        super().__init__(server_list_url, server_provider_url)

    def parse(self) -> dict:
        super().parse()

        res = self.session.get(self.server_list_url, timeout=60)
        assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
        html = etree.HTML(res.text)
        server_card_xpath_list = html.xpath('//div[@class="col-lg-3 mb-5"]')
        print(server_card_xpath_list) # ['Singapore', ..
        server_host_list = [x.xpath('div/ul/li[1]/div/span/text()')[0].strip() for x in server_card_xpath_list]
        print(server_host_list) # ['Singapore', ..
        server_region_list = [x.xpath('div/ul/li[2]/div/span/text()')[0].strip() for x in server_card_xpath_list]
        print(server_region_list) # ['Singapore', ..
        server_available_list = [x.xpath('div/ul/li[4]/span/text()[1]')[0] for x in server_card_xpath_list]
        print(server_available_list) # ['Singapore', ..
        server_url_list = [x.xpath('div/a/@href')[0] for x in server_card_xpath_list]
        print(server_url_list) # ['https://www.akunssh.com/singapore-v2ray-server', ..

        ret = dict()
        for host,region,available,url in zip(server_host_list,server_region_list,server_available_list,server_url_list):
            if not available:
                continue
            if not self.check_server(host, 80):
                continue
            ret[url] = {'region': region, 'host': host, 'port': 80, 'Referer': res.url}
        return ret             


SLP_AKUNSSH = Server_list_parser_akunssh()