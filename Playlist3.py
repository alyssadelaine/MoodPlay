import os
#use the subprocess module to call the essentia extractor that will return gaia values
import subprocess
from os import listdir
from os.path import isfile, join
import shelve
import numpy as np

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
numCharacteristics = 12

#now: test code, and debug startup process before moving onto generation

def main():
    #check in the shelve module to see if this is the first time MoodPlay has been used on this computer
    #if so:
    startup()
    #onclickMood:
#        onclickMood(mood)
    db = shelve.open('moodplay.db')
    try:
        matrix = s[similarityMatrix]
    finally:
        db.close()
    printMatrix(matrix)
    
    

def startup():
    songID = 0
    #first arg ("./streaming_extractor_archivemusic") = extractor to be called
    #second arg(../../../audio.mp3) = music file
    #third arg (returnfile2) = output file (from which the needed information -- gaia stuff -- will be read)
    #go into relevant directory, check for song files
    songList = []
    songStringList = []
    bigCharacteristicsList = []
    
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
        similarityList = []
        songString = str(song) + str(songID) + ".json"
        songStringList.append(songString)
        print("song equals " + song + " and songID equals " + str(songID))
        subprocess.call(["./streaming_extractor_archivemusic", "music/" + filenames[songID], songString])
        songID+=1
        #now: go into songString, and create an array for that song with its properties
        #then add that to the big list of songs
        json_data = open(songString)
        data = json.load(json_data)
        danceable = data["highlevel"]["danceability"]["all"]["danceable"]
        similarityList.append(danceable)
        female = data["highlevel"]["gender"]["all"]["female"]
        similarityList.append(female)
        instrumental = data["highlevel"]["voice_instrumental"]["all"]["instrumental"]
        similarityList.append(instrumental)
        chord_scale = data["tonal"]["chords_scale"]
        if chord_scale == "major":
            chord_scale = 1
        else:
            chord_scale = 0
        similarityList.append(chord_scale)
        genreList= ("alternative", "blues", "electronic", "funksoulrnb", "jazz", "pop", "raphiphop", "rock")
        for genre in genreList:
            item = data["highlevel"]["genre_dortmund"]["all"][genre]
            similarityList.append(item)
        bigCharacteristicsList.append(similarityList)

    numSongs = len(songList)
    similarityProfiles = np.empty((numSongs, numSongs))
    for song1 in songList:
        index1 = songList.index(song1)
        for song2 in songList:
            index2 = songList.index(song2)
            characteristicNum = 0
            similaritySum = 0
            while characteristicNum <= numCharacteristics:
                similaritySum += bigCharacteristicList[index1][characteristicNum] + bigCharacteristicList[index2][characteristicNum]
                characteristicNum += 1
            #only fill in top right triangle
            if index1 > index2:
                similarityProfiles[index1][index2]
            else:
                similarityProfiles[index2][index1]
    database = shelve.open('moodplay.db')
    try:
        database['similarityMatrix'] = similarityProfiles
    finally:
        database.close()
    

    """
    #index of the song whose similarity list we are computing
    index1 = 0
    #index of the songs we're comparing it to
    index2 = 0
    noCompare = 0
    Sum = 0
    for song in songList:
        noCompare = songList.index(song)
        if (index2 != noCompare):
            characteristicNum = 0
            for characteristic in bigCharacteristicsList[index2]:
                Sum += characteristic^2 + bigCharacteristicsList[index1][characteristicNum]
                characteristicNum += 1
        index+=1"""
            
 """       alternative = data["highlevel"]["genre_dortmund"]["all"]["alternative"]
        blues = data["highlevel"]["genre_dortmund"]["all"]["blues"]
        electronic = data["highlevel"]["genre_dortmund"]["all"]["electronic"]
        funksoul = data["highlevel"]["genre_dortmund"]["all"]["funksoulrnb"]
        jazz = data["highlevel"]["genre_dortmund"]["all"]["jazz"]"""
        #now can access any descriptors with data[key1][key2]
    #add all of these things to a shelve module
    #create a boolean within the shelve module that will explain that we have already made this list
        #sum of squared distances (Euclidean distance)

        #features: danceability, chords, instrumental, female, alternative, blues, electronic, folkcountry, funksoulrnb, jazz, pop, raphiphop, rock

"""def onclickMood:
    if mood in moods:"""

def printMatrix(testMatrix):
        print ' ',
        for i in range(len(matrix[1])):  # Make it work with non square matrices.
              print i,
        print
        for i, element in enumerate(testMatrix):
              print i, ' '.join(element)

main()


        

