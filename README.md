# BookerDB
Open Source Show Management System

__Description:__

BookerDB is a tool to help musicians, artists and bookers with the organization of shows and everything around.
BookerDB is based on a csv database, classified by dates. It is possible to add/delete entries and do a lot more of manipulations.
It has a monitor to show all kind of filters around the database, like coming dates, played dates, statistics, contacts, etc... It can also export database entries into PDF (as info sheet with all important information) to take them as reminder on tour.


![screenshot](https://github.com/sonejostudios/BookerDB/blob/master/BookerDB.png "BookerDB")


__Main Features:__

* Add/Save/Delete Shows
* Monitor Filters COMING, PLAYED, WAITING, CANCELLED, WORK IN PROGRESS, CONTACT ONLY, City, Country, Venue, Artist, Contacts, etc...
* Statistics
* Notes
* Search
* Filter Monitor
* Backup and Restore
* Sync Addresses and Contacts
* Export Show(s) to PDF file(s)
* Export Monitor to text file (i.e for printing)
* Open Monitor with default Text Editor
* View Venue location on OSM or Gmaps (via Web Browser)
* Direct Links to Search engines, Youtube, Facebook, Soundcloud, Mails, etc 
* Send E-Mail to Contact via default Mail Client
* Import/Export database to Working Folder
* Remote Working Folder (in cloud) handling (locked when imported, unlocked when exported)
* Use your own logo
* Open Folders from BookerDB directly (MATE, Cinnemon, GNOME, KDE only)
* Notify actions via OS
* Sync Addresses and Contacts
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
* Web Browser (i.e Firefox)
* File Manager (caja, nemo, nautilus, dolphin)
* PDF Reader


__Notes:__

* BookerDB was my playground for learning Python, so except a very very bad code. For now it's fine for me, I learned a lot and it works, but it __definitely__ needs a complete rewrite. If you have suggestions or you want to help with the rewrite, please contact me. Otherwise, have fun with it and organize yourself a lot of amazing shows!
* BookerDB is for now a Linux-only Software. It was tested only on LinuxMint MATE, but it should work also on Cinnamon, GNOME and KDE. No OSX and Windows versions are available.


__Tips and Tricks:__

* Point your working directory on a Cloud Service (Dropbox, Owncloud, Nextcloud etc). So the PDFs and all the exports will be shared with the other band/artist members. Use Import/Export Database to import it from or to export it to the remote working folder. Thanks to the remote database handling, different people can work on the same database. When imported, the remote database will be locked, so other people will not have access to it. Exporting it back will unlock it. If you are not using BookerDB with a remote database, you can ignore these options.
* Export the desired monitor view and open it with your favorit Text Editor or with an Office Suite (i.e LibreOffice) for printing.
* BookerDB makes an automatic database backup on starting (./bak/data.startbak.csv)
* All manual Backups will be stored in ./bak/ with the actual date and time.
* BookerDB is only a Gui for the database. That means, not saved changes (changes, clean, etc) will only be saved by "Save Edit" od "Add". If you have deleted something by mistake, just don't save, go to an other show and come back, everything will be there as expected.
* Thanks to the CSV standard, it is possible to edit the database with an Office Suite (i.e. LibreOffice Calc). This make database viewing and manipulation even easier! (but make a backup first...)
* Change the BookerDB Logo with your own logo (in ./logo): "logo.png" will be used PDF export, "logo_gui.png" will be used in the GUI (this as to be 100x100 pixels).
* Change your currency on "Fee" only, the others will be updated automatically. Be careful, all currency entries have to be written as currency code : N.N CCC (i.e. 100.50 EUR) or N CCC (i.e 100 EUR).
* Use TAB while adding shows, it is specially designed to go through all entries in the right order.
* If you want to use BookerDB with different artists and different working folders, just install it several time on your computer. So you can have different remote working folder with each artist and you can also change the logo for each artist.
* Use mouse right-click to delete text entries (works on all except the working folder).
* Open external text editor directly with mouse right-click on monitor.
* Use Tools/Sync to copy Addresses and Contacts.
* In the show list, special states are shown with special symbols: -> = WORK IN PROGRESS, # = CANCELLED, $ = WAITING FOR MONEY, (space) = CONTACT ONLY.




__Menu:__

Database:
* DB Backup: This makes a Backup of the Database with date and time. It will be stored in the Backup forlder (bak in the app's main folder). You can access this folder directly via the menu Folder/Backupdir.
* Restore Backup: This will copy the newest Backup back to the main Database. If no actual Backups are available, this will restore the Start Backup.
* Import from Workdir: This imports the Database from the working directory (if exported there before) to the app's root directory. This in only interesting if the working directory is pointed to a cloud folder and used between different people. Importing the Database from Workdir will lock the database in the working directory, so nobody else can import it until it is exported back.
* Export to Workdir: Export the Database from the App's root directory to the working directoty. This will also unlock the Database in the working directory.


Tools:
* Export This Show to PDF: This will export the selected to to PDF into the working directory.
* Export All Shows to PDF: This will export all Shows of the Database to PDFs into the working directory. Usefull to have all PDFs up-to-date with the database entries. Be carefull, this will overwrite all PDFs and depending on the amount of shows, this can take a really long time!
* Export Monitor to TXT: This will export the current monitor view to a .txt file into the working folder. This will overwrite existing monitor exports. Really useful for sharing and printing.
* Open Monitor with Texteditor: Exports the Monitor content to a .txt file and open it with the default text editor. Same as: Right-click with the mouse on the monitor.
* Sync the Venue's Address : This will copy the current Address to all Shows with the same Venue in this City. This will replace Street, No, ZIP and Country. This also trigger an automatic Backup.
* Sync the Venue's Contact : This will copy the current Contact Entries to all Shows with the same Venue in this City. This will replace Contact, Phone and E-Mail. This also trigger an automatic Backup.


Folders:
* Open Workdir: Opens the working directory.
* Open Backupdir: Opens the backup directory (bak).
* Open Rootdir: Opens the root directory of BookerDB.


Web:
* Show on OSM: Try to find the Venue's Address on Open Street Map.
* Show on GMaps: Try to find the Venue's Adress on Google Maps.
* Web Search DDGo: Search for the Venue in DuckDuckGo.
* Web Search G: Search for the Venue on Google Search.
* Web Search Images: Search for Images on Google Images.
* Web Search Yt: Search for the Venue on YouTube.
* Web Search Fb: Search for the Venue on Facebook.
* Web Search Sc: Search for the Venue on Soundcloud.
* E-Mail to Contact: Start default mail application with the contact's e-mail.

(All Web Links are handled by DuckDuckGo with the Bang Syntax).


Help:
* Github: Direct link to BookerDB's Github.
* About: About BookerDB and version number.



__Buttons:__

* Save Edit: Save the current entry. If you are editing the very first entry, this will jump to the second one after saving due to database handling.
* Delete: Delete the current entry.
* Add: Create a new entry with the current informations. Also useful for copying entries.
* Clear all fields of the current entry. This will not be saved until the entry is saved via "Save Edit".

Important: Keep in mind BookerDB is just a "mirror" to the database. That means, nothing will be saved until it is explecitely saved via "Save Edit".


__Search/Filter:__

* Search highlights the searched shows in the show list. Validate with "Enter" or left-click. Right-click to delete. Focus it with "F1".
* Filter filters monitor text lines. Validate with "Enter" or left-click. This will automatically trigger the search fonction for the show list. Right-click to delete.


__Actual States:__

* COMING: Coming shows.
* PLAYED: Played and paid shows (completely done).
* WAITING FOR MONEY: Played but not paid yet, waiting for payment. ($ in show list).
* CANCELLED: Cancelled shows. (# in show list).
* WORK IN PROGRESS: Shows actually in negociation (work in progress). If the date is not fixed yet, use 9999-99-99 as date. (-> in show list).
* CONTACT ONLY: A venue, contact, info, but not a organized show. This will insert 9999-99-99 as date (not shown in show list), and the show will be sorted at the end of the Database.


__Keyboard and Mouse Shortcuts:__

Mouse:
* Right-click on Entries : Delete Entry.
* Right-click on Monitor : Open Monitor with default Text Editor. 
* Mouse roll on "Monitor Presets" or "Actual State" to navigate quickly.
* Left-click on Search and Filter will start the search/filtering.


Keyboard:
* Ctrl+1 : Focus on Search.
* Ctrl+2 : Focus on Filter.
* Ctrl+3 : Focus on first Entry (Artists).
* Ctrl+L : Focus on Show List.
* Ctrl+P : Focus on Monitor Presets.

* Ctrl+S : Save/Edit this Show.
* Ctrl+D : Delete this Show.
* Ctrl+A : Add Show to Database.
* Ctrl+K : Clear all Entries.
* Ctrl+B : Backup Database.
* Ctrl+T : Export Monitor and open it with default Text Editor.

* Ctrl+O : Search on Open Street Map with default Web Browser.
* Ctrl+M : Search on Google Maps with default Web Browser.
* Ctrl+Q : Search on DuckDuckGo with default Web Browser.
* Ctrl+W : Search on Google with default Web Browser.

* Ctrl+E : Send E-Mail to Contact with default Mail Application.

