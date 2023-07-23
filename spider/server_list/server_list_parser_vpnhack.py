import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)

from .server_list_parser_base import Server_list_parser_base

from lxml import etree
from tqdm import tqdm

'''
vpnhack的vmess服务器联不通
'''

class Server_list_parser_vpnhack(Server_list_parser_base):
    name = 'vmess_list_vpnhack'

    def __init__(self, server_list_url: str = 'https://vpnhack.com/v2ray/vmess',
                 server_provider_url: str = None) -> None:
        super().__init__(server_list_url, server_provider_url)

    def parse(self) -> dict:
        super().parse()

        res = self.session.get(self.server_list_url, timeout=60)
        assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
        # print(res.text)
        html = etree.HTML(res.content)
        region_card_xpath_list = html.xpath('//div[@class="col-lg-3 mb-3"]')
        # region_str_list = [x.xpath('div/h5/text()')[0] for x in region_card_xpath_list]
        # # print(region_str_list) # ['Singapore', ..
        region_url_list = [x.xpath('div/a/@href')[0] for x in region_card_xpath_list]
        # print(region_url_list) # ['https://www.vpnhack.com/singapore-v2ray-server', ..

        ret = dict()
        # for region,url in tqdm(zip(region_str_list,region_url_list),
        #                         desc=f'{self.name} parsing regions: ', total=len(region_str_list)):
        for url in tqdm(region_url_list, desc=f'{self.name} parsing regions: '):
            res = self.session.get(url, timeout=60)
            assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
            # print(res.text)
            html = etree.HTML(res.text)
            server_card_xpath_list = html.xpath('//div[@class="col-lg-3 mb-3"]')
            server_host_list = [x.xpath('div/table/tr[1]/td[2]/b/text()')[0].strip() for x in server_card_xpath_list] # 有些网页源代码中table下面不一定有tbody，而是直接跟tr
            # print(region_str_list) # ['Singapore', ..
            server_region_list = [x.xpath('div/table/tr[2]/td[2]/b/text()')[0].strip() for x in server_card_xpath_list]
            # print(region_str_list) # ['Singapore', ..
            server_available_list = [len(x.xpath('div/p/span[@class="badge bg-success"]'))>0 for x in server_card_xpath_list]
            # print(region_str_list) # ['Singapore', ..
            server_url_list = [x.xpath('div/a/@href')[0] for x in server_card_xpath_list]
            # print(region_url_list) # ['https://www.vpnhack.com/singapore-v2ray-server', ..

            for host,region,available,url in zip(server_host_list,server_region_list,server_available_list,server_url_list):
                if not available:
                    continue
                if not self.check_server(host, 80):
                    continue
                ret[url] = {'region': region, 'host': host, 'port': 80, 'Referer': res.url}
        return ret             


SLP_VPNHACK = Server_list_parser_vpnhack()