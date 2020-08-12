import sys
import multiprocessing
import warnings

if sys.platform != 'win32':
    multiprocessing.set_start_method('fork')


class CommonPool(object):
    def map(self, func, args):
        return list(map(func, args))


class AutoPool(object):
    def __init__(self, mode, processes):

        if mode == 'multiprocessing' and sys.platform == 'win32':
            warnings.warn('multiprocessing not support in windows, turning to multithreading')
            mode = 'multithreading'

        self.mode = mode
        self.processes = processes

        if mode == 'vectorization':
            pass
        elif mode == 'cached':
            pass
        elif mode == 'multithreading':
            from multiprocessing.dummy import Pool as ThreadPool
            self.pool = ThreadPool(processes=processes)
        elif mode == 'multiprocessing':
            from multiprocessing import Pool
            self.pool = Pool(processes=processes)
        else:  # common
            self.pool = CommonPool()

    def map(self, func, args):
        return self.pool.map(func, args)
