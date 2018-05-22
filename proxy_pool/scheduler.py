import time
import asyncio, aiohttp
import logging; logging.basicConfig(level=logging.INFO)
import re

from .settings import *
from .db import RedisClient
from .getter import ProxyGetter

from multiprocessing import Process

from asyncio import TimeoutError
try:
    from aiohttp.errors import ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError

from aiohttp.client_exceptions import ClientOSError


class Scheduler(object):
    # start: 启动方法
    # check_pool: 检查数据库中代理数量
    # test_handler: 从数据库中取出一半的代理进行测试
    # start_crawl: 调用抓取函数，并将结果传递给测试函数
    # start_test: 异步测试启动函数
    # test_proxy: 测试每个代理是否可用
    # 所用到的常量全部都定义在 settings 当中

    def __init__(self):
        # 初始化数据库删除上次的残留 初始化一个抓取对象
        self._conn = RedisClient()
        self._conn.flush()
        self.getter = ProxyGetter()

    def start(self):
        check_process = Process(target=self.check_pool)
        tester_process = Process(target=self.test_handler)
        check_process.start()
        tester_process.start()

    def check_pool(self):
        # 当代理池数量小于50就开始抓取
        while True:
            if self._conn.len_queue() < 50:
                self.start_crawl()
            else:
                logging.info('sleep 10 s')
                time.sleep(POOL_LEN_CHECK_CYCLE)

    def test_handler(self):
        # 只要有数据库不为空就取出一半的代理进行检查
        while True:
            count = self._conn.len_queue() // 2
            if count > 10:
                logging.info('Waiting for adding')
                time.sleep(VALID_CHECK_CYCLE)
                continue
            proxy_list = self._conn.get_half_proxy(count)
            self.start_test(proxy_list)
            logging.info('sleep 30 s')
            time.sleep(VALID_CHECK_CYCLE)

    def start_crawl(self):
        # 调用抓取函数 返回None表示抓取失败

        proxy_list = self.getter.get_proxy()
        if proxy_list:
            self.start_test(proxy_list)
        else:
            logging.info('sleep 10 s')
            time.sleep(10)
            self.start_crawl()

    def start_test(self, proxy_list):
        # 异步测试

        logging.info('Start Testing')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_proxy(proxy) for proxy in proxy_list]
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            logging.info('Async Error')

    async def test_proxy(self, proxy):
        try:
            async with aiohttp.ClientSession() as s:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    headers = {
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
                    }
                    logging.info('Testing %s' %proxy)
                    async with s.get(TEST_API, proxy=real_proxy, timeout=TIMEOUT, headers=headers) as response:
                        if response.status == 200:
                            ip_addr = await response.text()
                            ip_address = re.match(r'.*?:(.*?),address.*?', ip_addr).group(1)
                            if ip_address != "本机的ip":
                                logging.info('Put The Valid Proxy %s in redis' %proxy)
                                self._conn.put_proxy(proxy)
                except(ProxyConnectionError, TimeoutError, ValueError):
                    logging.info('Invalid Proxy %s' %proxy)
        except (ServerDisconnectedError, ClientResponseError,ClientConnectorError, ClientOSError) as e:
            logging.info('Aiohttp ClientSession Error')






