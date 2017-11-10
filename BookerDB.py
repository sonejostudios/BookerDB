# BookerDB - Open Source Show Management System
# Version 0.2.1


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import csv
import os
import datetime
import subprocess
from subprocess import call
import webbrowser

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font



data_file = "data.csv"

monitor_presets_sel = StringVar
tour = StringVar
tour_sum = StringVar
exportpath = StringVar
money_sum_string = StringVar

coming_fee = 0.0
coming_fee_add = 0.0

date = StringVar
city = StringVar
venue = StringVar

date_time = str(datetime.datetime.now())
today = date_time[:10]

pdf_ypos = +20

map_select = 0


white = "#ffffff"
black = "#000000"


preset_list  = ("COMING", "COMING + Artist", "PLAYED", "WAITING FOR MONEY", "CANCELLED", "CONTACT ONLY","Actual States",
                "Statistics",  "Notes", "Cities", "Countries", "Artists", "Venues","Contacts",
                "E-Mails", "COMING E-Mails", "PLAYED E-Mails","WAITING E-Mails","CANCELLED E-Mails", "CONTACT ONLY E-Mails",
                "Address", "Address Print", "Print", "Database Monitor",
                "Tour", "Tour2", "Tour3", "Tour4", "Tour5", "Tour6")


state_list = ("COMING", "PLAYED", "WAITING FOR MONEY", "CANCELLED", "CONTACT ONLY")




# about
def about_app():
    messagebox.showinfo("About", "BookerDB 0.2.1\nby Vincent Rateau\nwww.sonejo.net\n\nLicensed under GPL 3.0")

def website():
    webbrowser.open_new_tab("https://github.com/sonejostudios/BookerDB")

def websearch():
    venue = venue_entry.get()
    city = city_entry.get()
    country = country_entry.get()

    webbrowser.open_new_tab("https://duckduckgo.com/?q=" + venue + "+" + city + "+" + country)




### ------ CONFIG ------- ####

def write_config():
    exportpath = str(exportpath_entry.get())
    configfile = open("config.csv", "w")
    configfile.write(exportpath)
    configfile.close()


def read_config():
    configfile = open("config.csv", "r")

    exportpath = configfile.read()

    # set path in exportpath_entry
    exportpath_entry.delete(0, END)
    exportpath_entry.insert(0, exportpath)

    configfile.close()


# print do nothing
def do_nothing():
    print("do nothing")
    pass


#notify
def notify(message):
    os.system('notify-send "{}" "{}"'.format("BookerDB", message))


# focus next widget
def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")


# check if os command exists
def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


# on quit
def on_quit():
    workdir = exportpath_entry.get()

    # save export path into config.csv
    write_config()

    try:
        file = open(workdir + "data.workdir.csv.lok", "r")
        messagebox.showerror("Remote DB", "The Remote Database in the Working Folder is locked !\nPlease Export it back.")
    except:
        root.quit()


# check environement and set file browser
def set_env():
    # save export path into config.csv
    write_config()

    if cmd_exists("caja") == TRUE: # MATE
        return "caja"
    elif cmd_exists("nemo") == TRUE: # Cinnamon
        return "nemo"
    elif cmd_exists("nautilus") == TRUE: # GNOME
        return "nautilus"
    elif cmd_exists("dolphin") == TRUE: # KDE
        return "dolphin"
    else:
        messagebox.showerror("Error", "No filebrowser detected.")


# open workdir
def open_workdir():
    workdir = exportpath_entry.get()
    filebrowser = set_env()
    call(filebrowser + " " + workdir, shell=TRUE) # better than os.system

def open_bakdir():
    bakdir = os.path.dirname(os.path.realpath(__file__))
    filebrowser = set_env()
    call(filebrowser + " " + bakdir + "/bak", shell=TRUE)

def open_rootdir():
    rootdir = os.path.dirname(os.path.realpath(__file__))
    filebrowser = set_env()
    call(filebrowser + " " + rootdir, shell=TRUE)



# remote database
def export_to_workdir():
    workdir = exportpath_entry.get()

    os.system("cp data.csv " + workdir + "data.workdir.csv")
    os.system("rm " + workdir + "data.workdir.csv.lok ")
    notify("Database exported to Working Folder.\nRemote DB unlocked.")



def import_from_workdir():
    workdir = exportpath_entry.get()
    try:
        file = open(workdir + "data.workdir.csv", "r")
        os.system("cp " + workdir + "data.workdir.csv data.csv")
        os.system("mv " + workdir + "data.workdir.csv " + workdir + "data.workdir.csv.lok")
        notify("Database imported from Working Folder.\nRemote DB locked.")
    except:
        messagebox.showerror("Database", "Database in Workdir is locked !\nTry again later...")
    read_csv_line()







# check state and do warnings or focus
def state_check(event):
    print("state selected")

    if statebox_entry.get() == "CONTACT ONLY":
        messagebox.showwarning("Info", "CONTACT ONLY will delete the date when saved or added.")

    elif statebox_entry.get() != "CONTACT ONLY" and date_entry.get() == "9999-99-99":
        date_entry.delete(0,END)
        date_entry.focus_set()


# maps
def show_on_map():
    if map_select == 0:
        show_map("osm")
    else:
        show_map("gmaps")

def show_osm():
    global map_select
    map_select = 0
    mapsmenu.entryconfig(0, label="Show on OSM *")
    mapsmenu.entryconfig(1, label="Show on GMaps")
    #map.config(text="Show on OSM")
    #show_map("osm")
    notify("Show Venues on OSM.")


def show_gmaps():
    global map_select
    map_select = 1
    mapsmenu.entryconfig(1, label="Show on GMaps *")
    mapsmenu.entryconfig(0, label="Show on OSM")
    #map.config(text="Show on GMaps")
    #show_map("gmaps")
    notify("Show Venues on GMaps.")


def show_map(x):
    city = city_entry.get()
    city2 = city.replace(" ", "+")
    street = street_entry.get()
    street2 = street.replace(" ","+")
    nr = nr_entry.get()
    nr2 = nr.replace(" ","+")
    country = country_entry.get()
    country2 = country.replace(" ", "+")

    # gmaps
    if x == "gmaps":
        webbrowser.open_new_tab("https://www.google.de/maps/place/" + country2 + "+" + city2 + "+" + street2 + "+" + nr2)

    # open street map
    else:
        webbrowser.open_new_tab("https://www.openstreetmap.org/search?query=" + country2 + "+" + city2 + "+" + street2 + "+" + nr2)






