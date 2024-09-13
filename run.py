from multiprocessing import Process

from spider.server.server_parser_lionssh import SP_LIONSSH
from spider.server.server_parser_greenssh import SP_GREENSSH
from spider.server.server_parser_sshvpnfree import SP_SSHVPNFREE
from spider.server.server_parser_vpnjantit import SP_VPNJANTIT, Server_parser_vpnjantit
from spider.server.server_parser_sshocean import SP_SSHOCEAN
from spider.server.server_parser_freevmess import SP_FREEVMESS
from spider.server.server_parser_akunssh import SP_AKUNSSH
from spider.server.server_parser_freevpn import SP_FREEVPN

import os,time

if __name__ == '__main__':
    # SP_GREENSSH 的网站和服务器的ip似乎都不通
    spiders = [
        Server_parser_vpnjantit(server_dict={
            'https://www.vpnjantit.com/create-free-account?server=hk1&type=V2ray': {'region': 'Hong Kong, Hong Kong', 'host': 'hk1.vpnjantit.com', 'ip': '8.218.127.229', 'use_ip': False, 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
            'https://www.vpnjantit.com/create-free-account?server=hk2&type=V2ray': {'region': 'Hong Kong, Hong Kong', 'host': 'hk2.vpnjantit.com', 'ip': '8.218.64.170', 'use_ip': False, 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
            'https://www.vpnjantit.com/create-free-account?server=hk3&type=V2ray': {'region': 'Hong Kong, Hong Kong', 'host': 'hk3.vpnjantit.com', 'ip': '8.217.100.15', 'use_ip': False, 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
            'https://www.vpnjantit.com/create-free-account?server=premihk1&type=V2ray': {'region': 'Hong Kong, Hong Kong', 'host': 'premihk1.vpnjantit.com', 'ip': '8.217.135.42', 'use_ip': False, 'port': 10000, 'Referer': 'https://www.vpnjantit.com/free-v2ray-vmess-7-days'},
        })
    ]
    # spiders = [SP_GREENSSH,SP_VPNJANTIT,SP_SSHOCEAN,SP_FREEVMESS,SP_AKUNSSH]
    # spiders = [SP_VPNJANTIT,SP_SSHOCEAN,SP_GREENSSH,SP_FREEVMESS]
    # spiders = [SP_LIONSSH,SP_GREENSSH,SP_SSHVPNFREE,SP_SSHOCEAN,SP_FREEVMESS]
    # spiders = [SP_FREEVPN]
    # spiders = [SP_LIONSSH,]
    # spiders = [SP_AKUNSSH]
    # spiders = [SP_GREENSSH,SP_VPNJANTIT,SP_FREEVMESS,SP_AKUNSSH]
    spider_processes = [Process(target=s.run) for s in spiders]
    [process.start() for process in spider_processes]
    # for process in spider_processes:
    #     process.start()
    #     time.sleep(10)
    [process.join() for process in spider_processes]
    # SP_FREEVPN.run()

    # if os.environ.get('MODE', 'RELEASE')=='DEBUG':
    #     from utils.update_subscription import update_subscription
    #     from utils.update_git import update_git
        # update_subscription()
        # update_git()
