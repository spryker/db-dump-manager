import time


class Timer:
    __start_time__ = None
    __stop_time__ = None

    def __init__(self):
        self.start()

    def start(self):
        self.__start_time__ = time.time()

    def stop(self):
        self.__stop_time__ = time.time()

    def get_time_in_seconds(self):
        return "{0:.4f}".format(round(self.__stop_time__ - self.__start_time__, 4))
