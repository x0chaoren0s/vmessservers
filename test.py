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
# sl=SLP_VPNJANTIT.parse()
# for item in list(sl.items()):
#     print(item)
# print(len(sl))
server_dict={
    'https://www.vpnjantit.com/create-free-account?server=ae1&type=V2ray': {'region': 'Dubai, UAE', 'host': 'ae1.vpnjantit.com', 'ip': '185.249.135.239', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ae2&type=V2ray': {'region': 'Al Fujairah City, UAE', 'host': 'ae2.vpnjantit.com', 'ip': '5.44.42.16', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ae3&type=V2ray': {'region': 'Al Fujairah City, UAE', 'host': 'ae3.vpnjantit.com', 'ip': '5.44.42.186', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ae4&type=V2ray': {'region': 'Al Fujairah City, UAE', 'host': 'ae4.vpnjantit.com', 'ip': '5.44.42.42', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=au2&type=V2ray': {'region': 'Sydney, Australia', 'host': 'au2.vpnjantit.com', 'ip': '47.74.90.55', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=az1&type=V2ray': {'region': 'Baku, Azerbaijan', 'host': 'az1.vpnjantit.com', 'ip': '180.149.44.176', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=be1&type=V2ray': {'region': 'Brussels, Belgium', 'host': 'be1.vpnjantit.com', 'ip': '141.98.233.6', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=bg1&type=V2ray': {'region': 'Sofia, Bulgaria', 'host': 'bg1.vpnjantit.com', 'ip': '195.123.227.30', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=bg2&type=V2ray': {'region': 'Sofia, Bulgaria', 'host': 'bg2.vpnjantit.com', 'ip': '195.123.228.112', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=bg3&type=V2ray': {'region': 'Sofia, Bulgaria', 'host': 'bg3.vpnjantit.com', 'ip': '195.123.228.18', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=bh1&type=V2ray': {'region': 'Manama, Bahrain', 'host': 'bh1.vpnjantit.com', 'ip': '38.54.2.143', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=br4&type=V2ray': {'region': 'S�o Paulo, Brazil', 'host': 'br4.vpnjantit.com', 'ip': '89.39.161.235', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=br6&type=V2ray': {'region': 'S�o Paulo, Brazil', 'host': 'br6.vpnjantit.com', 'ip': '78.111.102.76', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ca1&type=V2ray': {'region': 'Montr�al, Canada', 'host': 'ca1.vpnjantit.com', 'ip': '51.79.70.147', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ca2&type=V2ray': {'region': 'Montr�al, Canada', 'host': 'ca2.vpnjantit.com', 'ip': '192.99.247.52', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=cz1&type=V2ray': {'region': 'Prague, Czech Republic', 'host': 'cz1.vpnjantit.com', 'ip': '195.123.246.120', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=cz2&type=V2ray': {'region': 'Prague, Czech Republic', 'host': 'cz2.vpnjantit.com', 'ip': '62.233.57.53', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ee1&type=V2ray': {'region': 'Tallinn, Estonia', 'host': 'ee1.vpnjantit.com', 'ip': '185.123.53.178', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=fi1&type=V2ray': {'region': 'Helsinki, Finland', 'host': 'fi1.vpnjantit.com', 'ip': '77.91.103.148', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=fr3&type=V2ray': {'region': 'Strasbourg, France', 'host': 'fr3.vpnjantit.com', 'ip': '149.202.55.79', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=fr5&type=V2ray': {'region': 'Paris, France', 'host': 'fr5.vpnjantit.com', 'ip': '188.92.28.44', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=gr2&type=V2ray': {'region': 'Frankfurt am Main, Germany', 'host': 'gr2.vpnjantit.com', 'ip': '51.75.74.253', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=gr3&type=V2ray': {'region': 'Frankfurt am Main, Germany', 'host': 'gr3.vpnjantit.com', 'ip': '51.68.172.194', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=gr4&type=V2ray': {'region': 'Karlsruhe, Germany', 'host': 'gr4.vpnjantit.com', 'ip': '87.106.198.110', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=gr5&type=V2ray': {'region': 'Frankfurt am Main, Germany', 'host': 'gr5.vpnjantit.com', 'ip': '193.233.164.246', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=gr6&type=V2ray': {'region': 'Frankfurt am Main, Germany', 'host': 'gr6.vpnjantit.com', 'ip': '62.133.60.134', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=gr7&type=V2ray': {'region': 'Karlsruhe, Germany', 'host': 'gr7.vpnjantit.com', 'ip': '217.160.33.100', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=hk3&type=V2ray': {'region': 'Hong Kong, Hong Kong', 'host': 'hk3.vpnjantit.com', 'ip': '185.244.208.71', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=hu1&type=V2ray': {'region': 'Budapest, Hungary', 'host': 'hu1.vpnjantit.com', 'ip': '193.201.188.110', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ie1&type=V2ray': {'region': 'Dublin, Ireland', 'host': 'ie1.vpnjantit.com', 'ip': '95.164.44.151', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=il1&type=V2ray': {'region': 'Petah Tiqva, Israel', 'host': 'il1.vpnjantit.com', 'ip': '195.20.17.47', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=in2&type=V2ray': {'region': 'Panvel, India', 'host': 'in2.vpnjantit.com', 'ip': '139.84.170.47', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=in5&type=V2ray': {'region': 'Artist Village, India', 'host': 'in5.vpnjantit.com', 'ip': '103.248.61.51', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=in6&type=V2ray': {'region': 'Mumbai, India', 'host': 'in6.vpnjantit.com', 'ip': '147.139.3.65', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=it2&type=V2ray': {'region': 'Palermo, Italy', 'host': 'it2.vpnjantit.com', 'ip': '91.201.65.220', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=it3&type=V2ray': {'region': 'Palermo, Italy', 'host': 'it3.vpnjantit.com', 'ip': '45.86.231.50', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=jp1&type=V2ray': {'region': 'Urayasu, Japan', 'host': 'jp1.vpnjantit.com', 'ip': '95.85.94.220', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=jp3&type=V2ray': {'region': 'Tokyo, Japan', 'host': 'jp3.vpnjantit.com', 'ip': '47.245.1.171', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=kh1&type=V2ray': {'region': 'Phnom Penh, Cambodia', 'host': 'kh1.vpnjantit.com', 'ip': '220.158.233.184', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=kr1&type=V2ray': {'region': 'Paripark, South Korea', 'host': 'kr1.vpnjantit.com', 'ip': '141.164.46.148', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=kz1&type=V2ray': {'region': 'Almaty, Kazakhstan', 'host': 'kz1.vpnjantit.com', 'ip': '176.120.72.175', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=kz2&type=V2ray': {'region': 'Almaty, Kazakhstan', 'host': 'kz2.vpnjantit.com', 'ip': '45.80.208.143', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=lu1&type=V2ray': {'region': 'Dudelange, Luxembourg', 'host': 'lu1.vpnjantit.com', 'ip': '107.189.7.49', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=md1&type=V2ray': {'region': 'Chisinau, Moldova', 'host': 'md1.vpnjantit.com', 'ip': '194.110.247.103', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=my2&type=V2ray': {'region': 'Kuala Lumpur, Malaysia', 'host': 'my2.vpnjantit.com', 'ip': '47.250.14.181', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=my3&type=V2ray': {'region': 'Kuala Lumpur, Malaysia', 'host': 'my3.vpnjantit.com', 'ip': '47.254.231.238', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=my4&type=V2ray': {'region': 'Kuala Lumpur, Malaysia', 'host': 'my4.vpnjantit.com', 'ip': '47.254.192.14', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=nl2&type=V2ray': {'region': 'Amsterdam, Netherlands', 'host': 'nl2.vpnjantit.com', 'ip': '195.123.219.71', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ph3&type=V2ray': {'region': 'Manila, Philippines', 'host': 'ph3.vpnjantit.com', 'ip': '103.56.5.143', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ph5&type=V2ray': {'region': 'Manila, Philippines', 'host': 'ph5.vpnjantit.com', 'ip': '87.121.117.103', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ph7&type=V2ray': {'region': 'Quezon City, Philippines', 'host': 'ph7.vpnjantit.com', 'ip': '49.157.46.156', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=pl1&type=V2ray': {'region': 'Warsaw, Poland', 'host': 'pl1.vpnjantit.com', 'ip': '146.59.44.159', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=pt1&type=V2ray': {'region': 'Braga, Portugal', 'host': 'pt1.vpnjantit.com', 'ip': '5.182.39.240', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ro1&type=V2ray': {'region': 'Bucharest, Romania', 'host': 'ro1.vpnjantit.com', 'ip': '82.117.255.207', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=se1&type=V2ray': {'region': 'Stockholm, Sweden', 'host': 'se1.vpnjantit.com', 'ip': '46.246.98.117', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-premium-account?server=sg1&type=V2ray': {'region': 'Singapore, Singapore', 'host': 'sg1.vpnjantit.com', 'ip': '128.199.247.154', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=sg2&type=V2ray': {'region': 'Singapore, Singapore', 'host': 'sg2.vpnjantit.com', 'ip': '103.231.188.124', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=sg3&type=V2ray': {'region': 'Singapore, Singapore', 'host': 'sg3.vpnjantit.com', 'ip': '45.76.150.232', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=sk1&type=V2ray': {'region': 'Bratislava, Slovakia', 'host': 'sk1.vpnjantit.com', 'ip': '5.35.103.179', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=sp1&type=V2ray': {'region': 'Logro�o, Spain', 'host': 'sp1.vpnjantit.com', 'ip': '212.227.228.91', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=sz1&type=V2ray': {'region': 'Z�rich, Switzerland', 'host': 'sz1.vpnjantit.com', 'ip': '45.90.59.186', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=th1&type=V2ray': {'region': 'Bangkok, Thailand', 'host': 'th1.vpnjantit.com', 'ip': '185.78.165.153', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=th2&type=V2ray': {'region': 'Mueang Nonthaburi, Thailand', 'host': 'th2.vpnjantit.com', 'ip': '141.98.19.77', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=th3&type=V2ray': {'region': 'Bangkok, Thailand', 'host': 'th3.vpnjantit.com', 'ip': '103.114.203.80', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=tr1&type=V2ray': {'region': 'Istanbul, Turkey', 'host': 'tr1.vpnjantit.com', 'ip': '83.217.9.70', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=tr5&type=V2ray': {'region': 'Istanbul, Turkey', 'host': 'tr5.vpnjantit.com', 'ip': '45.144.153.64', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=tr6&type=V2ray': {'region': 'Istanbul, Turkey', 'host': 'tr6.vpnjantit.com', 'ip': '83.217.9.81', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ua1&type=V2ray': {'region': 'Kyiv, Ukraine', 'host': 'ua1.vpnjantit.com', 'ip': '82.118.18.101', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=ua2&type=V2ray': {'region': 'Kyiv, Ukraine', 'host': 'ua2.vpnjantit.com', 'ip': '5.34.182.12', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=uk2&type=V2ray': {'region': 'Bexley, United Kingdom', 'host': 'uk2.vpnjantit.com', 'ip': '57.128.171.79', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=dfr1&type=V2ray': {'region': 'Paris, France', 'host': 'dfr1.vpnjantit.com', 'ip': '51.159.70.15', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=in10&type=V2ray': {'region': 'Artist Village, India', 'host': 'in10.vpnjantit.com', 'ip': '103.248.61.184', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=in13&type=V2ray': {'region': ', India', 'host': 'in13.vpnjantit.com', 'ip': '216.185.57.253', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=in14&type=V2ray': {'region': 'Artist Village, India', 'host': 'in14.vpnjantit.com', 'ip': '103.248.61.101', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=indo&type=V2ray': {'region': 'Paseh, Indonesia', 'host': 'indo.vpnjantit.com', 'ip': '103.77.107.142', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=sau1&type=V2ray': {'region': 'Jeddah, Saudi Arabia', 'host': 'sau1.vpnjantit.com', 'ip': '38.54.61.246', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=sg10&type=V2ray': {'region': 'Singapore, Singapore', 'host': 'sg10.vpnjantit.com', 'ip': '103.231.188.87', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=sg11&type=V2ray': {'region': 'Singapore, Singapore', 'host': 'sg11.vpnjantit.com', 'ip': '8.219.223.204', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=usa2&type=V2ray': {'region': 'Atlanta, USA', 'host': 'usa2.vpnjantit.com', 'ip': '85.239.52.97', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=usa4&type=V2ray': {'region': 'Miami, USA', 'host': 'usa4.vpnjantit.com', 'ip': '5.34.178.157', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=usa7&type=V2ray': {'region': 'Chicago, USA', 'host': 'usa7.vpnjantit.com', 'ip': '195.211.98.34', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=usa8&type=V2ray': {'region': 'Ashburn, USA', 'host': 'usa8.vpnjantit.com', 'ip': '194.213.18.208', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=usa9&type=V2ray': {'region': 'Miami, USA', 'host': 'usa9.vpnjantit.com', 'ip': '50.114.37.34', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=indo8&type=V2ray': {'region': 'Sukabumi, Indonesia', 'host': 'indo8.vpnjantit.com', 'ip': '103.150.191.145', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=indo9&type=V2ray': {'region': 'Jakarta, Indonesia', 'host': 'indo9.vpnjantit.com', 'ip': '103.127.133.66', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=premiuk&type=V2ray': {'region': 'East Grinstead, United Kingdom', 'host': 'premiuk.vpnjantit.com', 'ip': '51.75.170.141', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-premium-account?server=premisg1&type=V2ray': {'region': 'Singapore, Singapore', 'host': 'premisg1.vpnjantit.com', 'ip': '128.199.246.46', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-premium-account?server=premisg3&type=V2ray': {'region': 'Singapore, Singapore', 'host': 'premisg3.vpnjantit.com', 'ip': '66.42.53.216', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-premium-account?server=premisg4&type=V2ray': {'region': 'Singapore, Singapore', 'host': 'premisg4.vpnjantit.com', 'ip': '194.36.179.233', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-premium-account?server=premisg7&type=V2ray': {'region': 'Singapore, Singapore', 'host': 'premisg7.vpnjantit.com', 'ip': '188.166.250.18', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-premium-account?server=premiindo&type=V2ray': {'region': 'Jakarta, Indonesia', 'host': 'premiindo.vpnjantit.com', 'ip': '147.139.145.163', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=premiusa1&type=V2ray': {'region': 'Los Angeles, USA', 'host': 'premiusa1.vpnjantit.com', 'ip': '107.181.187.115', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=premiusa2&type=V2ray': {'region': 'Los Angeles, USA', 'host': 'premiusa2.vpnjantit.com', 'ip': '195.123.242.216', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
    'https://www.vpnjantit.com/create-free-account?server=premiusa3&type=V2ray': {'region': 'Los Angeles, USA', 'host': 'premiusa3.vpnjantit.com', 'ip': '195.123.243.81', 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
}
SP=Server_parser_vpnjantit(server_dict=server_dict)
SP.parse()