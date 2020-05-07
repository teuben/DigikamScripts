#! /usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#

import os
import sys
import os.path
import sqlite3 as lite


def line1(lines):
    """ convert a string with newlines  to a single line with ; separating lines
    """
    return lines.replace('\n',';')

def uuid_root(uuid):
    """ convert a uuid string to the mount point - only for linux
        1) read which partition the uuid belong to, via blkid
        2) read disk name from /etc/mtab (2nd argument)
    """
    # allow two variations for uuid:
    #       "volumeid:?uuid=697ce268-34e6-4edc-b601-b30e3e9990df"
    #       "697ce268-34e6-4edc-b601-b30e3e9990df"
    idx = uuid.find('=') + 1
    f = os.popen('blkid -U %s' % uuid[idx:])
    lines = f.readlines()
    f.close()
    # if this device doesn't exist (e.g. on a DB from another computer)
    # fake it
    if len(lines) == 0:
        return "//"
    #
    dev = lines[0].strip()
    f = open('/etc/mtab')
    lines = f.readlines()
    for line in lines:
        word = line.split()
        if word[0] == dev:
            #print("DEV %s -> %s" % (dev,word[1]))
            return word[1]
    return "///"

class dkdb(object):
    """
    generic class to access the digikam4.db (sqlite) database
    AlbumRoots:   id, label, status, type, identifier, specificPath
    Albums:       id, albumRoot, relativePath, date, caption, collection, icon
    """
    def __init__(self, filename, disk=None):
        self.filename = filename
        self.disk = disk
        self.con = lite.connect(filename)
        self.cur = self.con.cursor()

        self.cur.execute('SELECT * FROM AlbumRoots')
        self.ars = self.cur.fetchall()
        self.arid = self.setAlbumRootID(disk)

    def setAlbumRootID(self, disk):
        albumRootID = -1
        for ar in self.ars:
            #print("#old ",ar[0], ar[1], ar[2], ar[3], ar[4], ar[5])    
            mountPoint =  uuid_root(ar[4])
            print("# %-3s  %-15s  %s %s  %-25s %s" % (ar[0], ar[1], ar[2], ar[3], mountPoint, ar[5]))
            if ar[5] == disk:
                albumRootID = ar[0]
                albumRoot   = mountPoint + '/' + ar[5]
        #print("AlbumRootID=%d" % albumRootID)
        return albumRootID
    
        
    def close(self):
        self.con.close()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        disk = sys.argv[2]
    else:
        disk = None
    d1 = dkdb(sys.argv[1], disk)    
    sys.exit(1)

