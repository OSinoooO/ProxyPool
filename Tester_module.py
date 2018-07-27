# -*- coding:utf-8 -*-
import aiohttp, asyncio, time
from Redis_module import RedisClient
from aiohttp.client_exceptions import ClientConnectionError, ClientError
from asyncio import TimeoutError

#期望响应状态码
VALID_STATUS_CODE = [200]
#测试目标网址
TEST_URL = 'http://www.baidu.com'
#每次异步测试的代理数
BATCH_TEST_SIZE = 100

class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self,proxy):
        """
        测试单个代理
        :param proxy:单个代理
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODE:
                        self.redis.max(proxy)
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应吗不合法', proxy)
            except (ClientError, ClientConnectionError, TimeoutError):
                self.redis.decrease(proxy)
                print('代理请求失败...')

    def run(self):
        """
        测试器主函数
        :return:
        """
        print('测试器开始运行...')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i+BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(1)
        except Exception as e:
            print('测试器发生错误...', e.args)
