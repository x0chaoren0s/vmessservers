import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)


from .server_parser_base import Server_parser_base, Tuple
from ..server_list.server_list_parser_freevpn import SLP_FREEVPN

from lxml import etree

import datetime, json, base64

class Server_parser_freevpn(Server_parser_base):
    name = 'freevpn'
    def __init__(self, server_dict: dict = None, server_list_parser = SLP_FREEVPN, interval_sec: int = 0) -> None:
        super().__init__(server_dict, server_list_parser, interval_sec)

    def filling_form(self, res) -> Tuple[str, dict]:
        form_data = dict()
        html = etree.HTML(res.text)
        websiteKey = html.xpath('//div[@class="g-recaptcha"]/@data-sitekey')[0]
        recaptcha_res = self.solve_recaptcha_v2(res.url, websiteKey)
        form_data['adblock_detected'] = '0'
        form_data['action']     = html.xpath('//input[@name="action"]/@value')[0]
        form_data['server']     = html.xpath('//input[@name="server"]/@value')[0]
        form_data['serverHost'] = html.xpath('//input[@name="serverHost"]/@value')[0]
        form_data['type']       = html.xpath('//input[@name="type"]/@value')[0]
        form_data['username']   = self.getRandStr(9)
        form_data['bugHost']    = 'cn.bing.com'
        form_data['g-recaptcha-response'] = recaptcha_res
        form_data['term']       = 'on'
        post_url = 'https://www.freevpn.us/core.json'
        return post_url, form_data
    
    def after_filling_form(self, res) -> dict:
        # ntls: vless://66726565-7670-4e2e-b573-2d6e6e656e6e@hkc-s89.v2sv.xyz:80?   # 此处add是真实add  提供商填错了写成cn.bing.com
        #               uuid@add:port?
        #           encryption=none&
        #           security=none&
        #           type=ws&
        #           host=hkc-s89.v2sv.xyz&      # 很离谱，同一个提供商的连接有时候要用ip，有时候要用host
        #           path=%2Ffreevpn%2Ffreevpn.us-nnennenne%2FHK
        #           #%5BHK%5D freevpn.us-nnennenne
        ret = dict()
        resJson = res.json()
        try:
            html = etree.HTML(resJson['html'])
            # ret['region'] = info_card_xpath.xpath('ul/li[1]/text()')[0].strip()
            ret['type'] = 'vless'
            ret['config'] = html.xpath('//textarea[@id="v2ntls"]/text()')[0].strip()
            ret['host'] = html.xpath('/html/body/div/ul/li[1]/text()')[0].split(':')[1].strip() # Host Name: hkc-s89.v2sv.xyz
            ret['port'] = 8880
            # ret['use_ip'] = False # 返回的config用的是ip对应的host（网页上没显示这个信息），host可用，但改成ip就能ping却用不了
            ret['date_create'] = self.normalized_local_date()
            ret['date_expire'] = resJson['expired'][:10] # "2024-09-05 08:52:37"
        except:
            ret['error_info'] = 'something wrong.'
            with open(f'{self.name}.html', 'w', encoding='GB18030') as fout:
                print(res.text, file=fout)
        return ret
    
SP_FREEVPN = Server_parser_freevpn()

if __name__ == '__main__':
    server_dict = SLP_FREEVPN.parse()
    sp = Server_parser_freevpn(server_dict)
    sp.parse()
