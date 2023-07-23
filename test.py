from spider.server_list.server_list_parser_vpnjantit import SLP_VPNJANTIT
from spider.server_list.server_list_parser_lionssh import SLP_LIONSSH
from spider.server_list.server_list_parser_akunssh import SLP_AKUNSSH
from spider.server_list.server_list_parser_sshvpnfree import SLP_SSHVPNFREE
from spider.server_list.server_list_parser_sshocean import SLP_SSHOCEAN
from spider.server_list.server_list_parser_freevmess import SLP_FREEVMESS
from spider.server_list.server_list_parser_opentunnel import SLP_OPENTUNNEL
from spider.server.server_parser_sshvpnfree import SP_SSHVPNFREE, Server_parser_sshvpnfree
from spider.server.server_parser_vpnjantit import Server_parser_vpnjantit
# from spider.server_list.server_list_parser_serverssh import SLP_SERVERSSH

# print(SLP_LIONSSH.parse())
# sl=SLP_SSHOCEAN.parse()
# for item in list(sl.items()):
#     print(item)
# print(len(sl))
server_dict={
    'https://www.vpnjantit.com/create-free-account?type=V2ray&server=ar1#create': {'region': 'Argentina 1', 'host': 'ar1.vpnjantit.com', 'ip': '38.54.45.124', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/create-free-account?server=cz2&type=V2ray'}
}
SP=Server_parser_vpnjantit(server_dict=server_dict)
SP.parse()