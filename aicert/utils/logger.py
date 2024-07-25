#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ZJUICSR'
__copyright__ = 'Copyright © 2024/07/22'


import logging
from logging import handlers
from logging.handlers import RotatingFileHandler

class Logger:
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self):
        self.__loggers = {}

    def add_logger(self, stid,
                   filename,
                   level='info',
                   when='D',
                   backCount=3,
                   # fmt='%(asctime)s [%(levelname)s] %(filename)-12s %(funcName)-24s Line: %(lineno)-6s Msg: %(message)s'
                   fmt='%(asctime)s [%(levelname)s]  Msg: %(message)s'):
        if stid not in self.__loggers.keys():
            logger = logging.getLogger(stid)
            format_str = logging.Formatter(fmt)  # 设置日志格式
            sh = logging.StreamHandler()  # 往屏幕上输出
            sh.setFormatter(format_str)  # 设置屏幕上显示的格式
            th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                                   encoding='utf-8')
            th.setFormatter(format_str)  # 设置文件里写入的格式
            logger.setLevel(self.level_relations.get(level))  # 设置日志级别
            logger.addHandler(sh)
            logger.addHandler(th)
            self.__loggers.update({stid: logger})
        else:
            logger = self.__loggers[stid]
        return logger

    def get_sub_logger(self, stid):
        if stid not in self.__loggers.keys():
            return -1
        return self.__loggers[stid]

    def del_logger(self, stid):
        del self.__loggers[stid]
        return 1

    def info(self, stid, msg):
        return self.__loggers[stid].info(msg)
        # return self.logger.info(msg)
