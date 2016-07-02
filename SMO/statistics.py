# coding: utf-8
categorys = {'education', 'book-reference', 'productivity', 'tools'}
import torndb
db = torndb.Connection("120.27.92.166","apk",user="root",password="112112")
#按类别统计各权限使用频度
def get_frequency():
    permissions = db.query("select name from permission_list WHERE frequency <> 0;")
    for per in permissions:
        sql = "insert into statistics select count(*),category,permission.name from permission,apk_permission where permission.name = '"+per['name']+"' and "+per['name']+" = 1 group by category;"
        db.execute(sql)

#计算权限的恶意权重
def get_weight():
    categorys = db.query("select distinct category from statistics")
    for cate in categorys:
        cate = cate['category']
        num = db.get("select count(package) from apk_permission WHERE category = '%s'"%(cate))
        num = num['count(package)']
        db.execute("update statistics set weight = frequency/%d WHERE category = '%s'"%(num, cate))

#计算每个apk的恶意值
categorys = db.query("select distinct category from statistics")
for cate in categorys:
    cate = cate['category']
    apks = db.query("select * from apk_permission WHERE category = '%s'"%cate)
    for apk in apks:
        permissions = db.query("select name,weight from statistics WHERE category = '%s'"%cate)
        sum = 0
        for per in permissions:
            sum += apk[per['name']] * per['weight']
        db.execute("update apk_permission set malice = %f WHERE package = '%s'"%(sum,apk['package']))


