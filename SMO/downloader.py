import torndb
import os
import sys
import requests
import multiprocessing

SAVE_DIR='E:/begin_android_english'
con = torndb.Connection("120.27.92.166", "apk1", user="root", password="112112")

finish_num = 0
fail_num = 0

def update(apk,state):
    sql = "UPDATE apk SET state = %s WHERE package = %s"
    con.update(sql,state, apk['package'])

def downloader(apk):
    global finish_num
    global fail_num
    try:
        apk_url = apk['url']
        if not apk_url[0:4] == 'https':
            apk_url = 'https'+apk_url[4:]
        category = apk['category']
        save_dir=os.path.join(SAVE_DIR, category)
        filename = apk['package']
        save_path=os.path.join(save_dir, filename.strip()+'.apk')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if not os.path.exists(save_path):
            print ('downloading:' + apk_url + ' as: ' + save_path)
            result = requests.get(apk_url).content
            file = open(save_path, 'wb+')
            file.write(result)
            file.flush()
            file.close()
            print ('download finish:'+apk_url+' as: '+save_path)
        else:
            print(save_path+'is exits')
            finish_num += 1
        update(apk, 1)
    except:
        etype, evalue, tracebackObj = sys.exc_info()[:3]
        print ('url:%s errortype:%s errorvalue:%s' % (apk_url, etype, evalue))
        fail_num += 1
        update(apk, -1)


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=8)
    progress = multiprocessing.Process()
    progress.start()
    while 1:
        apks = con.query('select * from apk')
        for apk in apks:
            downloader(apk)
        print ('finish: %d fail %d' %(finish_num,fail_num))
        print ('finish task')
        if not apks==None:
            break
    pool.close()
    progress.terminate()
    progress.join()
    pool.join()
