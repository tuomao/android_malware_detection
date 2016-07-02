#coding:utf-8

import sys

import torndb
from androguard.misc import AnalyzeAPK

PERMISSIONS={}
db=torndb.Connection("120.27.92.166","apk",user="root",password="112112")

def extract_apk_permisson(name,category):
    path = 'D:\\android\\crawler\\'+category+'\\'+name+'.apk'
    try:
        apk=APK(path)
        if apk.is_valid_APK():
            package=apk.get_package()
            permissions=apk.get_permissions()
            # clean repeat permission
            simple_permissions=set()
            for p in permissions:
                p=p.split('.')[-1]
                if PERMISSIONS.has_key(p):
                    simple_permissions.add(p)

            insert_sql='insert into new_apk_permission(package,isMalware'
            attrs=','

            for permission in simple_permissions:
                    attrs=attrs+permission+','

            attrs=attrs.rstrip(',')
            values="values ('%s',%d,"%(package,1)
            for i in range(len(simple_permissions)):
                values=values+'1,'
            values=values.rstrip(',')
            values=values+')'

            insert_sql=insert_sql+attrs+') '+values

            print insert_sql
            #db.insert(insert_sql)

            print ('analysis %s'%(path))
        else:
            print('%s is not valid apk'%(path))
    except:

        etype, evalue, tracebackObj = sys.exc_info()[:3]
        print ('apk:%s errortype:%s errorvalue:%s'%(path,etype,evalue))
    finally:
        db.update("update apk set state = 1 where name='%s'"%name)

def get_permissions():
    global PERMISSIONS
    sql='select * from permission_list'

    result=db.query(sql)
    PERMISSIONS={ item['name']:{'protectionLevel':item['protectionLevel'],'permissionGroup':item['permissionGroup']} for item in result }

def get_un_analysis_files():
    sql='select name,category from apk where state = 0'
    result=db.query(sql)
    return result

def mutil_process_analysis():
    pool=multiprocessing.Pool(processes=args.process)
    files=get_un_analysis_files()
    for file in files:
        pool.apply(extract_apk_permisson,(file['name'].strip(),file['category'].strip()))
    pool.close()
    pool.join()
    print('finish work')

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--process", default=30,type=int,
                        help="process number")
    args=parser.parse_args()
    get_permissions()
    mutil_process_analysis()



