# -*- coding:utf-8 -*-
from Redis_module import RedisClient
from ProxyGet_module import Crawler

#代理池上限
POOL_UPPER_THRESHOLD = 10000

class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断代理池是否达到上限
        :return: 是否达到上限
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        """
        获取代理并存入Redis数据库
        :return:
        """
        print('获取器开始运行...')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)