def stats():

    monitor.delete(0.0, END)

    # set var
    fee_sum = 0.0
    travelmoney_sum = 0.0

    coming_fee = 0.0
    played_fee = 0.0
    cancelled_fee = 0.0
    waiting_fee = 0.0
    contact_fee = 0

    coming_count = 0
    played_count = 0
    cancelled_count = 0
    waiting_count = 0
    contact_count = 0

    waiting_travelmoney = 0.0


    # monitor view presets
    monitor_presets_sel = monitor_presets.get()

    if monitor_presets_sel == "Statistics":
        with open('data.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                fee = row[19]
                fee_nb = fee[:-3]
                fee_float = float(fee_nb)
                fee_sum += fee_float

                travelmoney = row[20]
                travelmoney_nb = travelmoney[:-3]
                travelmoney_float = float(travelmoney_nb)
                travelmoney_sum += travelmoney_float
                travelmoney_sum2 = "%.2f" % travelmoney_sum

                state = int(row[32])

                if state == 0:
                    coming_fee += fee_float
                    coming_count += 1


                if state == 1:
                    played_fee += fee_float
                    played_count += 1


                if state == 2:
                    waiting_fee += fee_float
                    waiting_travelmoney += travelmoney_float
                    waiting_count += 1


                if state == 3:
                    cancelled_fee += fee_float
                    cancelled_count += 1

                if state == 4:
                    contact_fee += fee_float
                    contact_count += 1


        total_line_count = str(sum(1 for line in open(data_file)))

        fee_sum2 = "%.2f" % fee_sum
        currency = str(fee[-4:])

        fee_average = float(fee_sum2) / int(total_line_count)
        fee_average2 = "%.2f" % fee_average

        travelmoney_average = float(travelmoney_sum2) / int(total_line_count)
        travelmoney_average2 = "%.2f" % travelmoney_average

        waiting_fee_travel_sum = float(waiting_fee) + float(waiting_travelmoney)
        waiting_fee_travel_sum2 = "%.2f" % waiting_fee_travel_sum


        # check if gig count > 0, otherwise set 0 - for average
        if coming_count > 0:
            coming_fee_average = float(coming_fee) / int(coming_count)
            coming_average2 = "%.2f" % coming_fee_average
        else:
            coming_average2 = "0"

        if played_count > 0:
            played_fee_average = float(played_fee) / int(played_count)
            played_average2 = "%.2f" % played_fee_average
        else:
            played_average2 = "0"


        fee_sum_played_waiting = played_fee + waiting_fee
        count_sum_played_waiting = played_count + waiting_count

        if count_sum_played_waiting > 0:
            fee_sum_played_waiting_average = float(fee_sum_played_waiting) / int(count_sum_played_waiting)
            fee_sum_played_waiting_average2 = "%.2f" % fee_sum_played_waiting_average
        else:
            fee_sum_played_waiting_average2 = "0"

        monistats = "COMING - Shows : " + str(coming_count) + "\n" + \
                    "COMING - Fee : " + str(coming_fee) + currency + "\n" + \
                    "COMING - Average : " + coming_average2 + currency + "\n\n" + \
                    "-----------------------------------" + "\n\n" + \
                    "PLAYED - Shows : " + str(played_count) + "\n" + \
                    "PLAYED - Fee : " + str(played_fee) + currency + "\n" + \
                    "PLAYED - Average : " + played_average2 + currency + "\n\n" + \
                    "-----------------------------------" + "\n\n" + \
                    "PLAYED+WAITING - Shows : " + str(count_sum_played_waiting) + "\n" + \
                    "PLAYED+WAITING - Fee: " + str(fee_sum_played_waiting) + currency + "\n" + \
                    "PLAYED+WAITING - Average: " + str(fee_sum_played_waiting_average2) + currency + "\n\n" + \
                    "-----------------------------------" + "\n\n" + \
                    "WAITING FOR MONEY - Shows : " + str(waiting_count) + "\n" + \
                    "WAITING FOR MONEY - Fee : " + str(waiting_fee) + currency + "\n" + \
                    "WAITING FOR MONEY - Fee+Travel : " + str(waiting_fee_travel_sum2) + currency + "\n\n" + \
                    "-----------------------------------" + "\n\n" + \
                    "CANCELLED - Shows : " + str(cancelled_count) + "\n" + \
                    "CANCELLED - Fee : " + str(cancelled_fee) + currency + "\n\n" + \
                    "-----------------------------------" + "\n\n" + \
                    "CONTACT ONLY - Shows : " + str(contact_count) + "\n\n" + \
                    "-----------------------------------" + "\n\n" + \
                    "Shows in Database : " + total_line_count + "\n\n" + \
                    "-----------------------------------" + "\n"


        monitor.insert(END, monistats)
        monitor.insert(END, "\n")




### ------ READ-WRITE DB ------- ####

# read "tour" for listbox and monitor
def read_tour():

    # delete listbox and monitor
    gig_listbox.delete(0, END)
    monitor.delete(0.0, END)



    with open(data_file, 'r') as datafile:
        reader = csv.reader(datafile)
        for row in reader:

            date = str(row[0])
            city = str(row[1])
            venue = str(row[2])

            artist = str(row[3])

            street = str(row[4])
            nr = str(row[5])
            zip = str(row[6])
            country = str(row[7])

            contact = str(row[8])
            phone = str(row[9])
            email = str(row[10])

            fee = str(row[19])
            travelmoney = str(row[20])
            currency = str(fee[-4:])
            fee_float = float(fee[:-3])
            travelmoney_float = float(travelmoney[:-3])
            fee_sum = fee_float + travelmoney_float

            prints = str(row[27])

            addressprint1 = str(row[28])
            addressprint2 = str(row[29])
            addressprint3 = str(row[30])
            addressprint4 = str(row[31])

            statebox = state_list[int(row[32])]


            #insert in listbox
            if date == "9999-99-99":
                tour = "   " + city +  " (" +country + ")" + " - " + venue   #" (" +country + ")" +
            else:
                tour = date + " - " + city + " - " + venue  + " - " + artist
            gig_listbox.insert(END, tour)


            #monitor view presets
            monitor_presets_sel = monitor_presets.get()

            if monitor_presets_sel == "Tour":
                tour = date + " - " + city + " - " + venue + "\n"

            elif monitor_presets_sel == "Tour2":
                tour = date + " - " + city + " - " + venue + " - " + artist + "\n"

            elif monitor_presets_sel == "Tour3":
                tour = date + " " + city + " " + venue + "\n"

            elif monitor_presets_sel == "Tour4":
                tour = date + "\n" + city + "\n" + venue + "\n" + "\n"

            elif monitor_presets_sel == "Tour5":
                tour = date + "\n" + city + ", " + venue + "\n" + "\n"

            elif monitor_presets_sel == "Tour6":
                tour = date + " \n" + city + " - " + venue + "\n" + "\n"

            elif monitor_presets_sel == "Contacts":
                tour = venue +  " (" + city + " - " + date + " - " + artist + ")"  + "\n" + contact + " : " + phone + " - " +  email + "\n" + "\n"

            elif monitor_presets_sel == "Print":
                tour = city + " - " + venue  + " (" + artist + ") -> " + prints + "\n" + "\n"

            elif monitor_presets_sel == "Address":
                tour = venue + "\n" + street + " " + nr + "\n" + zip + " " + city + "\n" + country + "\n" + "\n"

            elif monitor_presets_sel == "Address Print":
                tour = venue + "\n" + addressprint1 + "\n" + addressprint2 + "\n" + addressprint3 + "\n" + addressprint4 + "\n\n" + "\n"

            elif monitor_presets_sel == "Statistics":
                pass

            elif monitor_presets_sel == "Actual States":
                tour = date + " - " + city   + " - " + venue + " (" + artist + ") : " + statebox + "\n"



            elif monitor_presets_sel == "COMING":
                if statebox == "COMING":
                    tour = date + " - " + city   + " - " + venue + "\n"
                else:
                    tour = ""

            elif monitor_presets_sel == "COMING + Artist":
                if statebox == "COMING":
                    tour = date + " - " + city   + " - " + venue  + " - " + artist + "\n"
                else:
                    tour = ""

            elif monitor_presets_sel == "PLAYED":
                if statebox == "PLAYED":
                    tour = date + " - " + city   + " - " + venue + " - " + artist + "\n"
                else:
                    tour = ""

            elif monitor_presets_sel == "CANCELLED":
                if statebox == "CANCELLED":
                    tour = date + " - " + city   + " - " + venue + " - " + artist + "\n"
                else:
                    tour = ""

            elif monitor_presets_sel == "WAITING FOR MONEY":
                if statebox == "WAITING FOR MONEY":
                    tour = date + " - " + city   + " - " + venue + " - " + artist + " : " + str(fee_sum) + currency + "\n"
                else:
                    tour = ""

            elif monitor_presets_sel == "CONTACT ONLY":
                if statebox == "CONTACT ONLY":
                    tour = city  + " (" + country + ")" + " - " + venue + " - " + artist + "\n"
                else:
                    tour = ""


            elif monitor_presets_sel == "Cities":
                tour = city + " (" + country + ")" + " - " + venue + " (" + artist + " - " + date + ")\n"

            elif monitor_presets_sel == "Countries":
                tour = country + " - " + city   + " - " + venue + " (" + artist + " - " + date + ")\n"


            elif monitor_presets_sel == "Artists":
                tour = artist   + " - " + city + " (" + country + ")" + " - " + venue + " (" + date + ")\n"

            elif monitor_presets_sel == "Venues":
                tour = venue   + " (" + city + " - " + country + ") - " + artist + " (" +  date + ")\n"


            elif monitor_presets_sel == "Notes":
                tour = ""
                pass


            elif monitor_presets_sel == "E-Mails":
                tour = contact + " <" + email + ">\n"


            elif monitor_presets_sel == "COMING E-Mails":
                if statebox == "COMING":
                    tour = contact + " <" + email + ">\n"
                else:
                    tour = ""

            elif monitor_presets_sel == "PLAYED E-Mails":
                if statebox == "PLAYED":
                    tour = contact + " <" + email + ">\n"
                else:
                    tour = ""


            elif monitor_presets_sel == "WAITING E-Mails":
                if statebox == "WAITING FOR MONEY":
                    tour = contact + " <" + email + ">\n"
                else:
                    tour = ""


            elif monitor_presets_sel == "CANCELLED E-Mails":
                if statebox == "CANCELLED":
                    tour = contact + " <" + email + ">\n"
                else:
                    tour = ""

            elif monitor_presets_sel == "CONTACT ONLY E-Mails":
                if statebox == "CONTACT ONLY":
                    tour = contact + " <" + email + ">\n"
                else:
                    tour = ""



            else:
                tour = date + " - " + city + " - " + venue + "\n"

            monitor.insert(END, tour)


    #calculate stats
    if monitor_presets_sel == "Statistics":
        stats()
    else:
        tour = date + " - " + city + " - " + venue


    #insert title in monitor
    if monitor_presets_sel == "COMING":
        monitor.insert(0.0, "COMING (" + today + ") :\n\n")

    if monitor_presets_sel == "COMING + Artist":
        monitor.insert(0.0, "COMING + Artist (" + today + ") :\n\n")

    if monitor_presets_sel == "PLAYED":
        monitor.insert(0.0, "PLAYED (" + today + ") :\n\n")

    if monitor_presets_sel == "CANCELLED":
        monitor.insert(0.0, "CANCELLED (" + today + ") :\n\n")

    if monitor_presets_sel == "WAITING FOR MONEY":
        monitor.insert(0.0, "WAITING FOR MONEY : Fee + Travel (" + today + ") :\n\n")

    if monitor_presets_sel == "CONTACT ONLY":
        monitor.insert(0.0, "CONTACT ONLY (" + today + ") :\n\n")


    if monitor_presets_sel == "Actual States":
        monitor.insert(0.0, "Actual States (All) (" + today + ") :\n\n")

    if monitor_presets_sel == "Statistics":
        monitor.insert(0.0, "Statistics (" + today + ") :\n\n")

    if monitor_presets_sel == "Contacts":
        monitor.insert(0.0, "Contacts (All) (" + today + ") :\n\n")

    if monitor_presets_sel == "Print":
        monitor.insert(0.0, "Print (All) (" + today + ") :\n\n")

    # reorder cities
    if monitor_presets_sel == "Cities":
        temp_dump_read()
        monitor.insert(0.0, "Cities (All) (" + today + ") :\n")

    # reorder countries
    if monitor_presets_sel == "Countries":
        temp_dump_read()
        monitor.insert(0.0, "Countries (All) (" + today + ") :\n")

    # reorder artists
    if monitor_presets_sel == "Artists":
        temp_dump_read()
        monitor.insert(0.0, "Artists (All) (" + today + ") :\n")

    # reorder venues
    if monitor_presets_sel == "Venues":
        temp_dump_read()
        monitor.insert(0.0, "Venues (All) (" + today + ") :\n")



    if monitor_presets_sel == "Address":
        monitor.insert(0.0, "Adresses (All) (" + today + ") :\n\n")

    if monitor_presets_sel == "Address Print":
        monitor.insert(0.0, "Adresses for Print (All) (" + today + ") :\n\n")


    if monitor_presets_sel == "Notes":
        read_notes()
        #monitor.insert(0.0, "Notes (" + today + ") :\n\n")

    if monitor_presets_sel == "E-Mails":
        monitor.insert(0.0, "E-Mails (All) (" + today + ") :\n\n")

    if monitor_presets_sel == "COMING E-Mails":
        monitor.insert(0.0, "COMING - E-Mails (" + today + ") :\n\n")

    if monitor_presets_sel == "PLAYED E-Mails":
        monitor.insert(0.0, "PLAYED - E-Mails (" + today + ") :\n\n")

    if monitor_presets_sel == "WAITING E-Mails":
        monitor.insert(0.0, "WAITING FOR MONEY - E-Mails (" + today + ") :\n\n")

    if monitor_presets_sel == "CANCELLED E-Mails":
        monitor.insert(0.0, "CANCELLED - E-Mails (" + today + ") :\n\n")

    if monitor_presets_sel == "CONTACT ONLY E-Mails":
        monitor.insert(0.0, "CONTACT ONLY - E-Mails (" + today + ") :\n\n")




# Specials for Notes
def read_notes():

    # open notes
    notefile = open("notes.txt", "r")
    tour = notefile.read()
    monitor.insert(0.0, tour)
    notefile.close()
    print("read Notes")


def write_notes(event):

    # write notes igf monitor == Notes
    monitor_presets_sel = monitor_presets.get()
    if monitor_presets_sel == "Notes":
        # save notes
        notefile = open("notes.txt", "w")
        notefile.write(monitor.get(0.0, END))
        notefile.close()
        print("write Notes")



# dump monitor into temp file, sort it, insert it back into monitor
def temp_dump_read():

    #write temp
    tempfile = open("temp.csv", "w")
    tempfile.write(monitor.get(0.0, END))
    tempfile.close()

    # sort temp.csv alphabetically via bash
    os.system("sort temp.csv -o temp.csv")

    tempfile = open("temp.csv", "r")
    tempfile2 = tempfile.read()

    monitor.delete(0.0, END)
    monitor.insert(0.0, str(tempfile2))

    tempfile.close()


# monitor export to txt file
def on_export_monitor():

    #get export text file with path
    exporttxt = exportpath_entry.get()  + monitor_presets.get() + ".txt"

    #print(monitor_presets.get())

    text_file = open(exporttxt, "w")
    text_file.write(monitor.get(0.0, END))
    text_file.close()
    print(exporttxt)

    notify(monitor_presets.get() + ".txt exported.")





# put listbox selection into spin
def select_via_listbox(event):

    gig_listbox_cursel = gig_listbox.curselection()
    gig_listbox_sel = gig_listbox_cursel[0]

    spin.delete(0, 'end')
    spin.insert(0, gig_listbox_sel+1)

    read_csv_line()



#count lines in database file
def count_lines():
    total_line_count = sum(1 for line in open(data_file))

    # set spinbox to max = lines in db
    spin.config(to=total_line_count)


#read whole file and print it to monitor
def read_whole_file():
        file = open(data_file, "r")
        filetext = file.read()

        # update monitor
        monitor.delete(1.0, END)
        monitor.insert(END, filetext)



#monitor update
def update_monitor(event):
    print("update monitor")
    read_csv_line()
    pass


# backup db
def database_backup():

    date_time = str(datetime.datetime.now())

    date_time_file = date_time[:19]
    date_time_file2 = date_time_file.replace(" ", "_")
    date_time_file3 = date_time_file2.replace(":", "-")

    #backup with date
    os.system("cp data.csv bak/" + date_time_file3 +  ".csv")

    print(date_time_file3)

    print("Database Backup")
    notify("Database Backup done.")




# read one specific line and trigger all gui updates
def read_csv_line():
    with open(data_file, 'r') as datafile:
        reader = csv.reader(datafile)
        row = [r for r in reader]

    view_row = row[int(spin.get())-1]

    date = view_row[0]
    city = view_row[1]
    venue = view_row[2]

    artist = view_row[3]

    street = view_row[4]
    nr = view_row[5]
    zip = view_row[6]
    country = view_row[7]

    contact = view_row[8]
    phone = view_row[9]
    email = view_row[10]

    info1 = view_row[11]
    info2 = view_row[12]
    info3 = view_row[13]
    info4 = view_row[14]
    info5 = view_row[15]
    info6 = view_row[16]
    info7 = view_row[17]
    info8 = view_row[18]

    fee = view_row[19]
    travelmoney = view_row[20]

    arrival = view_row[21]
    soundcheck = view_row[22]
    showtime = view_row[23]

    food = view_row[24]
    accom = view_row[25]
    breakfast = view_row[26]
    prints = view_row[27]

    addressprint1 = view_row[28]
    addressprint2 = view_row[29]
    addressprint3 = view_row[30]
    addressprint4 = view_row[31]

    statebox = view_row[32]


    # calculate final money
    fee_float = float(fee[:-4])
    travelmoney_float = float(travelmoney[:-4])

    currency = str(fee[-4:])

    money_sum = fee_float + travelmoney_float
    money_sum_string = str(money_sum) +  currency
    travelmoney_cur = str(travelmoney_float) +  currency
    #print(money_sum_string)




    clear_text()

    date_entry.insert(0, date)
    city_entry.insert(0, city)
    venue_entry.insert(0, venue)

    artist_entry.insert(0, artist)

    street_entry.insert(0, street)
    nr_entry.insert(0, nr)
    zip_entry.insert(0, zip)
    country_entry.insert(0, country)

    contact_entry.insert(0, contact)
    phone_entry.insert(0, phone)
    email_entry.insert(0, email)

    info_entry.insert(1.0, info1)
    info_entry.insert(2.0, "\n")
    info_entry.insert(2.0, info2)
    info_entry.insert(3.0, "\n")
    info_entry.insert(3.0, info3)
    info_entry.insert(4.0, "\n")
    info_entry.insert(4.0, info4)
    info_entry.insert(5.0, "\n")
    info_entry.insert(5.0, info5)
    info_entry.insert(6.0, "\n")
    info_entry.insert(6.0, info6)
    info_entry.insert(7.0, "\n")
    info_entry.insert(7.0, info7)
    info_entry.insert(8.0, "\n")
    info_entry.insert(8.0, info8)

    fee_entry.insert(0, fee)
    travelmoney_entry.insert(0, travelmoney_cur)
    moneysum_entry.configure(state="normal")
    moneysum_entry.insert(0, money_sum_string)
    moneysum_entry.configure(state="disable")

    arrival_entry.insert(0, arrival)
    soundcheck_entry.insert(0, soundcheck)
    showtime_entry.insert(0, showtime)

    food_entry.insert(0, food)
    accom_entry.insert(0, accom)
    breakfast_entry.insert(0, breakfast)
    print_entry.insert(0, prints)

    addressprint_entry.insert(1.0, addressprint1)
    addressprint_entry.insert(2.0, "\n")
    addressprint_entry.insert(2.0, addressprint2)
    addressprint_entry.insert(3.0, "\n")
    addressprint_entry.insert(3.0, addressprint3)
    addressprint_entry.insert(4.0, "\n")
    addressprint_entry.insert(4.0, addressprint4)

    statebox_entry.current(statebox) # statebox



    #count lines on each change
    count_lines()

    #read tour, insert in listbox and insert in monitor
    read_tour()

    # select right entry in gig_listbox
    spin_num = int(spin.get())-1
    gig_listbox.select_clear(0,END)
    gig_listbox.activate(spin_num)
    gig_listbox.selection_set(spin_num)
    gig_listbox.see(spin_num)


    # set monitor
    monitor_presets_sel = monitor_presets.get()
    if monitor_presets_sel == "Database Monitor":
        read_whole_file()




# when clear button is clicked
def on_clear_text():
    clear_text()

    # insert needed stuff
    date_entry.insert(0, "9999-99-99")
    fee_entry.insert(0, "0.0 EUR")
    travelmoney_entry.insert(0, "0.0 EUR")



# clear entries
def clear_text():
    artist_entry.delete(0, 'end')

    date_entry.delete(0, 'end')
    city_entry.delete(0, 'end')
    venue_entry.delete(0, 'end')

    street_entry.delete(0, 'end')
    nr_entry.delete(0, 'end')
    zip_entry.delete(0, 'end')
    country_entry.delete(0, 'end')

    contact_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')
    email_entry.delete(0, 'end')

    info_entry.delete(0.0, 'end')

    fee_entry.delete(0, 'end')
    travelmoney_entry.delete(0, 'end')
    moneysum_entry.configure(state="normal")
    moneysum_entry.delete(0, 'end')
    moneysum_entry.configure(state="disable")

    arrival_entry.delete(0, 'end')
    soundcheck_entry.delete(0, 'end')
    showtime_entry.delete(0, 'end')

    food_entry.delete(0, 'end')
    accom_entry.delete(0, 'end')
    breakfast_entry.delete(0, 'end')
    print_entry.delete(0, 'end')

    addressprint_entry.delete(0.0, 'end')

    # state entry
    statebox_entry.current(4)



def on_delete_entry_click():
    result = messagebox.askquestion("Delete Show", "Delete this Show?", icon='warning')
    if result == 'yes':
        print("show deleted")
        spinval = int(spin.get())
        listbox_size = gig_listbox.size()

        if listbox_size > 1:
            notify(str(city_entry.get()) + " - " + str(venue_entry.get()) + " - " + str(artist_entry.get()) + " deleted.")
            delete_entry(spinval)
        else:
            messagebox.showerror("Error",
                                 "It is not possible to empty the Database completely.\n\nPlease add a new Show to delete the first one.")

    else:
        print("not deleted")



def delete_entry(x):
    # when entry deleted go to the previous entry
    if int(spin.get()) > 1:
        spinnum = int(spin.get())-1
        spin.delete(0, 'end')
        spin.insert(0, spinnum)

    # delete spaces in database
    command = "sed -i " + str(x) + "d data.csv"

    print(date_entry.get(), city_entry.get(),venue_entry.get(),"removed")

    os.system(command)
    read_csv_line()


# save edit
def on_replace_click():
    notify(str(city_entry.get()) + " - " + str(venue_entry.get()) +  " - " +str(artist_entry.get()) + " saved !")

    add_to_db(1)

    #wenn added go up in spinbox (because remove_entry goes one down)
    if len(str(date_entry.get())) != 0:
        spinnum = int(spin.get()) + 1
        spin.delete(0, 'end')
        spin.insert(0, spinnum)

    read_csv_line()


# add
def on_add_click():
    notify(str(city_entry.get()) + " - " + str(venue_entry.get())+  " - " + str(artist_entry.get()) + " added !")
    add_to_db(0)
    read_csv_line()


# add entries to csv file and sort db
def add_to_db(x):

    #if CONTACT ONLY, set date to 9999-99-99
    if statebox_entry.get() == "CONTACT ONLY":
        date_entry.delete(0, END)
        date_entry.insert(0, "9999-99-99")


    #delete Text Entries after maximum line amount
    info_entry.delete(9.0, END)
    addressprint_entry.delete(5.0, END)


    # check if entry is possible
    if len(str(date_entry.get())) == 0 or len(str(fee_entry.get())) == 0 or len(str(travelmoney_entry.get())) == 0:
        messagebox.showerror("Error", "For saving/adding, you need to enter at least:\n+ a Date\n+ a Fee and its Currency\n+ a Travel Money and its Currency")


    # get all entries and write the to DB
    else:
        fields = [str(date_entry.get()), str(city_entry.get()), str(venue_entry.get()), str(artist_entry.get()),
                  str(street_entry.get()), str(nr_entry.get()), str(zip_entry.get()), str(country_entry.get()),
                  str(contact_entry.get()), str(phone_entry.get()), str(email_entry.get()),
                  str(info_entry.get(1.0,"1.0 lineend")), str(info_entry.get(2.0,"2.0 lineend")),
                  str(info_entry.get(3.0,"3.0 lineend")), str(info_entry.get(4.0,"4.0 lineend")),
                  str(info_entry.get(5.0, "5.0 lineend")), str(info_entry.get(6.0,"6.0 lineend")),
                  str(info_entry.get(7.0, "7.0 lineend")), str(info_entry.get(8.0, "8.0 lineend")),
                  str(fee_entry.get()), str(travelmoney_entry.get()),
                  str(arrival_entry.get()), str(soundcheck_entry.get()), str(showtime_entry.get()),
                  str(food_entry.get()), str(accom_entry.get()), breakfast_entry.get(), str(print_entry.get()),
                  str(addressprint_entry.get(1.0, "1.0 lineend")), str(addressprint_entry.get(2.0, "2.0 lineend")),
                  str(addressprint_entry.get(3.0, "3.0 lineend")), str(addressprint_entry.get(4.0, "4.0 lineend")),
                  str(statebox_entry.current())]

        with open(data_file,"a") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(fields)

        print(str(date_entry.get()),str(city_entry.get()),str(venue_entry.get()) + " added into database!")


        if x == 1:
            delete_entry(int(spin.get()))
        else:
            pass

        #sort data.csv alphabetically via bash
        os.system("sort data.csv -o data.csv")
        print("db alphabetically sorted")




### ------ PDF ------- ####

# import data from csv file and export to pdf
def on_export_all_button_click():
    result = messagebox.askquestion("Export", "Export All Shows to PDF ?\n\nThis will overwrite all PDFs in the working folder and can take a long time, depending of the amount of shows in the database.")
    if result == 'yes':
        import_all_data()


# import all DB data
def import_all_data():
    gig_data = csv.reader(open(data_file, "r"))

    for row in gig_data:
        read_row(row)


# import selected database row
def import_one_data():
    result = messagebox.askquestion("Export", "Export This Show to PDF ?")
    if result == 'yes':
        gig_data = csv.reader(open(data_file, "r"))
        gig_list = [d for d in gig_data]

        row_index = int(spin.get()) - 1
        sel_row = gig_list[row_index]

        read_row(sel_row)


# read data for export
def read_row(row):
    date = row[0]
    city = row[1]
    venue = row[2]

    artist = row[3]

    street = row[4]
    nr = row[5]
    zip = row[6]
    country = row[7]

    contact = row[8]
    phone = row[9]
    email = row[10]

    info1 = row[11]
    info2 = row[12]
    info3 = row[13]
    info4 = row[14]

    info5 = row[15]
    info6 = row[16]
    info7 = row[17]
    info8 = row[18]

    fee = row[19]
    travelmoney = row[20]

    arrival = row[21]
    soundcheck  = row[22]
    showtime  = row[23]
    food  = row[24]
    accom  = row[25]
    breakfast  = row[26]


    pdf_file_name = date + "_" + city + "_" + venue + "_" + artist + ".pdf"


    generate_pdf(date, city, venue, artist, street, nr, zip, country, contact, phone, email,
                 info1, info2, info3, info4, info5, info6, info7, info8, fee, travelmoney,
                 arrival, soundcheck, showtime, food, accom, breakfast, pdf_file_name)



#Build PDF
def generate_pdf(date, city, venue, artist, street, nr, zip, country, contact, phone, email,
                 info1, info2, info3, info4, info5, info6, info7, info8, fee, travelmoney,
                 arrival, soundcheck, showtime, food, accom, breakfast, pdf_file_name):

    # save export path into config.csv
    write_config()

    #calculate some stuff
    fee_float = float(fee[:-3])
    travelmoney_float = float(travelmoney[:-3])

    currency = str(fee[-3:])

    feetravelsum = str(fee_float + travelmoney_float)
    feetravelsum2 = feetravelsum + " " + currency

    # export_folder
    export_folder = str(exportpath_entry.get())
    c = canvas.Canvas(export_folder + pdf_file_name, pagesize=A4)


    # logo.
    logo = "logo/logo.png"
    c.drawImage(logo, 240, 670+pdf_ypos, width=100, height=100)


    # set font
    c.setFont("Helvetica", 12, leading=None)

    # artist
    c.drawCentredString(290, 640+pdf_ypos, artist)

    # date
    c.drawString(50, 600+pdf_ypos, "Date :  " + date)

    # city
    c.drawString(50, 580+pdf_ypos, "City :  " + city)

    # venue
    c.drawString(50, 560+pdf_ypos, "Venue :  " + venue)

    # address
    streetnr = street + " " + nr
    zipcity = zip + " " + city

    c.drawString(50, 540+pdf_ypos, "Address : ")
    c.drawString(110, 540 + pdf_ypos, streetnr)
    c.drawString(110, 520 + pdf_ypos, zipcity)
    c.drawString(110, 500 + pdf_ypos, country)

    # contact
    c.drawString(50, 460+pdf_ypos, "Contact :  " + contact)

    # phone
    c.drawString(50, 440+pdf_ypos, "Phone :  " + phone)

    # email
    c.drawString(50, 420+pdf_ypos, "E-Mail :  " + email)

    # info
    c.drawString(50, 400+pdf_ypos, "Info : ")
    c.drawString(110, 400+pdf_ypos, str(info1))
    c.drawString(110, 380+pdf_ypos, str(info2))
    c.drawString(110, 360+pdf_ypos, str(info3))
    c.drawString(110, 340+pdf_ypos, str(info4))

    c.drawString(110, 320+pdf_ypos, str(info5))
    c.drawString(110, 300+pdf_ypos, str(info6))
    c.drawString(110, 280+pdf_ypos, str(info7))
    c.drawString(110, 260+pdf_ypos, str(info8))

    # fee
    c.drawString(50, 220 + pdf_ypos, "Fee :  " + fee)

    # travel money
    c.drawString(50, 200 + pdf_ypos, "Travel Money :  " + travelmoney)

    # Fee + Travel money Sum
    c.drawString(50, 180 + pdf_ypos, "Fee + Travel :  " + feetravelsum2)

    # Arrival
    c.drawString(50, 140 + pdf_ypos, "Arrival :  " + arrival)

    # Soundcheck
    c.drawString(50, 120 + pdf_ypos, "Soundcheck :  " + soundcheck)

    # Showtime
    c.drawString(50, 100 + pdf_ypos, "Show Time :  " + showtime)

    # Food
    c.drawString(50, 80 + pdf_ypos, "Food & Drinks :  " + food)

    # Accomodation
    c.drawString(50, 60 + pdf_ypos, "Accomodation :  " + accom)

    # Breakfast
    c.drawString(50, 40 + pdf_ypos, "Breakfast :  " + breakfast)



    # today
    c.setFont("Helvetica", 8, leading=None)
    c.drawCentredString(291, 10 + pdf_ypos, today)


    # build page
    c.showPage()
    print("writting pdf file : " + str(exportpath_entry.get()) + pdf_file_name)

    notify(pdf_file_name + " exported.")

    c.save()



### ------ GUI ------- ####

root = Tk()
root.title("BookerDB")
root.geometry("830x800+300+30")
root.resizable(False, False)


#Button frame
button_frame = Frame(root)
button_frame.grid(row=0, column=1, rowspan=2)

#Logo
bitmap2 = PhotoImage(file="logo/logo_gui.png")
w = Canvas(button_frame, width=100, height=100, bd=0, highlightthickness=0, relief="ridge")
w.pack(padx=5, pady=5)
w.create_image(50,50, image=bitmap2)


#Entries
date_label = Label(button_frame, text=str(today))
date_label.pack(padx=5, pady=5)

# Spinbox
spin = Spinbox(button_frame, from_=1, to_=999, justify=CENTER, width=5, font=Font(family='Helvetica', size=20, weight='bold'), command=read_csv_line)
spin.bind("a", update_monitor)
spin.pack(padx=5, pady=5)


# Button
replace= ttk.Button(button_frame, text="Save Edit", width=19, state="normal", command= on_replace_click)
replace.pack(padx=5, pady=5, )

# Button
map= ttk.Button(button_frame, text="Show on Map", width=19, state="normal", command= show_on_map)
map.pack(padx=5, pady=5, )

# Button
#pdf= ttk.Button(button_frame, text="Export This Show to PDF", width=19, state="normal", command= import_one_data)
#pdf.pack(padx=5, pady=5, )

# Button
map= ttk.Button(button_frame, text="Web Search", width=19, state="normal", command= websearch)
map.pack(padx=5, pady=5, )

# Button
delete_button = ttk.Button(button_frame, text="Delete", width=19, command= on_delete_entry_click)
delete_button.pack(padx=5, pady=5)



# entry fields
entry_fields = Frame(root)
entry_fields.grid(row=0, column=2, rowspan=22, sticky=N, pady=5)


# Artist
artist_frame = Frame(entry_fields)
artist_label = Label(artist_frame, text="Artist(s)", justify=LEFT)
artist_label.grid(row=20, column=1, padx=0)
artist_entry = Entry(artist_frame, width=22, background=white)
artist_entry.grid(row=20, column=0, padx=5)
artist_frame.pack(fill=X)

# date
date_frame = Frame(entry_fields)
date_label = Label(date_frame, text="Date\n(YYYY-MM-DD)", justify=LEFT)
date_label.grid(row=0, column=1, padx=0)
date_entry = Entry(date_frame, width=22, background=white)
date_entry.focus_set() # set focus
date_entry.grid(row=0, column=0, padx=5)
date_frame.pack(fill=X)

# city
city_frame = Frame(entry_fields)
city_label = Label(city_frame, text="City", justify=LEFT)
city_label.grid(row=0, column=1, padx=0)
city_entry = Entry(city_frame, width=22, background=white)
city_entry.grid(row=0, column=0, padx=5)
city_frame.pack(fill=X)

# venue
venue_frame = Frame(entry_fields)
venue_label = Label(venue_frame, text="Venue", justify=LEFT)
venue_label.grid(row=0, column=1, padx=0)
venue_entry = Entry(venue_frame, width=22, background=white)
venue_entry.grid(row=0, column=0, padx=5)
venue_frame.pack(fill=X)


#label
spacer_label = Label(entry_fields, text="", font=("Helvetica", 1), justify=LEFT)
spacer_label.pack()

# street
street_frame = Frame(entry_fields)
street_label = Label(street_frame, text="Street", justify=LEFT)
street_label.grid(row=0, column=1, padx=0)
street_entry = Entry(street_frame, width=22, background=white)
street_entry.grid(row=0, column=0, padx=5)
street_frame.pack(fill=X)

# Nr./No.
nr_frame = Frame(entry_fields)
nr_label = Label(nr_frame, text="No", justify=LEFT)
nr_label.grid(row=0, column=1, padx=0)
nr_entry = Entry(nr_frame, width=22, background=white)
nr_entry.grid(row=0, column=0, padx=5)
nr_frame.pack(fill=X)

# ZIP
zip_frame = Frame(entry_fields)
zip_label = Label(zip_frame, text="ZIP", justify=LEFT)
zip_label.grid(row=0, column=1, padx=0)
zip_entry = Entry(zip_frame, width=22, background=white)
zip_entry.grid(row=0, column=0, padx=5)
zip_frame.pack(fill=X)


# Country
country_frame = Frame(entry_fields)
country_label = Label(country_frame, text="Country", justify=LEFT)
country_label.grid(row=0, column=1, padx=0)
country_entry = Entry(country_frame, width=22, background=white)
country_entry.grid(row=0, column=0, padx=5)
country_frame.pack(fill=X)


#label
spacer_label = Label(entry_fields, text="", font=("Helvetica", 1), justify=LEFT)
spacer_label.pack()


# contact name
contactname_frame = Frame(entry_fields)
contactname_label = Label(contactname_frame, text="Contact", justify=LEFT)
contactname_label.grid(row=0, column=1, padx=0)
contact_entry = Entry(contactname_frame, width=22, background=white)
contact_entry.grid(row=0, column=0, padx=5)
contactname_frame.pack(fill=X)

# contact phone
phone_frame = Frame(entry_fields)
phone_label = Label(phone_frame, text="Phone", justify=LEFT)
phone_label.grid(row=0, column=1, padx=0)
phone_entry = Entry(phone_frame, width=22, background=white)
phone_entry.grid(row=0, column=0, padx=5)
phone_frame.pack(fill=X)

# contact email
email_frame = Frame(entry_fields)
email_label = Label(email_frame, text="E-Mail", justify=LEFT)
email_label.grid(row=0, column=1, padx=0)
email_entry = Entry(email_frame, width=22, background=white)
email_entry.grid(row=0, column=0, padx=5)
email_frame.pack(fill=X)

#label
spacer_label = Label(entry_fields, text="", font=("Helvetica", 1), justify=LEFT)
spacer_label.pack()

# info Text
info_frame = Frame(entry_fields)
info_label = Label(info_frame, text="Info\n(8 lines only)", justify=LEFT)
info_label.grid(row=0, column=1, padx=0)
info_entry = Text(info_frame, width=25, height=8, background=white)
info_entry.config(wrap=WORD)
info_entry.bind("<Tab>", focus_next_window)
info_entry.grid(row=0, column=0, padx=5)
info_frame.pack(fill=X)

#label
spacer_label = Label(entry_fields, text="", font=("Helvetica", 1), justify=LEFT)
spacer_label.pack()

# fee
fee_frame = Frame(entry_fields)
fee_label = Label(fee_frame, text="Fee (N.N CCC)", justify=LEFT)
fee_label.grid(row=0, column=1, padx=0)
fee_entry = Entry(fee_frame, width=22, background=white)
fee_entry.grid(row=0, column=0, padx=5)
fee_frame.pack(fill=X)

# travel money
travelmoney_frame = Frame(entry_fields)
travelmoney_label = Label(travelmoney_frame, text="Travel Money", justify=LEFT)
travelmoney_label.grid(row=0, column=1, padx=0)
travelmoney_entry = Entry(travelmoney_frame, width=22, background=white)
travelmoney_entry.grid(row=0, column=0, padx=5)
travelmoney_frame.pack(fill=X)

# money sum
moneysum_frame = Frame(entry_fields)
moneysum_label = Label(moneysum_frame, text="SUM", justify=LEFT)
moneysum_label.grid(row=0, column=1, padx=0)
moneysum_entry = Entry(moneysum_frame, width=22, background=white, textvariable=money_sum_string, disabledforeground=black)
moneysum_entry.grid(row=0, column=0, padx=5)
moneysum_frame.pack(fill=X)


#label
spacer_label = Label(entry_fields, text="", font=("Helvetica", 1), justify=LEFT)
spacer_label.pack()


# arrival
arrival_frame = Frame(entry_fields)
arrival_label = Label(arrival_frame, text="Arrival Time", justify=LEFT)
arrival_label.grid(row=0, column=1, padx=0)
arrival_entry = Entry(arrival_frame, width=22, background=white)
arrival_entry.grid(row=0, column=0, padx=5)
arrival_frame.pack(fill=X)

# soundcheck
soundcheck_frame = Frame(entry_fields)
soundcheck_label = Label(soundcheck_frame, text="Soundcheck Time", justify=LEFT)
soundcheck_label.grid(row=0, column=1, padx=0)
soundcheck_entry = Entry(soundcheck_frame, width=22, background=white)
soundcheck_entry.grid(row=0, column=0, padx=5)
soundcheck_frame.pack(fill=X)

# showtime
showtime_frame = Frame(entry_fields)
showtime_label = Label(showtime_frame, text="Show Time", justify=LEFT)
showtime_label.grid(row=0, column=1, padx=0)
showtime_entry = Entry(showtime_frame, width=22, background=white)
showtime_entry.grid(row=0, column=0, padx=5)
showtime_frame.pack(fill=X)


# food
food_frame = Frame(entry_fields)
food_label = Label(food_frame, text="Food & Drinks", justify=LEFT)
food_label.grid(row=0, column=1, padx=0)
food_entry = Entry(food_frame, width=22, background=white)
food_entry.grid(row=0, column=0, padx=5)
food_frame.pack(fill=X)

# Accomodation
accom_frame = Frame(entry_fields)
accom_label = Label(accom_frame, text="Accomodation", justify=LEFT)
accom_label.grid(row=0, column=1, padx=0)
accom_entry = Entry(accom_frame, width=22, background=white)
accom_entry.grid(row=0, column=0, padx=5)
accom_frame.pack(fill=X)

# Breakfast
breakfast_frame = Frame(entry_fields)
breakfast_label = Label(breakfast_frame, text="Breakfast", justify=LEFT)
breakfast_label.grid(row=0, column=1, padx=0)
breakfast_entry = Entry(breakfast_frame, width=22, background=white)
breakfast_entry.grid(row=0, column=0, padx=5)
breakfast_frame.pack(fill=X)

#label
spacer_label = Label(entry_fields, text="", font=("Helvetica", 1), justify=LEFT)
spacer_label.pack()


# Print
print_frame = Frame(entry_fields)
print_label = Label(print_frame, text="Print", justify=LEFT)
print_label.grid(row=0, column=1, padx=0)
print_entry = Entry(print_frame, width=22, background=white)
print_entry.grid(row=0, column=0, padx=5)
print_frame.pack(fill=X)


# Address Print
addressprint_frame = Frame(entry_fields)
addressprint_label = Label(addressprint_frame, text="Address for Print\n(4 lines only)", justify=LEFT)
addressprint_label.grid(row=0, column=1, padx=0)
addressprint_entry = Text(addressprint_frame, width=25, height=4, background=white)
addressprint_entry.config(wrap=WORD)
addressprint_entry.bind("<Tab>", focus_next_window)
addressprint_entry.grid(row=0, column=0, padx=5)
addressprint_frame.pack(fill=X)


#Actual States
statebox_frame = Frame(entry_fields)
statebox_label = Label(statebox_frame, text="Actual State", justify=LEFT)
statebox_label.grid(row=0, column=1, padx=0)

statebox_entry = ttk.Combobox(statebox_frame, width=21)
statebox_entry.bind("<<ComboboxSelected>>", state_check)
statebox_entry["values"] = state_list
statebox_entry.current(0) # set init preset
statebox_entry.grid(row=0, column=0, padx=5, pady=10)
statebox_frame.pack(fill=X)



# Button
add_button= ttk.Button(entry_fields, text="Add", width=21, state="normal", command= on_add_click)
add_button.pack(side=TOP, anchor=W, padx=5, pady=5)

# Button
new_button = ttk.Button(entry_fields, text="Clear", width=21, command= on_clear_text)
new_button.pack(side=TOP, anchor=W, padx=5, pady=5)



#monitor
monitorframe = Frame(root)
monitorframe.grid(row=2, column=0, columnspan=2, rowspan=1, sticky=W+E+N+S, padx=5, pady=0)

xscrollbar = ttk.Scrollbar(monitorframe, orient=HORIZONTAL)
xscrollbar.pack(side=BOTTOM, fill=X)
yscrollbar = ttk.Scrollbar(monitorframe)
yscrollbar.pack(side=RIGHT, fill=Y)

monitor = Text(monitorframe, wrap=NONE, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set, width=50, height=26, padx=5, pady=5)
monitor.bind("<Tab>", focus_next_window)
monitor.pack(fill=X)
xscrollbar.config(command=monitor.xview)
yscrollbar.config(command=monitor.yview)



#Export path
exportpath_label = Label(root, text="/Working/Folder/")
exportpath_label.grid(row=3, column=0, columnspan=2, sticky=W+N+E+S)
exportpath_entry = Entry(root, width=52)
exportpath_entry.grid(row=4, column=0, columnspan=2, sticky=W+N+E+S, padx=5)

#listbox
gig_listbox_frame = Frame(root)
scrollbar = ttk.Scrollbar(gig_listbox_frame, orient=VERTICAL)
gig_listbox = Listbox(gig_listbox_frame, width= 40, height=18, yscrollcommand=scrollbar.set, selectmode=BROWSE)
gig_listbox.bind("<ButtonRelease-1>", select_via_listbox)
scrollbar.config(command=gig_listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
gig_listbox.pack(side=LEFT, fill=BOTH, expand=1)
gig_listbox_frame.grid(row=0, column=0, rowspan=1, sticky=N, padx=5, pady=5)

#monitor presets
monitor_presets = ttk.Combobox(root, width=18)
monitor_presets.bind("<Enter>", write_notes) # "Enter" == mouse hover widget
monitor_presets.bind("<<ComboboxSelected>>", update_monitor)
monitor_presets["values"] = preset_list
monitor_presets.current(0) # set init preset
monitor_presets.grid(row=1, column=0, pady=5, padx=5, sticky=W)



#menu
menubar = Menu(root)
# Database
dbmenu = Menu(menubar, tearoff=0)
dbmenu.add_command(label="DB Backup", command=database_backup)
dbmenu.add_command(label="Import from Workdir", command=import_from_workdir)
dbmenu.add_command(label="Export to Workdir", command=export_to_workdir)
dbmenu.add_separator()
dbmenu.add_command(label="Quit", command=on_quit)
menubar.add_cascade(label="Database", menu=dbmenu)

# Export
exportmenu = Menu(menubar, tearoff=0)
exportmenu.add_command(label="Export This Show to PDF", command=import_one_data)
exportmenu.add_command(label="Export All Shows to PDF", command=on_export_all_button_click)
exportmenu.add_separator()
exportmenu.add_command(label="Export Monitor to TXT", command=on_export_monitor)
menubar.add_cascade(label="Export", menu=exportmenu)

# Maps
mapsmenu = Menu(menubar, tearoff=0)
mapsmenu.add_command(label="Show on OSM *", command=show_osm)
mapsmenu.add_command(label="Show on GMaps", command=show_gmaps)
menubar.add_cascade(label="Maps", menu=mapsmenu)

# Folders
foldermenu = Menu(menubar, tearoff=0)
foldermenu.add_command(label="Open Workdir", command=open_workdir)
foldermenu.add_command(label="Open Backupdir", command=open_bakdir)
foldermenu.add_command(label="Open Rootdir", command=open_rootdir)
menubar.add_cascade(label="Folders", menu=foldermenu)

# Help
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Web Search", command=websearch)
helpmenu.add_command(label="GitHub", command=website)
helpmenu.add_command(label="About", command=about_app)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)






### ------ MAIN CALLS ------- ####

# auto backup on start
os.system("cp data.csv bak/data.startbak.csv")
print("DB Start Backup")

# on app start, read the first entry and display it
read_csv_line()

# read config file
read_config()


# mainloop
root.protocol('WM_DELETE_WINDOW', on_quit)
root.mainloop()


