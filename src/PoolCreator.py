import os
from functools import partial
from multiprocessing import Pool


class PoolCreator:
    def __init__(self, config, max_processes=os.cpu_count()):
        self.max_processes = max_processes
        self.config = config

    def create_pool_iterator(self, func_name, args):
        func = partial(func_name, self.config)
        # todo: investigate about lock
        return Pool(self.max_processes).imap_unordered(func, args)
