import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)


from .server_parser_base import Server_parser_base, Tuple
from ..server_list.server_list_parser_sshocean import SLP_SSHOCEAN

from lxml import etree

class Server_parser_sshocean(Server_parser_base):
    name = 'sshocean'
    def __init__(self, server_dict: dict = None, server_list_parser = SLP_SSHOCEAN, interval_sec: int = 0) -> None:
        super().__init__(server_dict, server_list_parser, interval_sec)

    def filling_form(self, res) -> Tuple[str, dict]:
        form_data = dict()
        html = etree.HTML(res.text)
        websiteKey = html.xpath('//div[@class="g-recaptcha"]/@data-sitekey')[0]
        recaptcha_res = self.solve_recaptcha_v2(res.url, websiteKey)
        if recaptcha_res=='solve failed.':
            form_data['error_info'] = recaptcha_res
        form_data['username'] = self.getRandStr(12)
        form_data['sni_bug'] = ''
        form_data['sni_type'] = 'sni'
        form_data['g-recaptcha-response'] = recaptcha_res
        form_data['submit'] = ''
        return res.url, form_data
    
    def after_filling_form(self, res) -> dict:
        ret = dict()
        html = etree.HTML(res.text)
        try:
            info_card_xpath = html.xpath('//div[@class="col-10 col-lg-4 col-10 card mb-2 h-100"]')[0]
            # ret['config'] = html.xpath('//input[@id="ssClipboard"]/@value')[0].strip()
            ret['config'] = html.xpath('//input[@id="ssClipboardtls"]/@value')[0].strip()
            # ret['cloudflare_host'] = info_card_xpath.xpath('div/div/ul/li[2]/span/text()')[0][17:]
            # ret['use_cloudflare'] = False
            # ret['region'] = html.xpath('//meta[@property="og:title"]/@content')[0][53:].strip()
            ret['change_host'] = False # 一般都可以修改设置中的host和sni为cn.bing.com，但是该网站的配置改了host后连不上
            #Created: 25 Mar 2024
            # ret['date_create'] = self.normalize_date(info_card_xpath.xpath('div/div/ul/li[11]/span/text()')[0][9:], '%d %b %Y')
            date_create_str = [s for s in info_card_xpath.xpath('div/div/ul/li/span/text()') if s.startswith('Created: ')][0][9:]
            ret['date_create'] = self.normalize_date(date_create_str, '%d %b %Y')
            #Expired: 1 Apr 2024
            # ret['date_expire'] = self.normalize_date(info_card_xpath.xpath('div/div/ul/li[12]/span/text()')[0][9:], '%d %b %Y')
            date_expire_str = [s for s in info_card_xpath.xpath('div/div/ul/li/span/text()') if s.startswith('Expired: ')][0][9:]
            ret['date_expire'] = self.normalize_date(date_expire_str, '%d %b %Y')

        except:
            ret['error_info'] = 'something wrong.'
            with open(f'{self.name}.html', 'w', encoding='GB18030') as fout:
                print(res.text, file=fout)
        return ret
    
SP_SSHOCEAN = Server_parser_sshocean()

if __name__ == '__main__':
    server_dict = SP_SSHOCEAN.parse()
    sp = Server_parser_sshocean(server_dict)
    sp.parse()
