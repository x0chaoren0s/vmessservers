import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)


from .server_parser_base import Server_parser_base, Tuple
from ..server_list.server_list_parser_freevmess import SLP_FREEVMESS

from lxml import etree

import datetime, json, base64

class Server_parser_freevmess(Server_parser_base):
    name = 'freevmess'
    def __init__(self, server_dict: dict = None, server_list_parser = SLP_FREEVMESS, interval_sec: int = 0) -> None:
        super().__init__(server_dict, server_list_parser, interval_sec)

    def filling_form(self, res) -> Tuple[str, dict]:
        form_data = dict()
        html = etree.HTML(res.text)
        websiteKey = html.xpath('//div[@class="h-captcha"]/@data-sitekey')[0]
        hcaptcha_res = self.solve_hcaptcha(res.url, websiteKey)
        form_data['name'] = self.getRandStr(9)+'6' # 要求5-10个字符，要有数字
        form_data['ipuser'] = html.xpath('//input[@name="ipuser"]/@value')[0]
        form_data['nameser'] = html.xpath('//input[@name="nameser"]/@value')[0]
        form_data['id_server'] = html.xpath('//input[@name="id_server"]/@value')[0]
        form_data['ipserver'] = html.xpath('//input[@name="ipserver"]/@value')[0]
        form_data['proov'] = html.xpath('//input[@name="proov"]/@value')[0]
        form_data['datecreated'] = html.xpath('//input[@name="datecreated"]/@value')[0]
        # form_data['firstNumber'] = html.xpath('//input[@name="firstNumber"]/@value')[0]
        # form_data['secondNumber'] = html.xpath('//input[@name="secondNumber"]/@value')[0]
        # form_data['captcha'] = f"{int(form_data['firstNumber'])+int(form_data['secondNumber'])}"
        form_data['g-recaptcha-response'] = hcaptcha_res
        form_data['h-captcha-response'] = hcaptcha_res
        form_data['submit'] = ''
        return res.url, form_data
    
    def after_filling_form(self, res) -> dict:
        ret = dict()
        html = etree.HTML(res.text)
        try:
            info_card_xpath = html.xpath('//div[@class="col-xs-12 col-sm-4 col-md-4 portfolio-item vlesstcp"][2]')[0]
            ret['region'] = info_card_xpath.xpath('ul/li[1]/text()')[0].strip()
            ret['config'] = html.xpath('//input[@id="myInput"]/@value')[0].strip()
            ret['host'] = json.loads(base64.b64decode(ret['config'].split('vmess://')[1]).decode())['add']
            ret['ip'] = info_card_xpath.xpath('ul/li[3]/text()')[0].strip()
            ret['port'] = int(info_card_xpath.xpath('ul/li[2]/text()')[0].split(' ')[-1])
            ret['use_ip'] = False # 返回的config用的是ip对应的host（网页上没显示这个信息），host可用，但改成ip就能ping却用不了
            ret['date_create'] = self.normalized_local_date()
            dt = datetime.datetime.strptime(ret['date_create'], "%Y-%m-%d")
            ret['date_expire'] = (dt + datetime.timedelta(days=5)).strftime("%Y-%m-%d")
        except:
            ret['error_info'] = 'something wrong.'
            with open(f'{self.name}.html', 'w', encoding='GB18030') as fout:
                print(res.text, file=fout)
        return ret
    
SP_FREEVMESS = Server_parser_freevmess()

if __name__ == '__main__':
    server_dict = SLP_FREEVMESS.parse()
    sp = Server_parser_freevmess(server_dict)
    sp.parse()
