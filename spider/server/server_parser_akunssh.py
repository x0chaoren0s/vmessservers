import sys
from pathlib import Path

from requests.models import Response as Response
sys.path.append(Path(__file__).parent.parent.parent)


from .server_parser_base import Server_parser_base, Tuple
from ..server_list.server_list_parser_akunssh import SLP_AKUNSSH

from lxml import etree

class Server_parser_akunssh(Server_parser_base):
    name = 'akunssh'
    def __init__(self, server_dict: dict = None, server_list_parser = SLP_AKUNSSH, interval_sec: int = 0) -> None:
        super().__init__(server_dict, server_list_parser, interval_sec)

    def filling_form(self, res) -> Tuple[str, dict]:
        form_data = dict()
        html = etree.HTML(res.text)
        post_url = 'https://akunssh.net'+html.xpath('//form/@action')[0]
        try:
            websiteKey = html.xpath('//div[@class="g-recaptcha"]/@data-sitekey')[0]
        except:
            form_data['error_info'] = 'no g-recaptcha data-sitekey'
            return post_url, form_data
        recaptcha_res = self.solve_recaptcha_v2(res.url, websiteKey)
        if recaptcha_res=='solve failed.':
            form_data['error_info'] = recaptcha_res
        form_data['_token'] = html.xpath('//input[@name="_token"]/@value')[0]
        form_data['slug'] = html.xpath('//input[@name="slug"]/@value')[0]
        form_data['username'] = self.getRandStr(12)
        form_data['sni'] = 'cn.bing.com'
        form_data['g-recaptcha-response'] = recaptcha_res
        form_data['submit'] = ''

        self._redirect_url = etree.HTML(res.text).xpath('//meta[@property="og:url"]/@content')[0]
        return post_url, form_data
    
    def post_redirect(self, res_before) -> Response:
        req = res_before.next.copy()
        req.url = self._redirect_url
        return self.session.send(req)
    
    def after_filling_form(self, res) -> dict:
        ret = dict()
        html = etree.HTML(res.text)
        info_card_xpath = html.xpath('//div[@class="alert alert-success alert-icon alert-dismissible fade show"]')[0]
        try:
            ret['host'] = info_card_xpath.xpath('div[2]/text()[2]')[0].strip()
            ret['date_create'] = self.normalize_date(info_card_xpath.xpath('div[5]/text()')[0].strip(), '%d %b %Y')
            ret['date_expire'] = self.normalize_date(info_card_xpath.xpath('div[6]/text()')[0].strip(), '%d %b %Y')
            # ret['config'] = info_card_xpath.xpath('div[8]/button[2]/@data-clipboard-text')[0].strip() # tls
            ret['config'] = info_card_xpath.xpath('div[9]/button[2]/@data-clipboard-text')[0].strip() # ntls
        except:
            ret['error_info'] = 'something wrong.'
            with open(f'{self.name}.html', 'w', encoding='GB18030') as fout:
                print(res.text, file=fout)
        return ret
    
SP_AKUNSSH = Server_parser_akunssh()

if __name__ == '__main__':
    server_dict = SLP_AKUNSSH.parse()
    sp = Server_parser_akunssh(server_dict)
    sp.parse()
