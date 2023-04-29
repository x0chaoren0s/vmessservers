from multiprocessing import Process

from spider.server.server_parser_lionssh import SP_LIONSSH
from spider.server.server_parser_greenssh import SP_GREENSSH
from spider.server.server_parser_sshvpnfree import SP_SSHVPNFREE
from spider.server.server_parser_vpnjantit import SP_VPNJANTIT
from utils.update_subscription import update_subscription

import os

if __name__ == '__main__':
    # spiders = [SP_lionssh,SP_FREEVMESS]
    spiders = [SP_VPNJANTIT,]
    spider_processes = [Process(target=s.parse) for s in spiders]
    [process.start() for process in spider_processes]
    [process.join() for process in spider_processes]

    update_subscription()