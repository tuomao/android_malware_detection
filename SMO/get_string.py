# coding: utf-8
import os
import torndb
import re
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.eElementTree as ET

apkPath = "D:\\android\\apktool_out\\"
dirlist = os.listdir(apkPath)
con = torndb.Connection('120.27.92.166','apk',user='root',password='112112')
def getPackage(path):
    try:
        root = ET.parse(path).getroot()
        return root.get('package')
    except:
        print path

def getString(path):
    tree = ET.parse(path)
    dict = {}
    for string in tree.findall('string'):
        id = string.get('name')
        text = string.text
        if not text == None:
            text = re.sub('[^a-zA-Z\'\s]', '', text)
            text = text.replace('\'', '\\\'')
            dict[id] = text.strip()
    return dict


def getLayoutString(path,dict):
    tree = ET.parse(path).getroot()
    android = "{http://schemas.android.com/apk/res/android}"
    layoutString = ''
    for text in tree.iter('TextView'):
        string = text.get(android+'text')
        if not string == None:
            pattern = re.compile("@string/(\S*)")
            res = pattern.search(string)
            if not res == None:
                s = res.group(1)
                if not dict.get(s)==None:
                    layoutString += dict[s]
            elif not string == '':
                string = re.sub('[^a-zA-Z\'\s]','', string)
                string = string.replace('\'','\\\'')
                layoutString += string.strip()+','
    return layoutString


for i in range(1,len(dirlist)):  # 得到apk 文件夹下的每一个子的类别
    filelist = apkPath + dirlist[i]  # 获取每个类别的路径
    apklist = os.listdir(filelist)  # 获取每个路径下的apk 列表
    for APK in apklist:
        APK = filelist+'\\'+APK
#APK = 'D:\\android\\apktool_out\\books-reference\\25_Small_Surah_Bangla_1.2'
        path = APK+'\\AndroidManifest.xml'
        layoutString = ''
        if os.path.exists(path):
            package = getPackage(path)
        path = APK+'\\res\\values\\strings.xml'
        if os.path.exists(path):
            dict = getString(path)
        path = APK+'\\res\\layout'
        if os.path.exists(path):
            layoutlist = os.listdir(path)
            for file in layoutlist:
                if os.path.isfile(path + '\\' + file):
                    layoutString += getLayoutString(path + '\\' + file,dict)
        con.execute("update apk_permission set layout_string='%s' where package='%s'"%(layoutString,package))
    print dirlist[i]+' done'
con.close()
print "all work done"

