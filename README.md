# DigikamScripts

Dealing with digikam quirks.  If you set up digikam to store captions and labels in the picture, the
other major thing left are the album captions. These scripts allow you to store them in a ALBUM/.caption
file, and re-read them again.

The hierarchy we are dealing with is  Collections - Albums - Photos

* listall_digikam4.py db_name

  For a given sqlite database, list all album captions for all collections

* list_digikam4.py  db_name [path_name]

  For a given sqlite database and path it will list all folder descriptions that are not empty
  It also adds some statistics

* repair_digikam4.py  db_from ID_from  db_to ID_to

  This applies the folder descriptions of {db_from,ID_from} to the {db_to,ID_to}, which of
  course will be changed!   ID's are the integers you need to obtain from list_digikam4.py

  **WARNING**   this hasn't been tested recently, 

* read_digikram4.py  db_name [path_name]

  Will populate the db_name (assumed to be sqlite) with album titles found in .caption files
  that did not have a caption in the db
  If there is no .caption file, it will also write one.

  It has been confirmed that digikam and these python scripts can simultaneously writen in the database,
  which is perhaps surprising. Despite that, I recommend that you close digikam when writing into the
  db.

# Caveats

This is by no means a finished product. I just needed to merge some old album captions into a new one. See the
section below on ideas what might be coming.

# Possible enhancements:

* allow album captions to go into a (one liner?) text file in the album directory. picasa used to do this.

* allow these album captions (from a file in the directory) to be merged into the digikam4.db file.

* allow a version of repair_digikam that can read a text file (e.g. created via list_digikam, with some editing)
