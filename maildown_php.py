#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import imaplib
from email.mime.text import MIMEText
from email.utils import formataddr
import email
from mailParser import mailparser
import csv
import codecs
import linecache
import sys
import time
import os

#
# name2 = "xxxx@gmail.com"
# password2 = "xxxx"

storename = "ArtiLoves"

qq_smtp = 'smtp.exmail.qq.com'
qq_imap = 'imap.exmail.qq.com'

gmail_smtp = 'smtp.gmail.com'
gmail_imap = 'imap.gmail.com'

outname = 'mail.csv'


def readCsv(name):
    file = csv.reader(open(name))
    ret = {}
    for row in file:
        try:
            email = row[2]
            name = row[3]
            trackid = row[6]

            email = email.strip()
            name = name.strip()
            trackid = trackid.strip()


            if email not in ret:
                list=[]
                list.append([name, trackid])
            else:
                list.append([name, trackid])
            ret[email] = list

        except Exception, e:
            print e.message;

    return ret


#登录邮箱
def login_imap(name, password, type='qq'):
    if type == 'gmail':
        host = gmail_imap
    else:
        host = qq_imap

    try:
        server = imaplib.IMAP4_SSL(host, 993)
        server.login(name, password)
        return server
    except Exception, e:
        print(e.message)

    return None

#退出邮箱
def logout_imap(server):
    try:
        server.logout()
        return True
    except Exception, e:
        print(e.message)

    return False


#下载邮件
def download_mail(imap_server, writer, login_email):

    # 邮箱中其收到的邮件的数量
    imap_server.select("INBOX")
    typ, data = imap_server.search(None, 'UNSEEN')  # SEEN--已读邮件,UNSEEN--未读邮件,ALL--全部邮件
    if data[0]:
        number_list = data[0].split()  # 邮件编号list,编号越大邮件时间越近
        number_list.reverse()
        writer.writerow(
            ["邮箱类型", "发送邮件名", "发送邮件", "主题", "日期", "邮件内容"])
        for the_mail_number in number_list:
            # 将邮件标记为已读
            #email_server.store(the_mail_number, '+FLAGS', '\\SEEN')
            # 邮件内容详情
            try:
                typ, data = imap_server.fetch(the_mail_number, '(RFC822)')
                text = data[0][1]
                message = email.message_from_string(text)  # 转换为email.message对象
                parser = mailparser(message)
                sender = parser.get_from()
                subject = parser.get_subject()   #主题
                date = parser.get_date()   #日期
                emailcontent = parser.get_content()  #邮件内容
                sender_name = sender[0]    #发送邮件名
                sender_email = sender[1]   #发送邮件
                writer.writerow([login_email, sender_name, sender_email, subject, date, emailcontent])
                print sender_email
            except Exception, e:
                print(e.message)
    else:
        print "inbox is empty"


    # 关闭select
    imap_server.close()


try:
    # kfaccount = line.replace('\r', '').replace('\n', '').replace('\t', '')
    # kfaccount = kfaccount.split('|')
    kf_user = sys.argv[1]    #邮箱号
    kf_pass = sys.argv[2]    #密码
    mail_type = sys.argv[3]  #邮件类型
    currenttime=time.strftime("%Y%m%d%H:%M:%S", time.localtime())
    currentfilepath="/data/html/website/public/mail/" + str(kf_user) + "/"
    isExists = os.path.exists(currentfilepath)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(currentfilepath)
        print(currentfilepath + "Creating a successful")

    else:
        # 如果目录存在则不创建，并提示目录已存在
        print("Directory already exists ")
    f = open(currentfilepath+ str(kf_user) + "-email-" + currenttime+".csv", 'wb')
    f.write(codecs.BOM_UTF8)
    file2 = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    imap_server = login_imap(kf_user, kf_pass)
    #imap_server = login_imap(name2, password2, 'gmail')
    download_mail(imap_server, file2, mail_type)
    logout_imap(imap_server)
except Exception as e:
    print(e)
