import os
#use the subprocess module to call the essentia extractor that will return gaia values
import subprocess
from os import listdir
from os.path import isfile, join

#lists to be stored in shelve
#list of songs
#list(songs)
#lists of similarities
#list(similarityRhythm)
#etc. for all the other features we want
#list of all moods
#list(moods)
#list of times of day accounted for: morning, afternoon, late afternoon, evening, early morning
#list(times)

def main():
    #check in the shelve module to see if this is the first time MoodPlay has been used on this computer
    #if so:
    startup()
    #onclickMood:
#        onclickMood(mood)
    
    

def startup():
    songID = 0
    #first arg ("./streaming_extractor_archivemusic") = extractor to be called
    #second arg(../../../audio.mp3) = music file
    #third arg (returnfile2) = output file (from which the needed information -- gaia stuff -- will be read)
    #go into relevant directory, check for song files
    songList = []
    songStringList = []
    
    thisDir = os.getcwd()
    songID = 0
    #print(thisDir)
    musicDir = thisDir + '/music'
    print(musicDir)
    #os.listdir(musicDir)
    filenames = next(os.walk(musicDir))[2]
    for filename in filenames:
        songList.append(filename)
        print filename
    """for f in thisDir:
        print("in for loop, f is " + f)
        if isfile(f):
            songList.append(f)"""
    # subprocess.call(["./streaming_extractor_archivemusic", "music/" + filenames[0], "audioTest"])
    # I know the following is roundabout, but it works...
    for song in songList:
        songString = str(song) + str(songID) + ".json"
        songStringList.append(songString)
        print("song equals " + song + " and songID equals " + str(songID))
        subprocess.call(["./streaming_extractor_archivemusic", "music/" + filenames[songID], songString])
        songID+=1
        #now: go into songString, and create an array for that song with its properties
        #then add that to the big list of songs
        json_data = open(songString)
        data = json.load(json_data)
        #now can access any descriptors with data[key1][key2]
    #add all of these things to a shelve module
    #create a boolean within the shelve module that will explain that we have already made this list
        #sum of squared distances (Euclidean distance)

"""def onclickMood:
    if mood in moods:"""

main()


        

