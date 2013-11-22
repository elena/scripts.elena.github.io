import os, requests
# http://clients.thecut.net.au/nhg/widget/
# http://clients.thecut.net.au.s3.amazonaws.com/TEWA/v4/
URL = 'http://clients.thecut.net.au.s3.amazonaws.com/TEWA/v4/%s.jpg'
NUM = 18

for x in range(1,NUM):
    r = requests.get(URL % x)
    file_name = os.getcwd()+'/'+str(x)+'.jpg'
    f = open(file_name, 'w+')
    f.write(r.content)
    f.close()
    print file_name

