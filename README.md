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

  
