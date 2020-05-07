#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#

import sqlite3 as lite
import os, sys

# picasa's and my own one-liner album summary
fcheck = ['Picasa.ini', '.picasa.ini', 'photos.txt']


def line1(lines):
    """ convert a string with newlines  to a single line with ; separating lines
    """
    return lines.replace('\n',';')

def fexist(fname):
    """ report if file exists
    """
    f = os.path.isfile(fname)
    caption = None
    if f:
        print '  ',fname
        lines = open(fname).readlines()
        if len(lines) == 1:
            caption = lines[0].strip()
        else:
            caption = ""
            for line in lines:
                w = line.split('=')
                if w[0] == 'description':
                    caption = caption + w[1].strip() + " "
        if len(caption) > 0:
            print '  ',caption
    return caption

def frename(fname):
    """ rename if file exists
    """
    f = os.path.isfile(fname)
    if f:
        fname_new = fname + ".bck"
        cmd = "mv %s %s" % (fname,fname_new)
        print "   CMD: ",cmd
        os.system(cmd)


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
        caption_old = line1(row[4])
        print row[1],row[2],row[3],caption_old
        for f in fcheck:
            fname = disk + row[2] + '/' + f
            caption = fexist(fname)
            if caption is not None:
                print "   ",caption
                caption = caption_old + " " + caption
                cmd = 'UPDATE Albums set caption = "%s" where relativePath = "%s"' % (caption,row[2])
                con1.execute(cmd)
                frename(fname)
    print "# Found %d albums with a caption" % ncapt

if True:
    nzero = 0
    cmd = 'SELECT * FROM Albums where albumRoot == %d AND caption IS NULL' % albumRoot
    cur1.execute(cmd)
    rows = cur1.fetchall()
    for row in rows:
        nzero += 1
        # print row[1],row[2],row[3]
        caption = ""
        for f in fcheck:
            fname = disk + row[2] + '/' + f
            caption = fexist(fname)
            if caption is not None:
                print "   ",caption
                cmd = 'UPDATE Albums set caption = "%s" where relativePath = "%s"' % (caption,row[2])
                con1.execute(cmd)
                frename(fname)
    print "# Found %d albums with no caption" % nzero

con1.commit()
n = con1.total_changes
print "Total number of rows updated in %s : %d" % ( db1, n)
con1.close()
