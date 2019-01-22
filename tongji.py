# -*- coding: utf-8 -*-
import os
import csv
import sys
import datetime
csv.field_size_limit(sys.maxsize)
#条件
uu=['Money','refund','back','charge','scam','return']


#获取每个站点邮箱内符合条件的邮件
def getEverySiteEmailData():
    tempdata = {'2018/11': [], '2018/12': [], "2019/01": [],"other":[]}
    for root, dirs, files in os.walk("site"):
        for a in files:
            # print(a.replace(".csv", ""))
            with open("site/" + a, 'r') as csv_file:
                csv_reader_lines = csv.reader(csv_file)  # 逐行读取csv文件
                #将csv文件转换为数组
                data = []  # 创建列表准备接收csv各行数据
                for one_line in csv_reader_lines:
                    data.append(one_line)
                #遍历数组(每条邮件内容)
                for da in data:
                    if len(da)>=5:
                        try:
                            for uukey in uu:
                                if uukey.lower() in da[5].lower() or uukey in da[3].lower():
                                    d1 = datetime.datetime.strptime(str(da[4]).replace("/", "-"),'%Y-%m-%d')
                                    if ((d1-datetime.datetime.strptime('2018-11-01', '%Y-%m-%d')).days>=0 and (d1- datetime.datetime.strptime('2018-11-30', '%Y-%m-%d')).days<=0):
                                        tempdata['2018/11'].append(da)
                                        break

                                    elif ((d1-datetime.datetime.strptime('2018-12-01', '%Y-%m-%d')).days>=0 and (d1- datetime.datetime.strptime('2018-12-31', '%Y-%m-%d')).days<=0):
                                        tempdata['2018/12'].append(da)
                                        break
                                    elif ((d1-datetime.datetime.strptime('2019-1-01', '%Y-%m-%d')).days>=0 and (d1- datetime.datetime.strptime('2019-1-31', '%Y-%m-%d')).days<=0):
                                        tempdata['2019/01'].append(da)
                                        break
                                    else:
                                        tempdata['other'].append(da)
                        except Exception as e:
                            print(e)
    return tempdata

#获取11，12，1月份的拒付邮件数
def getRefuseData():
    with open("refuse.csv", 'r') as csv_file:
        csv_reader_lines = csv.reader(csv_file)  # 逐行读取csv文件
        # 将csv文件转换为数组
        data = []  # 创建列表准备接收csv各行数据
        for one_line in csv_reader_lines:
            data.append(one_line)
        print(len(data))
        #过滤掉头部，从第一行取
        tempdata={'2018/11':[],'2018/12':[],"2019/01":[],"other":[]}
        for index in range(1,len(data)):
            print(data[index][23])
            d1 = datetime.datetime.strptime(str(data[index][23]).replace("/","-"), '%Y-%m-%d %H:%M:%S')

            if ((d1-datetime.datetime.strptime('2018-11-01', '%Y-%m-%d')).days>=0 and (d1- datetime.datetime.strptime('2018-11-30', '%Y-%m-%d')).days<=0):
                tempdata['2018/11'].append(data[index])

            elif ((d1-datetime.datetime.strptime('2018-12-01', '%Y-%m-%d')).days>=0 and (d1- datetime.datetime.strptime('2018-12-31', '%Y-%m-%d')).days<=0):
                tempdata['2018/12'].append(data[index])

            elif ((d1-datetime.datetime.strptime('2019-1-01', '%Y-%m-%d')).days>=0 and (d1- datetime.datetime.strptime('2019-1-31', '%Y-%m-%d')).days<=0):
                tempdata['2019/01'].append(data[index])
            else:
                tempdata['other'].append(data[index])
    return tempdata




#获取收件箱中的邮件
total=getEverySiteEmailData()

#定义统计数据
statistics={'2018/11': {}, '2018/12': {}, "2019/01": {},"other":{}}


# 统计11，12，01发邮件的数量
sendemails=[]
for key, value in total.items():
    statistics[key]['sendemail'] = len(value)
    for va in value:
        if len(va) > 2:
            sendemails.append(str(va[2]).strip())#邮箱号
# print(sendemails)


#统计每月（11，12，19/01）拒付数
refuseemail={'2018/11': [], '2018/12': [], "2019/01": [],"other":[]}
orders=getRefuseData()


for key,value in orders.items():
    statistics[key]['refused']=len(value)
    for va in value:
        # print(len(va))
        if len(va)>16:
            refuseemail[key].append(str(va[16]).strip())

#统计发送邮件并拒付的、拒付没有发邮件的
for key,dateemail in refuseemail.items():
    #遍历每个月email
    i = 0
    j = 0
    for email in dateemail:
        #发送邮件并拒付的
        if email in sendemails:
            i=i+1
        else:
            j=j+1
    statistics[key]['sendemail&refused'] = i
    statistics[key]['refused&nosendemail'] = j

print(statistics)