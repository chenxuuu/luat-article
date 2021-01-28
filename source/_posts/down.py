#coding:utf-8
import time
import os
import sys
import json
import urllib
import urllib.request
import re
import shutil
from multiprocessing.dummy import Pool as ThreadPool

#设置UA，防止屏蔽
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; rv:60.0) Gecko/20100101 Firefox/60.0')]
urllib.request.install_opener(opener)

def get(i):
    try:
        print("loading..."+str(i))
        url = "https://doc.openluat.com/api/site/article?id="+str(i)
        html = urllib.request.urlopen(url,timeout=5).read().decode('utf-8')
        info = json.loads(html)
        if info["code"] != 0:
            print("no article")
            return
        title = info["data"]["title"].replace("\"", "\\\"")
        time_local = time.localtime(info["data"]["publish_at"])
        publish_time = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        url = "http://doc.openluat.com/api/site/text?id="+str(info["data"]["text_id"])
        html = urllib.request.urlopen(url,timeout=5).read().decode('utf-8')
        info = json.loads(html)
        if info["code"] != 0:
            print("no article")
            return
        text = info["data"]["content"].replace("\r", "").replace("{{", "{ {").replace("}}", "} }")
        text = re.sub('http://doc.openluat.com/article/(.+?)/0',
                lambda x: "https://doc.luatos.wiki/{}".format(x.group(1)),
                text)
        md = open(str(i)+".md", "w",encoding='utf-8')
        md.write("---\n")
        md.write("title: \""+title+"\"\n")
        md.write("date: "+publish_time+"\n")
        md.write("---\n\n")
        md.write(text)
        md.close()
    except Exception as e:
        print(i)
        print(e)


items = list(range(0,2421))
pool = ThreadPool(100)
pool.map(get, items)
pool.close()
pool.join()
