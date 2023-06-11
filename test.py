from spider.server_list.server_list_parser_vpnjantit import SLP_VPNJANTIT
from spider.server_list.server_list_parser_lionssh import SLP_LIONSSH
from spider.server_list.server_list_parser_akunssh import SLP_AKUNSSH
from spider.server_list.server_list_parser_sshvpnfree import SLP_SSHVPNFREE
from spider.server_list.server_list_parser_sshocean import SLP_SSHOCEAN
from spider.server_list.server_list_parser_freevmess import SLP_FREEVMESS
from spider.server.server_parser_sshvpnfree import SP_SSHVPNFREE, Server_parser_sshvpnfree
# from spider.server.server_parser_vpnjantit import Server_parser_vpnjantit
# from spider.server_list.server_list_parser_serverssh import SLP_SERVERSSH

# print(SLP_LIONSSH.parse())
sl=SLP_FREEVMESS.parse()
for item in list(sl.items()):
    print(item)
print(len(sl))
# server_dict={
#     'https://sshvpnfree.com/accounts/VMESS/60': {'region': 'France, Gravelines', 'port': 80, 'Referer': 'https://sshvpnfree.com/type/VMESS'}
# }
# SP=Server_parser_sshvpnfree(server_dict=server_dict)
# SP.parse()