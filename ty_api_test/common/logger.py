#coding=utf-8

import os
import logging
from datetime import *
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, 'logs')
class Log:
    def __init__(self):
        # 1.创建一个logger
        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.DEBUG)
        # 2.创建一个handler，用于写入日志文件
        # fh = logging.FileHandler(self.log_path, encoding="utf-8",mode='w')
        # fh.setLevel(logging.DEBUG)
        # 3.定义handler的输出格式
        formatter = logging.Formatter(self.fmt)
        #fh.setFormatter(formatter)
        # ch.setFormatter(formatter)
        # 4.再创建一个handler，用于输出到控制台
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        # 检查并添加Handler
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

            fh = logging.FileHandler(self.log_path, encoding="utf-8", mode='w')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
        # 5.将logger添加到handler里面
        #self.logger.addHandler(fh)
        #self.logger.addHandler(ch)
    @property
    def log_path(self):
        # logfile1 = datetime.now().strftime("%Y-%m-%d")      #当前时间的格式化输出,注意不要带":",文件名不允许
        logfile1 = datetime.datetime.now().strftime("%Y-%m-%d")
        logpath1 = os.path.join(LOG_PATH,logfile1)
        if not os.path.exists(logpath1):     #按时间建日志文件夹
            os.makedirs(logpath1)
        logfile2 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        logpath2 = os.path.join(logpath1, "{}.log".format(logfile2))
        return logpath2
    @property
    def fmt(self):
        # return '%(levelname)s\t%(asctime)s\t[%(filename)s:%(lineno)d]\t%(message)s'    #日志格式说明，%(asctime)s: 打印日志的时间；
        return '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'    #%(levelname)s: 打印日志级别名称；

    # def debug(self, msg):
    #     """
    #     定义输出的颜色debug--white，info--green，warning/error/critical--red
    #     :param msg: 输出的log文字
    #     :return:
    #     """
    #     self.logger.debug("debug:%s".format(msg))

    # def info(self, msg):
    #     self.logger.info("info:%s".format(msg))
    #
    # def warning(self, msg):
    #     self.logger.warning("warning:%s".format(msg))
    #
    # def error(self, msg):
    #     self.logger.error("error:%s".format(msg))
    #
    # def critical(self, msg):
    #     self.logger.critical("critical:%s".format(msg))
log = Log().logger
if __name__ == '__main__':
    log = Log().logger
    log.info("hello")
    log.debug("bug警告")
    log.debug("22222")
    log.error("XXX")
    #log.info(LOG_PATH)