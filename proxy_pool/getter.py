import re 
import logging; logging.basicConfig(level=logging.INFO)

from .utils import get_page


class ProxyMetaclass(type):

    def __new__(cls, name, bases, attrs):
        attrs['__Crawlfunc__'] = []
        for k in attrs.keys():
            if k.startswith('crawl_'):
                attrs['__Crawlfunc__'].append(k)
        return type.__new__(cls, name, bases, attrs)


class ProxyGetter(object, metaclass=ProxyMetaclass):

    def get_proxy(self):
        # 调用自身的每个抓取函数
        # proxy_list = []
        # for callback in self.__Crawlfunc__:
        # proxy_list += eval("self.{}()".format(callback))
        proxy_list = self.crawl_daili66()
        return proxy_list

    def crawl_daili66(self):
        url = ''
        html = get_page(url)
        if html:
            proxy_list = []
            r = r'>\s*([\d.:]*?)\s*?<br'
            re_comlile = re.compile(r, re.S)
            for ip_adress in re_comlile.findall(html):
                proxy_list.append(ip_adress.strip())
            return proxy_list

    # 这些代理几乎都不能用～！
    # def crawl_data5u(self):
    #     url = 'http://www.data5u.com/free/gngn/index.shtml'
    #     html = get_page(url)
    #     if html:
    #         proxy_list = []
    #         r = r'<ul class="l2">\s*<span><li>(.*?)</li></span>\s*'
    #         r += '<span .*?"><li .*?>(.*?)</li></span>'
    #         r += '.*?<li>(\d).*?</li></span>'
    #         r += '\s*<span style="border:none; width: 190px;">'
    #         re_comlile = re.compile(r, re.S)
    #         ip_adress_list = re_comlile.findall(html)
    #         for adress, port, speed in ip_adress_list:
    #             if int(speed) <= 5:
    #                 result = adress + ':' + port
    #                 proxy_list.append(result.strip())
    #         return proxy_list


    # def crawl_kuaidaili(self):
    #     url = 'https://www.kuaidaili.com/free/inha/{}/'.fromat(random.randrange(1000))
    #     html = get_page(url)
    #     if html:
    #         proxy_list = []
    #         r = r'<td data-title="IP">([\d.]+?)</td>\s*'
    #         r += '<td data-title="PORT">(\d+)</td>'
    #         re_compile = re.compile(r, re.S)
    #         for ip, port in re_comlile.findall(html):
    #             result = ':'.join([ip, port])
    #             proxy_list.append(result.strip())
    #         return proxy_list

    # def crawl_xicidaili(self):
    #     url = 'http://www.xicidaili.com/nn/40'
    #     html = get_page(url)
    #     if html:
    #         proxy_list = []
    #         r = r'<td>([\d.]+?)</td>\s*'
    #         r += '<td>(\d+)</td>.*?'
    #         r += '<td>([HTPS]+?)</td>'
    #         re_compile = re.compile(r, re.S)
    #         for ip, port, protocol in re_compile.findall(html):
    #             if protocol == 'HTTP':
    #                 result = ":".join([ip, port])
    #                 proxy_list.append(result.strip())
    #         return proxy_list
