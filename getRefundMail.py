#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import imaplib
from email.mime.text import MIMEText
from email.utils import formataddr
import email
from mailParser import mailparser
import csv;
import codecs
import linecache


outname = 'mail.csv'


def readCsv(name):
    file = csv.reader(open(name))
    ret = {}
    for row in file:
        try:
            email = row[2]
            print email
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


res = readCsv(outname)
print res




