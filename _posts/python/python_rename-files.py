import os

FILE_PREFIX = 'news-'
[r for r,d,f in os.walk(os.getcwd())]
for x in f: os.rename(r+'/'+x, r+'/'+FILE_PREFIX+x)