import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)


from .server_parser_base import Server_parser_base, Tuple
from ..server_list.server_list_parser_vpnjantit import SLP_VPNJANTIT

from lxml import etree

class Server_parser_vpnjantit(Server_parser_base):
    name = 'vpnjantit'
    def __init__(self, server_dict: dict = None, server_list_parser = SLP_VPNJANTIT, interval_sec: int = 0) -> None:
        super().__init__(server_dict, server_list_parser, interval_sec)

    def filling_form(self, res) -> Tuple[str, dict]:
        form_data = dict()
        html = etree.HTML(res.text)
        try:
            websiteKey = html.xpath('//div[@class="g-recaptcha"]/@data-sitekey')[0]
        except:
            form_data['error_info'] = 'no g-recaptcha data-sitekey'
            return res.url, form_data
        recaptcha_res = self.solve_recaptcha_v2(res.url, websiteKey)
        if recaptcha_res=='solve failed.':
            form_data['error_info'] = recaptcha_res
        form_data['user'] = self.getRandStr(12)
        form_data['pass'] = 'kosong'
        form_data['g-recaptcha-response'] = recaptcha_res
        return res.url, form_data
    
    def after_filling_form(self, res) -> dict:
        ret = dict()
        html = etree.HTML(res.text)
        info_card_xpath = html.xpath('//div[@class="row block-9"]/div[2]/div/div/div')[0]
        try:
            ret['config'] = info_card_xpath.xpath('h5/input[@id="linknya2"]/@value')[0].strip()
            ret['region'] = info_card_xpath.xpath('h5[8]/text()')[0].strip()
            ret['date_create'] = self.normalized_local_date()
            ret['date_expire'] = self.normalize_date(info_card_xpath.xpath('h5[7]/text()')[0], '%Y-%m-%d / %H:%M:%S')
        except:
            ret['error_info'] = 'something wrong.'
            with open(f'{self.name}.html', 'w', encoding='GB18030') as fout:
                print(res.text, file=fout)
        return ret
    
SP_VPNJANTIT = Server_parser_vpnjantit()

if __name__ == '__main__':
    server_dict = SLP_VPNJANTIT.parse()
    sp = Server_parser_vpnjantit(server_dict)
    sp.parse()
