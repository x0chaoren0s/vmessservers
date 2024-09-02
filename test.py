from spider.server_list.server_list_parser_vpnjantit import SLP_VPNJANTIT
from spider.server_list.server_list_parser_lionssh import SLP_LIONSSH
from spider.server_list.server_list_parser_akunssh import SLP_AKUNSSH
from spider.server_list.server_list_parser_freevpn import SLP_FREEVPN
# from spider.server_list.server_list_parser_sshvpnfree import SLP_SSHVPNFREE
# from spider.server_list.server_list_parser_sshocean import SLP_SSHOCEAN
from spider.server_list.server_list_parser_freevmess import SLP_FREEVMESS
from spider.server_list.server_list_parser_greenssh import SLP_GREENSSH
# from spider.server_list.server_list_parser_opentunnel import SLP_OPENTUNNEL
# from spider.server.server_parser_sshvpnfree import SP_SSHVPNFREE, Server_parser_sshvpnfree
from spider.server.server_parser_vpnjantit import Server_parser_vpnjantit, SP_VPNJANTIT
# from spider.server.server_parser_sshocean import Server_parser_sshocean
from spider.server.server_parser_lionssh import Server_parser_lionssh
from spider.server.server_parser_freevpn import Server_parser_freevpn
# from spider.server.server_parser_akunssh import Server_parser_akunssh
# from spider.server_list.server_list_parser_serverssh import SLP_SERVERSSH

# print(SLP_FREEVPN.get_ip())
# sl=SLP_FREEVPN.run()
# print(len(sl))
# print(sl)
# for item in list(sl.items()):
#     print(item)
# server_dict={
#     'https://lionssh.com/create/vmess-ws-in-2': {'region': 'India', 'host': 'vm.in.servergo.pw', 'port': 80, 'Referer': 'https://lionssh.com/services/vray/asia/IN/7-days'}, 
#     'https://lionssh.com/create/vmess-jp-1': {'region': 'Japan', 'host': 'vm.jp.goserver.pw', 'port': 80, 'Referer': 'https://lionssh.com/services/vray/asia/JP/7-days'}, 
#     'https://lionssh.com/create/vmess-ws-us-1': {'region': 'America', 'host': 'vm.us.servergo.pw', 'port': 80, 'Referer': 'https://lionssh.com/services/vray/america/US/7-days'}, 
#     'https://lionssh.com/create/vmess-it-1': {'region': 'Italia', 'host': 'a.it.servergo.pw', 'port': 80, 'Referer': 'https://lionssh.com/services/vray/europe/IT/7-days'}
# }
server_dict={
#     'https://www.freevpn.us/v2ray-vless/hk/server-66/': {'region': 'Hong Kong, Hong Kong', 'host': 'hkc-s66.v2sv.xyz', 'port': 8880, 'Referer': 'https://www.freevpn.us/v2ray-vless/hk/'}, 
#     'https://www.freevpn.us/v2ray-vless/hk/server-88/': {'region': 'Hong Kong, Hong Kong', 'host': 'hkc-s88.v2sv.xyz', 'port': 8880, 'Referer': 'https://www.freevpn.us/v2ray-vless/hk/'}, 
#     'https://www.freevpn.us/v2ray-vless/hk/server-89/': {'region': 'Hong Kong, Hong Kong', 'host': 'hkc-s89.v2sv.xyz', 'port': 8880, 'Referer': 'https://www.freevpn.us/v2ray-vless/hk/'}, 
#     'https://www.freevpn.us/v2ray-vless/hk/server-135/': {'region': 'Hong Kong, Hong Kong', 'host': 'hkc-s135.v2sv.xyz', 'port': 8880, 'Referer': 'https://www.freevpn.us/v2ray-vless/hk/'}, 
    'https://www.freevpn.us/v2ray-vless/hk/server-144/': {'region': 'Hong Kong, Hong Kong', 'host': 'hkc-s144.v2sv.xyz', 'port': 8880, 'Referer': 'https://www.freevpn.us/v2ray-vless/hk/'}
}
# server_dict={
#      'https://www.vpnjantit.com/create-free-account?server=premihk1&type=V2ray': {'region': 'Hong Kong, Hong Kong', 'host': 'premihk1.vpnjantit.com', 'ip': '8.217.135.42', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
#      'https://www.vpnjantit.com/create-free-account?server=hk1&type=V2ray': {'region': 'Hong Kong, Hong Kong', 'host': 'hk1.vpnjantit.com', 'ip': '8.218.127.229', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
#      'https://www.vpnjantit.com/create-free-account?server=hk2&type=V2ray': {'region': 'Hong Kong, Hong Kong', 'host': 'hk2.vpnjantit.com', 'ip': '8.218.64.170', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
#      'https://www.vpnjantit.com/create-free-account?server=hk3&type=V2ray': {'region': 'Hong Kong, Hong Kong', 'host': 'hk3.vpnjantit.com', 'ip': '8.217.100.15', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'}
# }
SP=Server_parser_freevpn(server_dict=server_dict)
SP.run()
# server_info={
#     "region": "Hong Kong, Hong Kong",
#     "host": "hk1.vpnjantit.com",
#     "ip": "8.218.127.229",
#     "port": 10000,
#     "Referer": "https://www.vpnjantit.com/free-v2ray-vmess-7-days",
#     "config": "vmess://eyJ0eXBlIjogIm5vbmUiLCAicGF0aCI6ICIvdnBuamFudGl0IiwgImhvc3QiOiAiY24uYmluZy5jb20iLCAibmV0IjogIndzIiwgInBvcnQiOiAiMTAwMDAiLCAiYWRkIjogIjguMjE4LjEyNy4yMjkiLCAicHMiOiAiMjAyNC0wNS0yMyB2cG5qYW50aXQ6IEhvbmcgS29uZywgSG9uZyBLb25nIiwgInRscyI6ICIiLCAiYWlkIjogIjAiLCAidiI6ICIyIiwgImlkIjogIjgwN2IwNTI0LTEzNjMtMTFlZi05YWQ3LTBiNmE2YTNjODkxZiIsICJzbmkiOiAiY24uYmluZy5jb20ifQ==",
#     "date_create": "2024-05-16",
#     "date_expire": "2024-05-23",
#     "date_span": "2024-05-16 - 2024-05-23"
# }
# SP.adjust_config(server_info)
# print(Server_parser_akunssh().getRandStr(12))
# print(SP_VPNJANTIT.check_server('ae1-vmess.tunnel.cx',443))

# from playwright.sync_api import sync_playwright
# import time
# playwright = sync_playwright().start()
# browser = playwright.chromium.launch(headless=False)
# page = browser.new_page()
# page.goto("https://tool.chinaz.com/speedworld/www.vpnjantit.com")
# page.wait_for_load_state('load')
# time.sleep(5)
# print([e.get_attribute('title') for e in page.locator('xpath=//div[@name="ip"]/a').all()] )

vless://66726565-7670-4e2e-b573-2d6f6c626e65@hkc-s144.v2sv.xyz:8880?encryption=none&security=none&type=ws&host=hkc-s144.v2sv.xyz&path=%2Ffreevpn%2Ffreevpn.us-olbnelrtu%2FHK#2024-09-05 freevpn: Hong Kong, Hong Kong