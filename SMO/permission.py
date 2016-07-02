#coding: utf-8
import torndb
import os
con = torndb.Connection('120.27.92.166','apk',user='root',password='112112')

file = open('./permission list.csv','r')
# for line in file:
#     con.insert('insert into permission_list(name) VALUE(%s)',line.strip('\n'))
create_table_sql = "create table new_apk_permission(package VARCHAR (255),isMalware int DEFAULT 0,"
for line in file:
    create_table_sql = "%s %s int DEFAULT 0," % (create_table_sql,line.strip('\n'))
    # try:
    #     insert_sql = "insert into permission(name,protectionLevel,permissionGroup) VALUES " \
    #         "('%s','%s','%s')" % (permission.get('name'), permission.get('protectionLevel'), permission.get('group'))
    #     #con.execute(insert_sql)
    # except:
    #     pass

create_table_sql = create_table_sql+"PRIMARY KEY (package))"
con.execute(create_table_sql)
con.close()