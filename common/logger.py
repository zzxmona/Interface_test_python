# -*- coding: utf-8 -*-



import logging
import time
# 日志


def logger(logDir):
    log = logging.getLogger(f'{time.time()}')
    # log = logging.getLogger(f'{time.time()}')  # 定义一次就可以，其他地方需要调用logger,只需要直接使用logger就行了
    log.setLevel(level = logging.DEBUG)  # 定义过滤级别
    formatter = logging.Formatter(
        '[%(asctime)s][%(threadName)s][%(module)s][Line:%(lineno)d][%(levelname)s]%(message)s')

    console = logging.StreamHandler()  # 日志信息显示在终端terminal
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    filehandler = logging.FileHandler(fr'{logDir}\log.txt')  # Handler用于将日志记录发送至合适的目的地，如文件、终端等
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)

    log.addHandler(filehandler)
    log.addHandler(console)

    return log