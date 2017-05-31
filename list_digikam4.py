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

albumRoot = -1

con1 = lite.connect(db1)
cur1 = con1.cursor()
cur1.execute('SELECT * FROM AlbumRoots')
ars = cur1.fetchall()

for ar in ars:
    print "#old ",ar[0], ar[1], ar[2], ar[3], ar[5]
    if ar[5] == disk:
        albumRoot = ar[0]

if albumRoot < 1:
    print "No matching path to match for"
    sys.exit(0)
else:
    print "# albumRoot = ",albumRoot
        
if True:
    ncapt = 0
    cmd = 'SELECT * FROM Albums where albumRoot == %d AND caption IS NOT NULL' % albumRoot
    cur1.execute(cmd)
    rows = cur1.fetchall()
    for row in rows:
        ncapt += 1
        print row[1],row[2],row[3],line1(row[4])
    print "# Found %d albums with a caption" % ncapt

if True:
    nzero = 0
    cmd = 'SELECT * FROM Albums where albumRoot == %d AND caption IS NULL' % albumRoot
    cur1.execute(cmd)
    rows = cur1.fetchall()
    for row in rows:
        nzero += 1
        # print row[1],row[2],row[3]
    print "# Found %d albums with no caption" % nzero


con1.close()
