#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#

import sqlite3 as lite
import sys

def line1(lines):
    """ convert a string with newlines  to a single line with ; separating lines
        the double-quote needs to be removed...
    """
    return lines.replace('\n',';').replace('"','')

db1 = sys.argv[1]
d1  = int(sys.argv[2])
db2 = sys.argv[3]
d2  = int(sys.argv[4])


print("# ",db1,d1)
con1 = lite.connect(db1)
cur1 = con1.cursor()
cur1.execute('SELECT * FROM AlbumRoots')
ar1 = cur1.fetchall()
for ar in ar1:
    if ar[0] == d1:
        print("# From: ",ar[0], ar[1], ar[2], ar[3], ar[5])

        print("# ",db2,d2)
con2 = lite.connect(db2)
cur2 = con2.cursor()
cur2.execute('SELECT * FROM AlbumRoots')
ar2 = cur2.fetchall()
for ar in ar2:
    if ar[0] == d2:
        print("# To:   ",ar[0], ar[1], ar[2], ar[3], ar[5])
        path_to = ar[5]

# sys.exit(0)        


# loop over all records in the old one that have a caption
# then take those and stuff them into the new one (even if it has one already)

cmd1 = 'SELECT * FROM Albums where albumRoot == %d AND caption IS NOT NULL' % d1
cur1.execute(cmd1)
rows = cur1.fetchall()
for row in rows:
    # print "ROW:",row
    cmd2 = 'SELECT * FROM Albums where albumRoot == %d and relativePath = "%s"' % (d2,row[2])
    cur2.execute(cmd2)
    r2 = cur2.fetchall()
    if len(r2) == 1:
        #print 'old',r1[0][1],r1[0][2],r1[0][3],r1[0][4]
        print('fix',row[1],row[2],row[3],line1(row[4]),'<-',r2[0][4])
        cmd = 'UPDATE Albums set caption = "%s" where relativePath = "%s"' % (line1(row[4]),row[2])
        #print "CMD:",cmd
        con2.execute(cmd)
    else:
        print("BAD len")


# when all is well, we commit (during development of the script we comment this out)

con2.commit()
n = con2.total_changes
# and report
print("Total number of rows updated in %s : %d" % ( db2, n))



con1.close()
con2.close()
