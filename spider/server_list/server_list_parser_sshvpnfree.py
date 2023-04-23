import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)

from .server_list_parser_base import Server_list_parser_base

from lxml import etree
from tqdm import tqdm

class Server_list_parser_sshvpnfree(Server_list_parser_base):
    name = 'vmess_list_sshvpnfree'

    def __init__(self, server_list_url: str = 'https://sshvpnfree.com/type/VMESS',
                 server_provider_url: str = None) -> None:
        super().__init__(server_list_url, server_provider_url)

    def parse(self) -> dict:
        super().parse()

        res = self.session.get(self.server_list_url, timeout=60)
        assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
        html = etree.HTML(res.text)
        server_card_xpath_list = html.xpath('//div[@class="col-md-3"]')
        # server_host_list = [x.xpath('div/div/ul/li[1]/span/b/text()')[0].strip() for x in server_card_xpath_list]
        # print(region_str_list) # ['Singapore', ..
        server_region_list = [x.xpath('div/ul/li[4]/span/text()')[0].strip()+', '+
                              x.xpath('div/ul/li[5]/span/text()')[0].strip() for x in server_card_xpath_list]
        # print(region_str_list) # ['Singapore', ..
        # server_available_list = [len(x.xpath('div/div/p/span[@class="badge badge-success"]'))>0 for x in server_card_xpath_list]
        # print(region_str_list) # ['Singapore', ..
        server_url_list = [x.xpath('div/ul/div/a/@href')[0] for x in server_card_xpath_list]
        # print(region_url_list) # ['https://www.sshvpnfree.com/singapore-v2ray-server', ..

        ret = dict()
        for region,url in zip(server_region_list,server_url_list):
            ret[url] = {'region': region, 'port': 80, 'Referer': res.url}
        return ret             


SLP_SSHVPNFREE = Server_list_parser_sshvpnfree()