import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)

from .server_list_parser_base import Server_list_parser_base

from lxml import etree
from tqdm import tqdm

class Server_list_parser_opentunnel(Server_list_parser_base):
    name = 'vmess_list_opentunnel'

    def __init__(self, server_list_url: str = 'https://opentunnel.net/v2ray/',
                 server_provider_url: str = None) -> None:
        super().__init__(server_list_url, server_provider_url)

    def parse(self) -> dict:
        super().parse()

        res = self.session.get(self.server_list_url, timeout=60)
        assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
        html = etree.HTML(res.text)
        server_card_xpath_list = html.xpath('//div[@class="col-lg-3 mb-5 mb-lg-4"]')
        server_host_list = [x.xpath('div/div/ul/li[1]/text()[3]')[0].strip() for x in server_card_xpath_list]
        # print(region_str_list) # ['Singapore', ..
        server_region_list = [x.xpath('div/div/div[2]/span[1]/text()')[0].strip() for x in server_card_xpath_list]
        # print(region_str_list) # ['Singapore', ..
        server_available_list = [len(x.xpath('div/div/div[2]/span[@class="status status-green"]'))>0 and
                                 len(x.xpath('div/div/div[3]/span[@class="badge bg-primary mt-1"]'))>0 for x in server_card_xpath_list]
        # print(region_str_list) # ['Singapore', ..
        server_url_list = [self.server_provider_url+x.xpath('div/div/div/a/@href')[0] for x in server_card_xpath_list]
        # print(region_url_list) # ['https://www.opentunnel.com/singapore-v2ray-server', ..

        ret = dict()
        for host,region,available,url in tqdm(zip(server_host_list,server_region_list,server_available_list,server_url_list),
                                                 total=len(server_host_list), desc=f'{self.name} checking hosts: '):
            if not available:
                continue
            if not self.check_server(host, 80):
                continue
            ret[url] = {'region': region, 'host': host, 'port': 80, 'Referer': res.url}
        return ret                    


SLP_OPENTUNNEL = Server_list_parser_opentunnel()