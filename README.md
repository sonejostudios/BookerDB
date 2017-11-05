# BookerDB
Open Source Show Management System

__Description:__

BookerDB is a tool to help musicians, artists and bookers with the organization of shows and everything around.
BookerDB is based on a csv database, classified by dates. It is possible to add/delete entries and do a lot more of manipulations.
It has a monitor to show all kind of filters around the database, like coming dates, played dates, statistics, contacts, etc... It can also export database entries into PDF (as info sheet with all important information) to take them as reminder on tour.


![screenshot](https://github.com/sonejostudios/BookerDB/blob/master/BookerDB.png "BookerDB")


__Features:__

* add/save/delete shows
* Monitor Filters COMING, PLAYED, WAITING, CANCELLED, CONTACT, City, Country, Venue, Artist, Contacts, etc...
* Statistics
* Notes
* Export Show(s) to PDF files
* Export Monitor to text file (i.e for printing)
* View show location on OSM or Gmaps (via webbrowser)
* Import/Export database to Working Folder. 
* Remote Working Folder (in cloud) handling (locked when imported, unlocked when exported)
* Use your own logo
* Backup system
* Open Folders from BookerDB directly (MATE, Cinnemon, GNOME, KDE only)
* Notify actions via OS
* and many many more...
  

__Installation:__

1. copy the whole BookerDB folder on your system
```
git clone https://github.com/sonejostudios/BookerDB.git
```

2. from this folder start BookerDB with: 
```
python3 BookerDB.py
```

__Requirements:__

* Python3
* Tkinter
* GNU/Linux (with cp, sed and sort)
* Webbrowser (i.e Firefox)
* File Manager (caja, nemo, nautilus, dolphin)
* PDF Reader


__Notes:__

* BookerDB was my playground for learning Python, so except a very very bad code. For now it's fine for me, I leared a lot and it works, but it __definitely__ needs a complete rewrite. If you have suggestions or you want to help with the rewrite, please contact me. Otherwise, have fun with it and organize yourself a lot of amazing shows!
* BookerDB is for now a Linux-only Software. It was tested only on LinuxMint MATE, but it should work also on Cinnamon, GNOME and KDE. No OSX and Windows versions are available.


__Tips and Tricks:__

* Point your working directory on a Cloud Service (Dropbox, Owncloud, Nextcloud etc). So the PDFs and all the exports will be shared with the other band/artist members. Use Import/Export Database to import it from or to export it to the remote working folder. Thanks to the remote database handling, different people can work on the same database. When imported, the remote database will be locked, so other people will not have access to it. Exporting it back will unlock it.
* Export the desired monitor view and open it with your favorit Text Editor or with an Office Suite (i.e LibreOffice) for printing.
* BookerDB makes an automatic database backup on starting (./bak/data.startbak.csv)
* All manual backups will be stored in ./bak/ with the actual date. If you want to do more backups in one day, just export the Database Monitor as Database Monitor.txt and rename it to data.csv
* BookerDB is only a Gui for the database. That means, not saved changes (changes, clean, etc) will only be saved by "Save Edit" od "Add". If you have deleted something by mistake, just don't save, go to an other show and come back, everything will be there as expected.
* Thanks to the CSV standard, it is possible to edit the database with an Office Suite (i.e. LibreOffice Calc). This make database viewing and manipulation even easier! (but make a backup first...)
* Change the BookerDB Logo with your own logo (in ./logo): "logo.png" will be used PDF export, "logo_gui.png" will be used in the GUI (this as to be 100x100 pixels).
* Change your currency on "Fee" only, the others will be updated automatically. Be careful, all currency entries have to be written as currency code : N.N CCC (i.e. 100.50 EUR) or N CCC (i.e 100 EUR).
* Use TAB while adding shows, it is specially designed to go through all entries in the right order.
* If you want to use BookerDB with different artists and different working folders, just install it several time on your computer. So you can have different remote working folder with each artist and you can also change the logo for each artist.




