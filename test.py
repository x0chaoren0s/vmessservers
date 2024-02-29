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
from spider.server.server_parser_lionssh import Server_parser_lionssh
from spider.server.server_parser_akunssh import Server_parser_akunssh
# from spider.server_list.server_list_parser_serverssh import SLP_SERVERSSH

# print(SLP_AKUNSSH.parse())
# sl=SLP_AKUNSSH.parse()
# for item in list(sl.items()):
#     print(item)
# print(len(sl))
server_dict={
    'https://akunssh.net/v2ray-vmess-server/create-v2ray-vmess-7-pl-account': {'region': 'Poland', 'host': 'pl1-vmess.tunnel.cx', 'port': 443, 'Referer': 'https://akunssh.net/v2ray-vmess-server'}
}
SP=Server_parser_akunssh(server_dict=server_dict)
SP.parse()