""" A quite inelegant and temporary way of working around Django's problem
with south migrations and custom user models.

This script replaces all the necessary part of migrations files to be more
generic.

INSTRUCTIONS
============

Replace variable "MIGRATIONS_LOCATION".

@@TD: detect by being in directory called 'migrations' rather than prefix of "0",
will perform marginally better.
@@TD: check all variable names are sane.
@@TD: better detection of duplicate settings imports
"""

import copy
import os
import re

DEBUG = True

MIGRATIONS_LOCATION = "/home/me/websites/django-project/"

frozen_match = """        'auth\.user': \{
            'Meta': \{'object_name': 'User'\},
            'date_joined': \('django\.db\.models\.fields\.DateTimeField', \[\], \{(.*)\}\),
            'email': \('django\.db\.models\.fields\.EmailField', \[\], \{(.*)\}\),
            'first_name': \('django\.db\.models\.fields\.CharField', \[\], \{(.*)\}\),
            'groups': \('django\.db\.models\.fields\.related\.ManyToManyField', \[\], \{(.*)\}\),
            'id': \('django\.db\.models\.fields\.AutoField', \[\], \{(.*)\}\),
            'is_active': \('django\.db\.models\.fields\.BooleanField', \[\], \{(.*)\}\),
            'is_staff': \('django\.db\.models\.fields\.BooleanField', \[\], \{(.*)\}\),
            'is_superuser': \('django\.db\.models\.fields\.BooleanField', \[\], \{(.*)\}\),
            'last_login': \('django\.db\.models\.fields\.DateTimeField', \[\], \{(.*)\}\),
            'last_name': \('django\.db\.models\.fields\.CharField', \[\], \{(.*)\}\),
            'password': \('django\.db\.models\.fields\.CharField', \[\], \{(.*)\}\),
            'user_permissions': \('django\.db\.models\.fields\.related\.ManyToManyField', \[\], \{(.*)\}\),
            'username': \('django\.db\.models\.fields\.CharField', \[\], \{(.*)\}\)
        \},
"""

frozen_replace = """        settings.AUTH_USER_MODEL: {
            'Meta': {'object_name': settings.AUTH_USER_MODEL.split('.')[-1]},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
"""


model_match = """from django.db import models"""
model_replace = """from django.db import models
from django.conf import settings"""

model_dupe_match = """from django.conf import settings
from django.conf import settings"""
model_dupe_replace = """from django.conf import settings"""


#  Replacments are a 3 tuple:
# (match, replace, method)
#
# `match` is the text to be replaced.
# `replace` is what it is replaced with.
# `method` is which method should be used the choices are: 're' or 'str'.
REPLACEMENTS = [(frozen_match, frozen_replace, 're'),
                (model_match, model_replace, 'str'),
                (model_dupe_match, model_dupe_replace, 'str'),
                (''', 'to': "orm['auth.User']"''',
                 """, 'to': "orm['{0}']".format(settings.AUTH_USER_MODEL)""", 'str'),
                ("""to=orm['auth.User']""",
                 """to=orm[settings.AUTH_USER_MODEL]""", 'str')]


for root, dir, files in os.walk(MIGRATIONS_LOCATION):
    path = root.split('/')
    if DEBUG: print (len(path) - 1) *'---' , os.path.basename(root)
    for file in files:
        if DEBUG: print len(path)*'---', file
        if file[:1] == "0":
            if DEBUG: print (len(path) - 1) *'---' , root
            if DEBUG: print file
            for rep in REPLACEMENTS:
                file_open = open(root+'/'+file, 'r')
                file_contents = file_open.read()
                file_open.flush()
                file_open.close()
                contents = copy.deepcopy(file_contents)
                if rep[2] == 're':
                    matched = re.search(rep[0], file_contents)
                    if matched:
                        if DEBUG: print("Replacing: ")
                        if DEBUG: print(contents[matched.start():matched.start()+len(rep[0])])
                        contents_replace = re.sub(rep[0], rep[1], contents)
                        if DEBUG: print("With: ")
                        if DEBUG: print(contents_replace[matched.start():matched.start()+len(rep[1])+1])
                        file_write = open(root+'/'+file, 'w')
                        file_write.write(contents_replace)
                        file_write.flush()
                        file_write.close()
                    else:
                        if DEBUG: print('good')
                if rep[2] == 'str':
                    start = contents.find(rep[0])
                    if start != -1:
                        if DEBUG: print("Replacing: ")
                        if DEBUG: print(contents[start:start+len(rep[0])])
                        contents_replace = contents.replace(rep[0], rep[1])
                        if DEBUG: print("With: ")
                        if DEBUG: print(contents_replace[start:start+len(rep[1])+1])
                        file_write = open(root+'/'+file, 'w')
                        file_write.write(contents_replace)
                        file_write.flush()
                        file_write.close()
                    else:
                        if DEBUG: print('good')


print('Migrations updated.')

