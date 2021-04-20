import requests
import re
import time
import pymysql


class TaobaoSpider(object):
    """淘宝爬虫"""
    def __init__(self):
        self.url = 'https://s.taobao.com/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210410&ie=utf8&bcoffset=6&ntoffset=6&p4ppushleft=1%2C48&cps=yes&ppath=&s={}'
        # headers 从浏览器抓包获取
        self.headers = {
            "Host": "s.taobao.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cookie": "tfstk=cgq5BwNerAcVcgKep862Yi3wmJnhaUKjnnc4FPwcG0EytOeSwsYebfZEiYOjymDf.; cna=o0LvEowS1WgCAXzPwBKL2gva; isg=BLW1YyWTOQYH6F2meFNo6SFGxzhvMmlEZj2OfTfaVix1DtQA_4BHFeDMXFI4VYH8; l=eBINfn6mjyAptZnCBOfaKurza77tRIObYuPzaNbMiOCPON1epvmOW6a2UEYwCn1VnsaJR3o9oLLyBST_Ny4oh2nk8b8CgsDKJdTh.; _samesite_flag_=true; cookie2=18456445a2517a2205765ebb068fd03e; t=698f61158634be52b95bb03000775b81; _tb_token_=5efebb1613ee; _m_h5_tk=c5955a7f4715137d251f0c15ff2f5848_1618074767365; _m_h5_tk_enc=fc4aa7d8825e8dfafaf4c1982e70ec0f; sgcookie=E100EsMa42f1rWZ7J5g39bjARTk6mtZCb0KEiFw3y7ZQ8DLFGsuk8w6T%2B%2BKDduur71HJyzH47PaP6UmqWlSGK2CuvA%3D%3D; uc1=pas=0&cookie21=URm48syIYB3rzvI4Dim4&cookie14=Uoe1iuBwyX7m3A%3D%3D&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dCuwufJbg5hSPyytw%3D&nk2=F5RBxrOyvBHiKg%3D%3D&id2=UoewBV9a9Qhh%2Bw%3D%3D; csg=84f24a68; lgc=tb43505355; dnk=tb43505355; skt=a9d1141f8d62e2eb; existShop=MTYxODA2NjAzNg%3D%3D; uc4=id4=0%40UO%2B2vm6kj0CuLbAddkVDSPGi0mnK&nk4=0%40FY4Ko%2BZKbiLLgdDTsuuIVL22mSje; tracknick=tb43505355; _cc_=U%2BGCWk%2F7og%3D%3D; mt=ci=38_1; thw=cn; enc=LcuIfJVzy%2BizuYQkrf2lzaBvgYW%2BaVgaW1P9GJYlE3vHMSbGtfYi18z%2FYgMFjMJeRz8smVeRNixd0k3kvLVcWQ%3D%3D; _uab_collina=161798660359450799922121; JSESSIONID=0C01AEC615AB8CADD72FE3AAA51CD8A7; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; hng=CN%7Czh-CN%7CCNY%7C156; v=0; unb=1645392803; cookie17=UoewBV9a9Qhh%2Bw%3D%3D; _l_g_=Ug%3D%3D; sg=53d; _nk_=tb43505355; cookie1=W5tX1qKTbJUtrGyLHXakEu64CEsETeUkT%2BrBxngGFI0%3D; xlly_s=1; x5sec=7b227365617263686170703b32223a223635616664623761623432316261376266356639356630303535393137616134434d5449796f4d47454b724b75507278387465377a414561444445324e44557a4f5449344d444d374d54436e68594b652f502f2f2f2f3842227d",
            "Upgrade-Insecure-Requests": "1",
            "TE": "Trailers"
        }
        self.p = 0
        self.db = pymysql.connect(
            host='127.0.0.1', user='***', password='***', database='taobao', charset='utf8'
        )  # 使用自己用户名和密码
        self.corsur = self.db.cursor()

    # 获取页面
    def get_page(self, url):
        html = requests.get(url=url, headers=self.headers).text
        # print(html)
        self.parse_page(html)

    # 解析数据
    def parse_page(self, html):
        bds = r'"raw_title":"(.*?)",".*?detail_url":"(.*?)","view_price":"(.*?)","view_fee.*?item_loc":"(.*?)","view_sales":"(.*?)","comment_count"'
        ins = 'insert into bratable1 VALUES (%s,%s,%s,%s,%s)'
        pattern = re.compile(bds, re.S)
        r_list = pattern.findall(html)
        L = []
        for r in r_list:
            L.append(r)
            print(r)  # ('内衣套装女性感文胸调整型侧收小胸上托聚拢', '98.00', '广东 广州', '1.5万+人付款')
        # 休眠５秒防止被封
        self.corsur.executemany(ins, L)
        self.db.commit()
        time.sleep(5)

    def main(self):
        key = input('请输入要搜索的商品：')
        # 　拼接url
        for page in range(0, 44, 44):
            self.p += 1
            url = self.url.format(key, page)
            self.get_page(url=url)
            print('第%s页完成' % self.p)
        self.corsur.close()
        self.db.close()


if __name__ == '__main__':
    spider = TaobaoSpider()
    spider.main()
