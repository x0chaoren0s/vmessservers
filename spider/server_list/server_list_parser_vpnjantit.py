import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)

from .server_list_parser_base import Server_list_parser_base

from lxml import etree
from tqdm import tqdm

class Server_list_parser_vpnjantit(Server_list_parser_base):
    name = 'vmess_list_vpnjantit'

    def __init__(self, server_list_url: str = 'https://www.vpnjantit.com/free-v2ray-vmess-7-days',
                 server_provider_url: str = None) -> None:
        super().__init__(server_list_url, server_provider_url)

    def parse(self) -> dict:
        super().parse()

        res = self.session.get(self.server_list_url, timeout=60)
        assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
        # print(res.text)
        html = etree.HTML(res.text)
        region_card_xpath_list = html.xpath('//div[@class="col-lg-3 col-md-6"]')
        region_str_list = [x.xpath('div/ul/li[1]/text()')[0].split('Location ')[1].strip() for x in region_card_xpath_list] # ['Sofia, Bulgaria', ..
        server_host_list = [x.xpath('div/ul/li[2]/text()')[0].strip() for x in region_card_xpath_list] # ['bg2.vpnjantit.com', ..
        server_ip_url_list = [self.server_provider_url+x.xpath('div/ul/li[2]/a/@href')[0] for x in region_card_xpath_list] #['https://www.vpnjantit.com/host-to-ip?host=bg2.vpnjantit.com', ..
        server_url_list = [self.server_provider_url+x.xpath('div/a[2]/@href')[0] 
            for x in region_card_xpath_list if len(x.xpath('div/a[2]/@href'))] # ['https://www.vpnjantit.com/create-free-account?server=bg2&type=SSH', ..
        # server_ip_list = [self.parse_ip(url) for url in server_ip_url_list] # ['195.123.228.112', ..
        
        ret = dict()
        for region,host,ip_url,url in tqdm(zip(region_str_list,server_host_list,server_ip_url_list,server_url_list),
                                           total=len(region_str_list), desc=f'{self.name} parsing ips: '):
            ip = self.parse_ip(ip_url)
            if not self.check_server(ip, 10000):
                continue
            ret[url] = {'region': region, 'host': host, 'ip': ip, 'port': 10000, 'Referer': res.url}
        return ret
    
    def parse_ip(self, ip_url):
        res = self.session.get(ip_url, timeout=60)
        assert res.status_code==200, f'status_code: {res.status_code}, url: {res.url}'
        html = etree.HTML(res.text)
        return html.xpath('//div[@class="media block-6 services border text-left"]/p/font/text()[2]')[0].split(':')[1].strip()
                




SLP_VPNJANTIT = Server_list_parser_vpnjantit()
        
if __name__ == '__main__':
    pass
    servers = SLP_VPNJANTIT.parse()
    # print(servers)
    # for s in servers:
    #     print(s,servers[s])
    # print(len(servers))