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

def down(info):
    while True:
        try:
            id = str(info["id"])
            url = "http://doc.openluat.com/api/site/text?id="+str(info["text_id"])
            html = urllib.request.urlopen(url,timeout=30).read().decode('utf-8')
            j = json.loads(html)
            text = "\n"+j["data"]["content"]
            text = text.replace("\n# ","\n## ")
            text = re.sub('http://doc.openluat.com/article/(\\d+)/0',
                lambda x: "https://doc.luatos.wiki/{}/".format(x.group(1)),
                text)
            text = re.sub('http://doc.openluat.com/wiki/6\\?wiki_page_id=(\\d+)',
                lambda x: "https://doc.luatos.wiki/wiki/pages/{}.html".format(x.group(1)),
                text)
            text = re.sub('\n(# +.+)',
                lambda x: "\n\n{}\n".format(x.group(1)),
                text)
            md = open("pages/"+id+".md", "w",encoding='utf-8')
            md.write("# "+info["title"].replace("-"," ").replace("#"," ")+"\n\n")
            md.write(text)
            md.close()
            os.system("pandoc -o pages/"+id+".rst pages/"+id+".md")
            os.remove("pages/"+id+".md")
            print("download done "+str(id))
            break
        except:
            pass

url = "http://doc.openluat.com/api/site/wiki_page?wiki_id=6"
html = urllib.request.urlopen(url,timeout=30).read().decode('utf-8')
info = json.loads(html)

try:
    shutil.rmtree("pages/")
    os.mkdir("pages/")
except:
    pass
try:
    os.remove("index.rst")
except:
    pass

doc = open("pages/0.rst", "a+",encoding='utf-8')
doc.write("Luat模块应用手册\n")
doc.write("================\n\n")
doc.write("\n")
doc.close()


pool = ThreadPool(100)
pool.map(down, info["data"])
pool.close()
pool.join()

docs = []
for i in info["data"]:
    id = i["hook_id"]
    if not docs.__contains__(id):
        docs.append(id)
        doc = open("pages/"+str(id)+".rst", "a+",encoding='utf-8')
        doc.write("\n.. toctree::\n")
        doc.write("    :hidden:\n")
        doc.write("\n")
        doc.close()
    head = "    "
    if id == 0:
        head = "    pages/"
    doc = open("pages/"+str(id)+".rst", "a+",encoding='utf-8')
    doc.write(head+str(i["id"])+"\n")
    doc.close()
    print("toctree done "+str(i["id"]))

shutil.move("pages/0.rst", "index.rst")
