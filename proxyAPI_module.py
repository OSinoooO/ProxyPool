# -*- coding:utf-8 -*-
from flask import Flask, g
from Redis_module import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<center><h2>Welcome to OSin\'s Proxy Pool System</h2></center>'

@app.route('/random')
def get_proxy():
    """
    获取随机代理
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_count():
    """
    获取代理池总量
    :return: 代理池总量
    """
    conn = get_conn()
    return '<center><h5>sum(proxy) is:</h5><h3>' + str(conn.count()) + '</h3></center>'

if __name__ == '__main__':
    app.run()