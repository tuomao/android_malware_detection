# coding: utf-8
__author__ = 'tuomao'
from bs4 import  BeautifulSoup
import urllib2
import gzip
import StringIO
import torndb
import re
import multiprocessing

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '__cfduid=d723462f94bd7bba89c61f0ec1aa62b3d1464167804; _ga=GA1.2.557160409.1464167810; __atuvc=44%7C21; __atuvs=5747f336fb6d92b8000',
    'Host': 'apk-dl.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
}
data = None
apk_urls=[]

db = torndb.Connection("120.27.92.166","apk1",user="root",password="112112")


def insert(url, name, developer, rate, package, category):
    sql = "INSERT INTO apk(url, name, developer, rate, package, category) VALUES (%s,%s,%s,%s,%s,%s)"
    if url[0] != 'h':
        url = 'http:'+url.strip()
    try:
        db.insert(sql,url.encode('UTF-8'), name, developer,float(rate), package, category.encode('UTF-8'))
    except Exception as e:
        print(e)

def getdoc(url):
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    doc = response.read()
    doc = StringIO.StringIO(doc)
    gziper = gzip.GzipFile(fileobj=doc)
    return gziper.read()


def extract_apps_from_category(category, url):
    try:
        soup = BeautifulSoup(getdoc(url),"html5lib")
        apps = soup.find(attrs={'class':'items'}).find_all('a')
        for app in apps:
            tag = app.find(attrs={'class': 'price-container'})
            if tag.string.strip() == 'Free':
                url = app['href'].encode('UTF-8')
                if re.search(ur"[^\u0000-\u007F]+",url.decode('utf8')) == None:
                    rate = app.find(attrs={'class':'current-rating'})['style'][-4:-2]
                    rate = float(rate) / 20
                    if rate >= 3:
                        get_apk(url, category,rate)
    except Exception as e:
        print e


def get_apk(url, category, rate):
    global conn
    try:
        soup = BeautifulSoup(getdoc('http:'+url), "html5lib")
        apk_info = soup.find("div", class_="info").find_all('div')
        name = apk_info[1].contents[-1]
        pacname = apk_info[2].contents[-1]
        developer = apk_info[4].contents[2].string
        url = soup.find("a", class_="download")['href']
        soup = BeautifulSoup(getdoc('http:'+url.strip()),"html5lib")
        apk_url = soup.find_all('p')[1].find('a')['href']
        print(apk_url)
        insert(apk_url, name, developer, rate, pacname, category)
    except Exception as e:
       print(e)

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=8)
    progress = multiprocessing.Process()
    progress.start()
    print "start!!!"
    categorys = db.query("select * from category")
    for category in categorys:
        for currentPage in range(category['page'],50):
            cate_url = '%s?page=%d' % (category['url'],currentPage)
            print(cate_url)
            pool.apply(extract_apps_from_category, (category['name'],cate_url))
            db.update("update category SET page = %s WHERE name = %s",currentPage+1,category['name'])
    pool.close()
    progress.terminate()
    progress.join()
    pool.join()