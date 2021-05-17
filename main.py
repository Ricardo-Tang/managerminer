from requests_html import HTMLSession
import datetime
url=r"https://ezil.me/personal_stats?wallet=0xa66dba8f536756ce2a63d07c9660d85203947af7.zil1kysx4evfu8rz42wy088cjega2x92a8s6vfx9yc&coin=eth"

workurl = r"https://stats.ezil.me/current_stats/0xa66dba8f536756ce2a63d07c9660d85203947af7.zil1kysx4evfu8rz42wy088cjega2x92a8s6vfx9yc/workers"
detailurl = r"https://stats.ezil.me/historical_stats/0xa66dba8f536756ce2a63d07c9660d85203947af7.zil1kysx4evfu8rz42wy088cjega2x92a8s6vfx9yc/{}?time_from={}&time_to={}"
session=HTMLSession()


def getworker():
    info=session.get(workurl).json()
    workers=[]
    for e in info:
        workers.append(e['worker'])
    return workers


def createtime():
    a = datetime.datetime.today()
    o1 = datetime.timedelta(hours=-8)
    o2 = datetime.timedelta(days=-1,hours=-8)
    return [(a+o2).strftime("%Y-%m-%dT%H:%M:%SZ"), (a+o1).strftime("%Y-%m-%dT%H:%M:%SZ")]

def infourl(worker):
    t = createtime()
    return detailurl.format(worker,t[0],t[1])

def getworkerinfo(worker):
    workerinfo = session.get(detailurl.format(
        worker, "2021-05-15T03:00:00Z", "2021-05-16T03:00:00Z")).json()
    short = sum([e['short_average_hashrate']
                for e in workerinfo])/len(workerinfo)
    reported = sum([e['reported_hashrate']
                    for e in workerinfo])/len(workerinfo)
    print("{} {}".format(worker,len(workerinfo)))
    return short,reported


if __name__ == "__main__":
    workers = getworker()
    workers.append('zmc_home')
    infos = []
    for eworker in workers:
        info={}
        info['worker']=eworker
        info['short'],info['reported']=getworkerinfo(eworker)
        print(info)
        info['shorts']=info['short']/(10**6)
        info['reporteds']=info['reported']/(10**6)
        infos.append(info)
    short=sum([e['short'] for e in infos])
    reported = sum([e['reported'] for e in infos])
    for einfo in infos:
        print(einfo)

    with open("result-0516.txt","w") as f:
        for einfo in infos:
            f.write("{}\t{:.1f}\t{:.1f}\t\n".format(einfo['worker'],einfo['shorts'],einfo['reporteds']))