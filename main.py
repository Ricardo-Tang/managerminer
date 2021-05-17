import yaml
import os
from requests_html import  HTMLSession
import datetime

config=""
session=HTMLSession()
# path os.path.join(os.path.abspath("."),"config.yml")
def init():
    short=os.path.join(os.path.abspath("."), "short")
    reported = os.path.join(os.path.abspath("."), "reported")
    if os.path.exists(short)==False:
        os.mkdir(short)
    if os.path.exists(reported) == False:
        os.mkdir(reported)
    

def loadConfig(path):
    fs = open(path, encoding="utf-8")
    return yaml.load(fs)

def getdetailurl(worker):
    t = getDate()
    return config["url"]["info"].format(eth=config["wallet"]["eth"],zil=config["wallet"]["zil"],worker=worker,fromtime=t[0],totime=t[1])
def getinfo(worker):
    workerinfo=session.get(getdetailurl(worker)).json()
    short=0
    reported=0
    if len(workerinfo)==0:
        short = 0
        reported = 0
    else:
        short = sum([e['short_average_hashrate'] for e in workerinfo])/len(workerinfo)
        reported = sum([e['reported_hashrate'] for e in workerinfo])/len(workerinfo)
    return short/(10**6), reported/(10**6)

def getDate():
    a = datetime.date.today()
    a = datetime.datetime(a.year,a.month,a.day,11,0,0)
    o1 = datetime.timedelta(hours=-8)
    o2 = datetime.timedelta(days=-1, hours=-8)
    return [(a+o2).strftime("%Y-%m-%dT%H:%M:%SZ"), (a+o1).strftime("%Y-%m-%dT%H:%M:%SZ")]


def outshort(infos):
    with open("./short/{}.csv".format(datetime.date.today().strftime("%Y-%m-%d")),"w") as f:
        for e in infos:
            f.write("{},,".format(e['worker']))
        f.write("\n")
        for e in infos:
            f.write("{:.1f},,".format(e['short']))
        f.write("\n")


def outreported(infos):
    with open("./reported/{}.csv".format(datetime.date.today().strftime("%Y-%m-%d")), "w") as f:
        for e in infos:
            f.write("{},,".format(e['worker']))
        f.write("\n")
        for e in infos:
            f.write("{:.1f},,".format(e['reported']))
        f.write("\n")

if __name__=="__main__":
    init()
    config = loadConfig(os.path.join(os.path.abspath("."), "config.yml"))
    infos=[]
    for e in config['worker']:
        info = {}
        info['worker'] = e
        info['short'],info['reported']=getinfo(e)
        infos.append(info)
    outreported(infos)
    outshort(infos)

