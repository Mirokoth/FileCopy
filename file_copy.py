'''
The goal for this script is to automate the copying of weekly TV shows
Early test version by Rhyse Allan 06/2016
'''
import sys
import os
import json
import time
from time import strftime
from datetime import date
from subprocess import call
from os.path import join

print "File copy V0.1.0\n Rhyse Allan"

blank_moved_database = {
    "shows_moved": [],
    "movies_moved": []
}

blank_json_database = {
	"root_shows_ignore": [],
	"dest_shows": [],
	"dest_shows_ignore": [],
	"root_shows": []
}

blank_json_settings = {
	"input": [],
	"output": [],
    "movie_input": [],
    "movie_output": [],
    "file_ext": [".mkv", ".avi", ".mp4"],
    "log_loc": ""
}

set_json_moved = 'shows_moved.json' #Moved files database
set_json_setting = 'settings.json' #Settings JSON file name
set_json_database = 'showsdb.json' #TV Shows Database JSON file name


def zero_db():
    print "\nEnsure that you do want to wipe the database, you can NOT get this back."
    option = str.upper(raw_input("Please select database to reset - Folder Settings (F) - Shows DB (S) - Shows Moved (M) - Exit (E): "))
    if option == 'F':
        with open(set_json_setting, 'w') as json_set:
            json.dump(blank_json_settings, json_set)
            json_set.close()
            print "%s reset" % set_json_setting
            setting(set_json_setting)
    if option == 'S':
        with open(set_json_database, 'w') as json_db:
            json.dump(blank_json_database, json_db)
            json_db.close()
            print "%s reset" % set_json_database
            setting(set_json_setting)
    if option == 'M':
        with open(set_json_moved, 'w') as json_move:
            json.dump(blank_moved_database, json_move)
            json_move.close()
            print "%s reset" % set_json_moved
            setting(set_json_setting)
    else:
        setting(set_json_setting)

def setting(settings):
    option = raw_input("\nSettings Menu: \nView settings (V) - Modify settings (M) - Update Database of Shows (U) - Wipe a Database (W) -  Return to main menu (R): ")
    option = str.upper(option)
    if option == 'V': #View current settings
        with open(settings) as json_data:
            dat = json.load(json_data) #load json settings into dat
            print "\nCurrent settings configuration -"
            for S in dat:
                print "%s: %s" % (S, dat[S])
        with open(set_json_database) as json_data:
            dat = json.load(json_data)
            print "\nCurrent monitoring shows -"
            for S in dat['root_shows']:
                print "%s" % S
            setting(set_json_setting)
    elif option == 'M': #Modify Settings JSON file
        print "\nTo leave the current settings as it is leave the entry blank\n"
        input = raw_input("Please enter Show directory to copy from: ")
        output = raw_input("\nPlease enter Show Output Directory: ")
        mov_input = raw_input("\nPlease enter Movie directory to copy from: ")
        mov_output = raw_input("\nPlease enter Movie output directory: ")
        log_output = raw_input("Where were you like to store the log files? ")
        with open(settings, 'r') as json_data:
            dat = json.load(json_data) #load json settings into dat
            print "\n>>	Old %s		%s" % (settings, dat)
            dat['input'] = input
            dat['output'] = output
            dat['movie_input'] = mov_input
            dat['movie_output'] = mov_output
            dat['log_loc'] = log_output
            print ">>	New %s		%s\n\n" % (settings, dat)
            json_data.close()
        with open(settings, 'w') as json_data: #open Settings JSON in write
            json.dump(dat, json_data)	#export user provided settings back into Settings JSON
            json_data.close() #close connection
            print "Updated %s\n\n" % settings
        input = str.upper(raw_input("\nYou have changed directory settings, would you like to rebuild the database? (Y/N): "))
        if input == 'Y':
            db_update(set_json_setting, set_json_database)
        setting(set_json_setting)
    elif option == 'R': #Return to main menu
        menu()
    elif option == 'U':
        db_update(set_json_setting, set_json_database)
    elif option == 'W':
        zero_db()
    else:
        print "Sorry, I did not recognise your selection. Ensure to enter only the letter."
        setting(set_json_setting)

