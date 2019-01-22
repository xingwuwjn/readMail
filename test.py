import datetime
d1 = datetime.datetime.strptime('2015-1-01 17:41:21', '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime('2015-03-02', '%Y-%m-%d')
print((d1 - d2).seconds)
if (d1 - d2).seconds>0:
    print("true")
else:
    print("false")



if("2019-01-03">"2019-1-01" and "2019-01-03"<="2019-1-31"):
    print("true")
else:
    print("false")

result={}
domain='sosoluckyshops_myshopify_com'


if domain in result:
    print('ok')
else:
    result['sosoluckyshops.myshopify.com'] = 'sdlfjalsd'

print(result)