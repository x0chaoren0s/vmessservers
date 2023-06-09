from multiprocessing import Process

from spider.server.server_parser_lionssh import SP_LIONSSH
from spider.server.server_parser_greenssh import SP_GREENSSH
from spider.server.server_parser_sshvpnfree import SP_SSHVPNFREE
from spider.server.server_parser_vpnjantit import SP_VPNJANTIT
from spider.server.server_parser_sshocean import SP_SSHOCEAN
from spider.server.server_parser_freevmess import SP_FREEVMESS
from utils.update_subscription import update_subscription

import os

if __name__ == '__main__':
    spiders = [SP_LIONSSH,SP_GREENSSH,SP_SSHVPNFREE,SP_VPNJANTIT,SP_SSHOCEAN,SP_FREEVMESS]
    spiders = [SP_FREEVMESS,]
    spider_processes = [Process(target=s.parse) for s in spiders]
    [process.start() for process in spider_processes]
    [process.join() for process in spider_processes]

    update_subscription()