# -*- coding: utf-8 -*-
import email
import email.utils
import datetime
import re

class mailparser:
    subject = ''
    sender = '',''
    to = []
    cc = []
    content = ''
    lastcontent = ''
    htmlcontent = ''
    allcontent = []
    date = None

    qqsplit = '------------------ Original ------------------'
    gmailsplit = 'gmail_quote'

    def __init__(self, message):
        self.subject = ''
        self.sender = ''
        self.to = []
        self.cc = []
        self.content = ''
        self.lastcontent = ''
        self.htmlcontent = ''
        self.allcontent = []
        self.date = None


        subject = message.get("subject")
        self.subject = self.decode_utf8(subject)

        sender = message.get("from")
        sender = email.utils.parseaddr(sender)
        self.sender = self.decode_utf8(sender[0]), sender[1]

        date = message.get("date")
        #self.date = self.decode_utf8(date) #email.header.decode_header(date)
        date = email.header.decode_header(date)
        date = date[0][0].replace('+00:00', '')
        date = re.split('[+-]', date)
        date = date[0].strip()
        try:
            utcdatetime = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S')
            localdatetime = utcdatetime + datetime.timedelta(hours=+8)
            self.date = localdatetime.date()
        except:
            utcdatetime = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S')
            self.date = utcdatetime.date()
        #finally:
            #utcdatetime = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S +0800')
            #self.date = utcdatetime.date()


        to = message.get("to")
        tolist = to.split(',')
        for item in tolist:
            to = email.utils.parseaddr(item)
            i = self.decode_utf8(to[0]), to[1]
            self.to.append(i)

        cc = message.get("cc")
        if cc is not None:
            cclist = cc.split(',')
            for item in cclist:
                cc = email.utils.parseaddr(item)
                i = self.decode_utf8(cc[0]), cc[1]
                self.cc.append(i)

        for part in message.walk():
            if not part.is_multipart():
                charset = part.get_charset()
                contenttype = part.get_content_type().lower()
                # print 'content-type', contenttype
                name = part.get_param("name")  # 如果是附件，这里就会取出附件的文件名
                if name:
                    # 有附件
                    # 下面的三行代码只是为了解码象=?gbk?Q?=CF=E0=C6=AC.rar?=这样的文件名
                    fh = email.Header.Header(name)
                    fdh = email.Header.decode_header(fh)
                    fname = fdh[0][0]
                    print '附件名:', fname
                    # attach_data = par.get_payload(decode=True) #　解码出附件数据，然后存储到文件中

                    # try:
                    #     f = open(fname, 'wb') #注意一定要用wb来打开文件，因为附件一般都是二进制文件
                    # except:
                    #     print '附件名有非法字符，自动换一个'
                    #     f = open('aaaa', 'wb')
                    # f.write(attach_data)
                    # f.close()
                else:
                    content = part.get_payload(decode=True)  # 解码出文本内容，直接输出来就可以了。
                    c = contenttype, content
                    self.allcontent.append(c)
                    if contenttype == 'text/plain':
                        self.content = content
                    elif contenttype == 'text/html':
                        self.htmlcontent = content

        gindex = self.htmlcontent.find(self.gmailsplit)
        qindex = self.htmlcontent.find(self.qqsplit)

        if gindex == -1 and qindex == -1:
            self.lastcontent = self.content
        elif gindex > 0 and (qindex < 0 or gindex < qindex): # gmail
            strs = self.content.split('<')
            s = strs[0]
            i = s.rfind('\r\n')
            self.lastcontent = s[0:i]
        elif qindex >0 and (gindex < 0 or qindex < gindex): #qqmail
            strs = self.content.split(self.qqsplit)
            self.lastcontent = strs[0]
        else:
            self.lastcontent = self.content

    def get_subject(self):
        return self.subject

    def get_from(self):
        return self.sender

    def get_to(self):
        return self.to

    def get_cc(self):
        return self.cc

    def get_content(self):
        return self.content

    def get_htmlcontent(self):
        return self.htmlcontent

    def get_all_content(self):
        return self.allcontent

    def get_last_content(self):
        return self.lastcontent

    def get_date(self):
        return self.date

    def decode_utf8(self, str):
        if str.strip() == '':
            return ''

        h = email.Header.Header(str)
        dh = email.Header.decode_header(h)
        data = dh[0][0]
        charset = dh[0][1]
        if charset == None:
            ret = data.encode('utf-8')
        else:
            ret = unicode(dh[0][0], dh[0][1]).encode('utf-8')
        return ret