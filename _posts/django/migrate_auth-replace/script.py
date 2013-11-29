import os
import copy


DEBUG = True

var1 = "/home/elena/auth-replace.txt"
var2 = "/home/elena/auth-replace-2.txt"
var3 = "/home/elena/auth-replace-3.txt"
rep = "/home/elena/auth-replaced.txt"
fvar1 = open(var1, 'r')
fvar2 = open(var2, 'r')
fvar3 = open(var3, 'r')
frep = open(rep, 'r')
svar1 = fvar1.read()
svar2 = fvar2.read()
svar3 = fvar3.read()
srep = frep.read()

model_pre = """from django.db import models

"""
model_post = """from django.db import models
from thecut.authorship.settings import AUTH_USER_MODEL

"""

REPLACEMENTS = [
     (svar1, srep),
     (svar2, srep),
     (svar3, srep),
     (model_pre, model_post),
     (''', 'to': "orm['auth.User']"''',
      """, 'to': "orm['{0}']".format(AUTH_USER_MODEL)"""),
     ("""to=orm['auth.User']""",
      """to=orm[AUTH_USER_MODEL]""")]


WALK = os.getcwd()
WALK = "/home/elena/websites/turnerengineering.com.au/lib/python2.7/site-packages/thecut/"


for root, dir, files in os.walk(WALK):
    path = root.split('/')
    print (len(path) - 1) *'---' , os.path.basename(root)
    for file in files:
        print len(path)*'---', file
        if file[:2] == "00":
            print (len(path) - 1) *'---' , root
            print file
            for rep in REPLACEMENTS:
                f = open(root+'/'+file, 'r')
                s = f.read()
                f.flush()
                f.close()
                u = copy.deepcopy(s)
                start = u.find(rep[0])
                if start != -1:
                    print("Replacing: ")
                    print(u[start:start+len(rep[0])])
                    t = u.replace(rep[0], rep[1])
                    print("With: ")
                    print(t[start:start+len(rep[1])+1])
                    w = open(root+'/'+file, 'w')
                    w.write(t)
                    w.flush()
                    w.close()
                else:
                    print('pass')

