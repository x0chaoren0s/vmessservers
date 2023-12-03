from spider.server_list.server_list_parser_vpnjantit import SLP_VPNJANTIT
from spider.server_list.server_list_parser_lionssh import SLP_LIONSSH
from spider.server_list.server_list_parser_akunssh import SLP_AKUNSSH
from spider.server_list.server_list_parser_sshvpnfree import SLP_SSHVPNFREE
from spider.server_list.server_list_parser_sshocean import SLP_SSHOCEAN
from spider.server_list.server_list_parser_freevmess import SLP_FREEVMESS
from spider.server_list.server_list_parser_opentunnel import SLP_OPENTUNNEL
from spider.server.server_parser_sshvpnfree import SP_SSHVPNFREE, Server_parser_sshvpnfree
from spider.server.server_parser_vpnjantit import Server_parser_vpnjantit
from spider.server.server_parser_sshocean import Server_parser_sshocean
# from spider.server_list.server_list_parser_serverssh import SLP_SERVERSSH

# print(SLP_AKUNSSH.parse())
sl=SLP_SSHOCEAN.parse()
for item in list(sl.items()):
    print(item)
# print(len(sl))
# server_dict={
#     'https://sshocean.com/v2ray/vmess/canada/ca1': {'region': 'Canada', 'host': 'ca1.xv2ray.net', 'cloudflare_host': 'ca1.xv2ray.net', 'port': 80, 'Referer': 'https://sshocean.com/v2ray/vmess/canada'}
# }
# SP=Server_parser_sshocean(server_dict=server_dict)
# SP.parse()