def db_update(settings, database):		#settings and database should be the two JSON files
    option = str.upper(raw_input("\nUpdate database (U) - Wipe Database (W) - Return to settings (R) - Add destination files to shows copied (A): "))
    if option == 'U': #Update database
        with open(settings) as json_set: #Open Settings JSON
            with open(database) as json_data: #Open Database JSON
                data = json.load(json_data) #Write Database JSON to data
                set = json.load(json_set) #write Settings JSON to set
                for files in os.listdir(set['input']):
                    if files not in data['root_shows'] and files not in data['root_shows_ignore']: #Check if folder is not in the database already and not being ignored
                        confirm = str.upper(raw_input("\n%s is not in your database of shows, Would you like to add it? (Y/N): "% files))
                        if confirm == 'Y':		#Add folder to database
                            data['root_shows'].append(files)
                            print "Added %s to database\n" % files
                        if confirm == 'N':
                            confirm = str.upper(raw_input("Would you like to add this to your 'Ignore' list? (Y/N): "))
                            if confirm == 'Y':	#Add folder to ignore database
                                data['root_shows_ignore'].append(files)
                                print "Added %s to ignore list\n" % files
                        elif confirm != 'Y' and confirm != 'N': #If fat fingered ignore - Waiting for better option
                            print "Ensure that you enter either Y or N, ignoring %s" % files
                    else:
                        print "Skipping %s..." % files
            json_data.close()
        with open(database, 'w') as json_data:
            json.dump(data, json_data)
            json_data.close()
            print "\nTV Show database has been updated"
            setting(set_json_setting)
    if option == 'W':
        option = raw_input("This will wipe the database, please confirm by entering 'agree': ")
        if option == 'agree':
            with open(database, 'r') as json_data:
                data = json.load(json_data)
                json_data.close()
            data['root_shows_ignore'] = []
            data['root_shows'] = []
            print "\nWiping database...\n"
            with open(database, 'w') as jason_data:
                json.dump(data, jason_data)
                json_data.close()
            setting(set_json_setting)
        elif option != 'agree':
            setting(set_json_setting)
    if option == 'A':
        with open(set_json_moved) as json_mov:
            mov = json.load(json_mov)
        with open(settings) as json_set: #Open Settings JSON
            set = json.load(json_set)
            tmp = {"directory": [], "deeper": []}
            print "Adding files from %s" % set['output']
            for files in os.listdir(set['output']):
                tmp['directory'].append(join(set['output'], files))
            for dir in tmp['directory']:
                if "." in dir:
                    pass
                else:
                    for files in os.listdir(dir):
                        tmp['deeper'].append(join(dir, files))
            for folder in tmp['deeper']:
                for root, dir, files in os.walk(folder):
                    for file in files:
                        mov['shows_moved'].append(file)
        with open(set_json_moved, 'w') as json_mov:
            json.dump(mov, json_mov)
            json_mov.close()
        print "Files added..."
        time.sleep(2)
    if option != 'U' or option != 'W' or option != 'R' or option != 'A':
        setting(set_json_setting)

def create_dir(settings):       #Creates the directories to move the files to.
    print "Creating/confirming output directories...\n"
    time.sleep(2)
    with open(set_json_database) as json_data: #Open Database of shows to copy and set to json_data
        _dat = json.load(json_data)
        json_data.close()
    with open(settings) as json_set: #Open settings JSON and set to json_set
        _set = json.load(json_set)
        json_set.close()
    for show in _dat['root_shows']:
        try:
            os.mkdir(_set['output'] + "\\" + show) #Creates the folder for the show if it does not exist.
        except OSError as e:
            pass
        for root, dirs, files in os.walk(_set['input'] + "\\" + show):  #Creates directories under the show folder, season 1 etc
            for folder in dirs:
                try:
                    os.mkdir(_set['output'] + "\\" + show + "\\" + folder)
                    print "Created %s\\%s" % (show, folder)
                except OSError as e:
                    pass
    print "\nFolders setup... \nNow moving onto file copying...\n"
    time.sleep(2) #Pause 2 seconds

