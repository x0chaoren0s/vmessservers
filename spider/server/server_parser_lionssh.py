import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)


from .server_parser_base import Server_parser_base, Tuple
from ..server_list.server_list_parser_lionssh import SLP_LIONSSH

from lxml import etree
import json

class Server_parser_lionssh(Server_parser_base):
    name = 'lionssh'
    def __init__(self, server_dict: dict = None, server_list_parser = SLP_LIONSSH, interval_sec: int = 0) -> None:
        super().__init__(server_dict, server_list_parser, interval_sec, False)

    def filling_form(self, res) -> Tuple[str, dict]:
        form_data = dict()
        html = etree.HTML(res.text)
        websiteKey = html.xpath('//div[@class="g-recaptcha"]/@data-sitekey')[0]
        recaptcha_res = self.solve_recaptcha_v2(res.url, websiteKey)
        if recaptcha_res=='solve failed.':
            form_data['error_info'] = recaptcha_res
            return res.url, form_data
        form_data['bug_host'] = ''
        form_data['g-recaptcha-response'] = recaptcha_res
        form_data['server_type'] = 'vray'
        form_data['username'] = self.getRandStr(12)
        form_data['_token'] = html.xpath('//input[@name="_token"]/@value')[0]

        self.headers['x-csrf-token'] = html.xpath('//meta[@name="csrf-token"]/@content')[0]
        self.headers['x-requested-with'] = 'XMLHttpRequest'
        self.headers['x-xsrf-token'] = res.headers['set-cookie'].split('; ')[0].split('=')[1]

        return res.url, form_data
    
    def after_filling_form(self, res) -> dict:
        ret = dict()
        # html = etree.HTML(res.text)
        try:
            # info_card_xpath = html.xpath('//div[@class="alert alert_success py-4 text-sm bg-white border-green-600 text-green-600 shadow-lg leading-relaxed"]')[0]
            ret['config'] = json.loads(json.loads(res.content.decode())['data']['account']['config'])['ntls']
            ret['date_create'] = json.loads(res.content.decode())['data']['account']['created_at'][:10]
            ret['date_expire'] = json.loads(res.content.decode())['data']['account']['expired_at'][:10]
        except:
            ret['error_info'] = 'error in [after_filling_form]'
            with open(f'{self.name}.html', 'w', encoding='GB18030') as fout:
                print(res.text, file=fout)
        return ret
    
SP_LIONSSH = Server_parser_lionssh()