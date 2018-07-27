# -*- coding:utf-8 -*-
import redis
from random import choice

MAX_SCORE = 100
MIN_SCORE = 0
#初始分数
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, passwd=REDIS_PASSWORD):
        """
        初始化
        :param host: 地址
        :param port: 端口
        :param passwd: 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=passwd,decode_responses=True)

    def add(self, proxy):
        """
        添加代理，设置分数
        :param proxy: 代理
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, INITIAL_SCORE, proxy)

    def random(self):
        """
        随机获取有效代理,先尝试获取最高分数代理，若不存在，则按排名获取
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                return 'PoolEmptyError'

    def decrease(self, proxy):
        """
        代理不可用时分数减1，分数小于最小值则删除代理
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            #代理分数减1
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            #移除代理
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断数据库中代理是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为最高分数
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用， score设置为:', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取代理数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)