def file(settings, database, moved, both = False):
    create_dir(set_json_setting)
    _tmp = {"file_list": [],"files": [], "dir": [], "ignore": [], "dest": [], "dest_dir": []}    #Temporary list
    with open(settings) as json_set: #Open settings JSON and set to json_set
        _set = json.load(json_set)
        json_set.close()
    with open(database) as json_data: #Open Database of shows to copy and set to json_data
        _dat = json.load(json_data)
        json_data.close()
    with open(moved) as json_move: #Open database of files moved and set to json_move
        _mov = json.load(json_move)
        json_move.close()
    count = 0
    _dir = {"root_dir": [], "file_list": []} #Variable with temporary lists to store data working with?
    for D in _dat['root_shows']: #For each Show we are working with in showsdb.json
        _dir['root_dir'].append(join(_set['input'], D)) #Append the directory to the front of it and store it
    for show in _dir['root_dir']:   #For each show (now including full path)
        for root, dirs, files in os.walk(show): #walk Show dir and get Root, Directory and Files
            for name in dirs: #get each directory
                _tmp['dir'].append(join(root, name)) #join the root and directory names together, store in _tmp
    for F in _tmp['dir']:
        _tmp[F] = []
        for root, dirs, files in os.walk(F):
            _tmp[F].append(files)
            for X in files:
                if X in _mov['shows_moved']:
                        _tmp['ignore'].append(F + "\\" + X)
                else:
                    for ext in _set["file_ext"]:
                        if ext in X[-4:]:
                            count = count =+ 1
                            _tmp['file_list'].append(F + "\\" + X)
                            _tmp['files'].append(X)
    for x in _tmp['file_list']:
        call('esentutl /y "%s" /d "%s"' % (x, join(_set['output'], x[len(_set['input']) + 1:])), shell=True)
    if count == 0:
        time.sleep(2)
        print "\nShows are up to date...\n"
    with open(moved, 'w') as move:
        for file in _tmp['files']:
            _mov['shows_moved'].append(file)
        json.dump(_mov, move)
        move.close()
    time.sleep(1)
    print "Updating New Shows.txt"
    text = join(_set['log_loc'], "New Shows.txt")
    with open(text, 'a') as new_shows:
        for files in _tmp['files']:
            new_shows.write(files + " " + strftime("%a - %d, %B, %Y") + "\n")
        new_shows.close()
    print "\nShow copy complete!....  \n"
    time.sleep(2)
    if both == True:
        movie(set_json_setting, set_json_database, set_json_moved)
    else:
        menu()

def movie(settings, database, moved):
    with open(settings) as json_set: #Open settings JSON and set to json_set
        _set = json.load(json_set)
        json_set.close()
    with open(database) as json_data: #Open Database of shows to copy and set to json_data
        _dat = json.load(json_data)
        json_data.close()
    with open(moved) as json_move: #Open database of files moved and set to json_move
        _mov = json.load(json_move)
        json_move.close()
    count = 0
    _tmp = {"Movie_List": [], "files": [], "move_list_final": []}
    for file in os.listdir(_set['movie_input']):
        for ext in _set['file_ext']:
            if ext in file[-4:]:
                if file not in _mov['movies_moved']:
                    count =+ 1
                    _tmp['Movie_List'].append(join(_set['movie_input'], file))
                    _mov['movies_moved'].append(file)
                    _tmp['files'].append(file)
        for root, dir, files in os.walk(join(_set['movie_input'], file)):
            x = join(_set['movie_input'], file)
            for y in files:
                for ext in _set['file_ext']:
                    if ext in y[-4:]:
                       if y not in _mov['movies_moved']:
                            count =+1
                            _tmp['Movie_List'].append(join(x, y))
                            _mov['movies_moved'].append(y)
                            _tmp['files'].append(y)
    print "\nMovie copy time!\n"

    for x in _tmp['Movie_List']:
        choice = str.upper(raw_input("Would you like to add %s? Y or N: " % x))
        if choice == "Y":
            _tmp['move_list_final'].append(x)
        else:
            print "\nSkipping %s" % x
    for x in _tmp['move_list_final']:
        call('esentutl /y "%s" /d "%s"' % (x, join(_set['movie_output'], os.path.split(x)[1])), shell=True)
    if count == 0:
        time.sleep(2)
        print "\nMovies are up to date...\n"
    text = join(_set['log_loc'], "New Movies.txt")
    with open(text, 'a') as new_movies:
        for files in _tmp['files']:
            new_movies.write(os.path.split(files)[1] + " " + strftime("%a - %d, %B, %Y") + "\n")
        new_movies.close()
    with open(moved, 'w') as move:
        json.dump(_mov, move)
        move.close()
    print "Complete, returning to main menu"
    time.sleep(2)
    menu()

def menu():
    option = str.upper(raw_input("\nMenu options: \nSettings (S) - TV Show Copy (T) - Movie Copy (M) - Both (TM) - Exit (E): "))
    if option == 'S':
        setting(set_json_setting)
    elif option == 'T':
        both = False
        file(set_json_setting, set_json_database, set_json_moved)
    elif option == 'E':
        print "Exiting File Copy..."
        exit()
    elif option == 'M':
        movie(set_json_setting, set_json_database, set_json_moved)
    elif option == 'TM':
        file(set_json_setting, set_json_database, set_json_moved, both = True)
    else:
        print "Sorry, I did not recognise your selection. Ensure to enter only the letter."
        menu()

menu()
