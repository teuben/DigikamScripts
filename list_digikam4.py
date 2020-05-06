#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#

import sqlite3 as lite
import sys


def line1(lines):
    """ convert a string with newlines  to a single line with ; separating lines
    """
    return lines.replace('\n',';')

db1 = sys.argv[1]
if len(sys.argv) > 2:
    disk = sys.argv[2]
else:
    disk = ""

con1 = lite.connect(db1)
cur1 = con1.cursor()
cur1.execute('SELECT * FROM AlbumRoots')
ars = cur1.fetchall()

import os

def uuid_root(uuid):
    """ convert a uuid string to the mount point - only for linux
    """
    #print(uuid)
    idx = uuid.find('=') + 1
    f = os.popen('blkid -U %s' % uuid[idx:])
    lines = f.readlines()
    f.close()
    #print(lines)
    dev = lines[0].strip()
    f = open('/etc/mtab')
    lines = f.readlines()
    for line in lines:
        word = line.split()
        if word[0] == dev:
            #print("DEV %s -> %s" % (dev,word[1]))
            return word[1]
    
albumRootNo = -1
for ar in ars:
    #print("#old ",ar[0], ar[1], ar[2], ar[3], ar[4], ar[5])    
    mountPoint =  uuid_root(ar[4])
    print("#old ",ar[0], ar[1], ar[2], ar[3], mountPoint, ar[5])
    if ar[5] == disk:
        albumRootNo = ar[0]
        albumRoot   = mountPoint + '/' + ar[5]
        
import os.path

if albumRootNo < 1:
    print("No matching path to match for")
    sys.exit(0)
else:
    print("# albumRoot = %d %s" % (albumRootNo,albumRoot))
        
if True:
    ncapt = 0
    cmd = 'SELECT * FROM Albums where albumRoot == %d AND caption IS NOT NULL' % albumRootNo
    cur1.execute(cmd)
    rows = cur1.fetchall()
    for row in rows:
        ncapt += 1
        dirname = albumRoot + '/' + row[2]
        captionName = "%s/.caption" % dirname
        if not os.path.isfile(captionName):
            print("Going to write ",captionName)
            f = open(captionName,'w')
            f.write(row[4])
            f.close()
        print(row[1],row[2],row[3],line1(row[4]),captionName)
    print("# Found %d albums with a caption" % ncapt)

if True:
    nzero = 0
    cmd = 'SELECT * FROM Albums where albumRoot == %d AND caption IS NULL' % albumRootNo
    cur1.execute(cmd)
    rows = cur1.fetchall()
    for row in rows:
        nzero += 1
        dirname = albumRoot + '/' + row[2]
        captionName = "%s/.caption" % dirname
        if os.path.isfile(captionName):
            print("WARNING: We have a caption in ",captionName)
            if False:
                f = open(captionName,'r')
                f.close()
        #print('CHECK',row[1],row[2],row[3])
        #print('CHECK',dirname)
    print("# Found %d albums with no caption" % nzero)


con1.close()
