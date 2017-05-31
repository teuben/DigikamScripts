# DigikamScripts
Dealing with digikam quirks

* listall_digikam4.py db_name

  For a given sqlite database, list all album captions

* list_digikam4.py  db_name [path_name]

  For a given sqlite database and path it will list all folder descriptions that are not empty
  It also adds some statistics

* repair_digikam4.py  db_from ID_from  db_to ID_to

  This applies the folder descriptions of {db_from,ID_from} to the {db_to,ID_to}, which of
  course will be changed!   ID's are the integers you need to obtain from list_digikam4.py

  
# Caveats

This is by no means a finished product. I just needed to merge some old album captions into a new one. See the
section below on ideas what might be coming.

# Possible enhancements:

* allow album captions to go into a (one liner?) text file in the album directory. picasa used to do this.

* allow these album captions (from a file in the directory) to be merged into the digikam4.db file.

* allow a version of repair_digikam that can read a text file (e.g. created via list_digikam, with some editing)
