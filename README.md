# DigikamScripts
Dealing with digikam quirks


* list_digikam4.py  db_name [path_name]

  For a given sqlite database and path it will list all folder descriptions that are not empty
  It also adds some statistics

* repair_digikam4.py  db_from path_from  db_to path_to

  This applies the folder descriptions of {db_from,path_from} to the {db_to,path_to}, which of
  course will be changed!

  
