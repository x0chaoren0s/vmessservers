import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)

from .server_list_parser_base import Server_list_parser_base

from lxml import etree
from tqdm import tqdm

class Server_list_parser_lionssh(Server_list_parser_base):
    name = 'vmess_list_lionssh'

    def __init__(self, server_list_url: str = 'https://lionssh.com/services/vray',
                 server_provider_url: str = None) -> None:
        super().__init__(server_list_url, server_provider_url)

    def parse(self) -> dict:
        super().parse()

        res = self.session.get(self.server_list_url, timeout=60, headers=self.headers)
        self.headers['Referer'] = res.url
        # assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
        # print(res.text)
        html = etree.HTML(res.text)
        region_card_xpath_list = html.xpath('//div[@class="lg:w-3/12 md:w-6/12 w-full p-4"]')
        region_str_list = [x.xpath('div/h3/text()')[0].strip() for x in region_card_xpath_list]
        # print(region_str_list) # ['Singapore', ..
        region_url_list = [x.xpath('div/div[3]/div/a[1]/@href')[0].strip() for x in region_card_xpath_list]
        # print(region_url_list) # ['https://www.lionssh.com/singapore-v2ray-server', ..
        region_available_list = [len(url)>0 for url in region_url_list]
        # print(region_available_list) # ['Singapore', ..

        ret = dict()
        hosts = set() # 有很多页面创建的是同一个host，因此需要记录，并对于同一个host只创建一次
        for region,url,available in tqdm(zip(region_str_list,region_url_list,region_available_list),
                                desc=f'{self.name} parsing regions: ', total=len(region_str_list)):
        # for url in tqdm(region_url_list, desc=f'{self.name} parsing regions: '):
            if not available:
                continue
            res = self.session.get(url, timeout=60, headers=self.headers)
            assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
            # print(res.text)
            html = etree.HTML(res.text)
            server_card_xpath_list = html.xpath('//div[@class="server-card bg-white rounded-lg shadow-countryCard p-6 border border-gray-70"]')
            server_host_list = [x.xpath('div/div[1]/span[2]/text()')[0].strip().split(':')[1].strip() for x in server_card_xpath_list]
            # print(server_host_list) # ['Singapore', ..
            # server_region_list = [x.xpath('div/div/ul/li[2]/span/b/text()')[0].strip() for x in server_card_xpath_list]
            # # print(region_str_list) # ['Singapore', ..
            server_available_list = [
                len(x.xpath('div[1]/div[@class="md:text-5xl text-3xl font-bold leading-tight mb-4 text-green-600"]'))>0 for x in server_card_xpath_list]
            # print(server_available_list) # ['Singapore', ..
            server_url_list = [x.xpath('div[1]/a/@href')[0] for x in server_card_xpath_list]
            # print(server_url_list) # ['https://www.lionssh.com/singapore-v2ray-server', ..

            for host,available,url in zip(server_host_list,server_available_list,server_url_list):
                if not available:
                    continue
                if host in hosts:
                    continue
                hosts.add(host)
                if not self.check_server(host, 80):
                    continue
                ret[url] = {'region': region, 'host': host, 'port': 80, 'Referer': res.url}
        return ret             


SLP_LIONSSH = Server_list_parser_lionssh()