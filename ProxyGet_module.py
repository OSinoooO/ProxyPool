# -*- coding:utf-8 -*-
import requests, re
from pyquery import PyQuery

class ProxyMetaClass(type):
    """
    借助元类实现获取所有以'crawl_'开头的方法名称
    可以灵活添加代理网站
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        #获取方法名，attrs键名对应方法名
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=ProxyMetaClass):
    def get_proxies(self, callback):
        """
        遍历每个获取代理的方法
        :param callback: 方法名
        :return: 代理池
        """
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('成功获取代理：', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_66ip(self):
        """
        从66ip上获取高匿名代理API接口
        :return: 高匿名代理
        """
        url = 'http://www.66ip.cn/nmtq.php?'
        headers = {
            'Host': 'www.66ip.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
        }
        params = {
            #该网站免费上限为300个
            'getnum': '300',
            'isp': '0',
            #0到4分别对应：0-不限匿名性；1-透明代理；2-普通代理；3-高匿代理；4-超匿代理
            'anonymoustype':'4',
            'area':'0',
            'proxytype':'2',
            'api':'66ip'
        }
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            proxis_trs = re.findall('var mediav_ad_height.*?</script>(.*?)</div>', response.text, re.S)
            trs = re.findall('\s+(.*?)<br />', proxis_trs[0], re.S)
            for tr in trs:
                yield tr.strip()
        except TimeoutError:
            print('页面加载出错...')
            return self.crawl_66ip()

    def crawl_xicidaili(self):
        """
        西刺代理API获取
        :return: 国内高匿代理
        """
        page_count = 4
        headers = {
            'Host': 'www.xicidaili.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
        }
        start_url = 'http://www.xicidaili.com/nn/{}'
        for url in (start_url.format(page) for page in range(1, page_count+1)):
            try:
                html = requests.get(url, headers=headers, timeout=10).text
                doc = PyQuery(html)
                proxies_trs = doc.find('#ip_list tr').items()
                for tr in proxies_trs:
                    if tr.find('td:nth-child(2)'):
                        proxy = tr.find('td:nth-child(2)').text()+':'+tr.find('td:nth-child(3)').text()
                        yield proxy
            except TimeoutError:
                print('页面加载出错...')

    def crawl_swei360(self):
        """
        三维360代理获取   ！！！该网站网速较慢(╯﹏╰)！！！
        :return: 高匿代理
        """
        start_url = 'http://www.swei360.com/free/?page='
        headers = {
            'Host': 'www.swei360.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
        }
        #获取最大页数
        try:
            response = requests.get(start_url+'1', headers=headers, timeout=10)
            doc = PyQuery(response.text)
            doc = doc.find('#listnav > ul > strong')
            page_count = re.findall('</font>/(.*?)</strong>', str(doc), re.S)
        except TimeoutError:
            return self.crawl_swei360()

        for url in (start_url + str(i) for i in range(1, int(page_count[0])+1)):
            try:
                doc = PyQuery(requests.get(url, headers=headers, timeout=10).text)
                trs = doc.find('#list > table > tbody > tr').items()
                for tr in trs:
                    proxy = tr.find('td:nth-child(1)').text() + ':' + tr.find('td:nth-child(2)').text()
                    yield proxy
            except TimeoutError:
                print('页面加载出错...')
