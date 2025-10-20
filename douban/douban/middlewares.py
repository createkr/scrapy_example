# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

import scrapy
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.http import HtmlResponse

import requests
from fake_useragent import UserAgent
from selenium import webdriver


class RandomUserAgentMiddleware:
    def process_request(self, request, spider):
        ua = UserAgent().chrome
        request.headers['User-Agent'] = ua
        print(f"代理使用的agent: {ua}")
class RandomProxyMiddleware:
    def __init__(self):
        #积流代理
        self.appid = "ohku1sj758jjovy6vvjt"
        self.secret = "kzccqwggomrdfyb36dr5nq42xts9jj7y"
        self.jiliuApi="https://api.jiliuip.com/getdip"
        self.jiliuValidApi = "https://api.jiliuip.com/getiptime"
        self.authUser = "jd2233199184"
        self.authPass = "xynwyqea"
        self.proxy_ip = ""

    def process_request(self, request, spider):
        # 设置代理    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
        if self.proxy_ip != "":
            time = self.check_ip_valid(self.proxy_ip)
            if time is not None and time >=10:
                request.meta['proxy'] = f'https://%s:%s@%s' % (self.authUser, self.authPass, self.proxy_ip)
                print(f"代理的ip: {self.proxy_ip } ")
            else:
                ip = self.get_proxy_ip()
                request.meta['proxy'] = f'https://%s:%s@%s' % (self.authUser, self.authPass, ip)
                self.proxy_ip = ip
                print(f"代理的ip: {self.proxy_ip } ")
        else:
            ip = self.get_proxy_ip()
            request.meta['proxy'] = f'https://%s:%s@%s' % (self.authUser, self.authPass, ip)
            self.proxy_ip = ip
            print(f"代理的ip: {self.proxy_ip} ")
    def get_proxy_ip(self):
        try:
            proxy_url = self.jiliuApi + "?app_id=" + self.appid + "&app_secret=" + self.secret + "&num=1"
            ip = requests.get(proxy_url).text
            return  ip
        except Exception as e:
            print(e)
            return  None

    def check_ip_valid(self,proxy):
        try:
            res = requests.get(self.jiliuValidApi + "?app_id=" + self.appid + "&app_secret=" + self.secret + "&proxy=" + proxy).json()
            return res['data'][proxy]
        except Exception as e:
            print(e)
            return  None

#  使用selenium 进行动态渲染

class SeleniumMiddleware:


    def process_request(self,request,spider):


        url = request.url
        #  当某个url 需要动态加载的时候就是用的selenium
        if 'daydata' in url:
            driver = webdriver.Chrome()
            driver.get( url)
            time.sleep(3)
            data = driver.page_source
            driver.close()
#              创建响应式对象
            res = HtmlResponse(url=url,body=data,encoding='utf-8',request=request)
            return  res









# if __name__ == '__main__':
#     proxy = RandomProxyMiddleware()
#     # ip = proxy.get_proxy_ip()
#     # print(ip)
#     time = proxy.check_ip_valid("58.19.54.142:20019")
#     print(time)
