import requests
import json
import time
import threading

'''
startline:1623240000  报名开始时间
status:1      活动状态
eventStatus:4 活动状态，4表示进行中，5表示已结束
流程：
1.脚本每十分钟搜索一次研究生学术
2.筛选未开始报名的活动（startline时间戳>现行时间戳）
3.将该活动加入排队报名列表
4.每隔200ms计算一次与startline的时间间隔
5.当时间差为负数时执行一次活动报名，记录下结果并推送到微信
6.删除这条任务
更新日期：2021年6月11日
使用方法：
1.用ios登录PU
2.进行一次关键词搜索并抓包
3.进行一次活动报名并抓包
3.根据URL找的相应的包名，替换掉cookie和content-type以及body部分
4.需要微信推送的话，修改pushplus_submit里的token部分
'''
submit_list = [] #这是即将申请的活动数组
threads = [] #这是用于并发的线程数组
def pu_search(keywords):
    url = 'https://pocketuni.net/?app=api&mod=Event&act=newEventList'

    head = {'Cookie': '***********************************************',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Content-Type': 'multipart/form-data; boundary=Boundary+*************',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'pocketuni.net',
            'User-Agent': 'client:iOS version:6.8.70 Product:iPhone OsVersion:14.6',
            'version': '6.8.70',
            'Content-Length': '444',
            'Accept-Language': 'zh-Hans-CN;q=1'
            }
    body = '''--Boundary+*************
Content-Disposition: form-data; name="keyword"

''' + keywords + '''
--Boundary+*************
Content-Disposition: form-data; name="oauth_token"

588e2d37a7d45d1ac3f4638a25e5083c
--Boundary+*************
Content-Disposition: form-data; name="oauth_token_secret"

cf3ab706a60d457373740da7c68be4b4
--Boundary+*************
Content-Disposition: form-data; name="page"

1
--Boundary+*************--

'''
    res = requests.post(url, headers=head, data=body.encode('utf-8'))
    res2 = json.loads(res.text)
    print(res2)
    return res2['content']
def pu_submit(id):
    url = 'https://pocketuni.net/?app=api&mod=Event&act=join2'

    head = {'Cookie': '*****************************************************************',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Content-Type': 'multipart/form-data; boundary=Boundary+*************',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'pocketuni.net',
            'User-Agent': 'client:iOS version:6.8.70 Product:iPhone OsVersion:14.6',
            'version': '6.8.70',
            'Content-Length': '444',
            'Accept-Language': 'zh-Hans-CN;q=1'
            }
    body = '''--Boundary+*************
Content-Disposition: form-data; name="id"

''' + id + '''
--Boundary+*************
Content-Disposition: form-data; name="oauth_token"

588e2d37a7d45d1ac3f4638a25e5083c
--Boundary+*************
Content-Disposition: form-data; name="oauth_token_secret"

cf3ab706a60d457373740da7c68be4b4
--Boundary+*************--

'''
    res = requests.post(url, headers=head, data=body.encode('utf-8'))
    res2 = json.loads(res.text)
    return res2
def pushplus_send(title,message):
    requests.get(f'http://pushplus.hxtrip.com/send?token=*************&title={title}&content={message}&template=html')
    return
def step1_3():
    while True:
        res = pu_search('研究生学术')
        for re in res:
            print(re)
            t = time.time()
            if t < int(re['startline']):
                print('发现可报名活动，加入队列！')
                submit_list.append(re)
                pushplus_send('发现一个可以报名的活动！', '活动信息：' + str(re))
        time.sleep(1200)
    return
def step4_6():
    while True:
        for sub in submit_list:
            t1 = time.time()
            t2 = sub['startline']
            if t1 > int(t2):
                print('活动开始报名，正在提交！')
                #post代码
                res = pu_submit(sub['id'])
                print(res)
                #微信推送代码
                pushplus_send('帮您提交了一个PU活动报名！','活动信息：'+ str(res))
                submit_list.remove(sub)
            time.sleep(0.2)
def main():
    threads.append(threading.Thread(target=step1_3))
    threads.append(threading.Thread(target=step4_6))
    for t in threads:
        print(t)
        t.start()
    return
if __name__ == '__main__':
    main()
