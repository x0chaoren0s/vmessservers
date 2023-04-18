from multiprocessing import Process

from spider.server.server_parser_lionssh import SP_LIONSSH
from spider.server.server_parser_greenssh import SP_GREENSSH

if __name__ == '__main__':
    # spiders = [SP_lionssh,SP_FREEVMESS]
    spiders = [SP_LIONSSH,]
    spider_processes = [Process(target=s.parse) for s in spiders]
    [process.start() for process in spider_processes]
    [process.join() for process in spider_processes]