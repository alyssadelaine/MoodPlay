import os
#use the subprocess module to call the essentia extractor that will return gaia values
import subprocess
from os import listdir
from os.path import isfile, join
import shelve
import json
import numpy as np
import math
import random

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
    dbname = 'moodplay.db'
    db = shelve.open(dbname)
    try:
        openYet = db['openYet?']
    except:
        openYet = False
        db.close()
        startup(dbname)
    try:
        print("openYet is " + str(openYet))
        songList = db['songList']
        matrix = db['similarityMatrix']
    finally:
        db.close()
    #onclickMood:
#        onclickMood(mood)
 #   onclickplay:
#        onClickPlay(dbname, songName, mood, time)
    printMatrix(matrix, songList)
    db = shelve.open(dbname)
    songList = db['songList']
    for song in songList:
        print song
    song = input('Enter a song choice')
    mood = 'None'
    time = 'morning'
    db.close()
    onClickPlay(dbname, song, mood, time)
        
    

def startup(dbname):
    songID = 0
    #first arg ("./streaming_extractor_archivemusic") = extractor to be called
    #second arg(../../../audio.mp3) = music file
    #third arg (returnfile2) = output file (from which the needed information -- gaia stuff -- will be read)
    #go into relevant directory, check for song files
    songList = []
    songStringList = []
    bigCharacteristicList = []
    
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
    #subprocess.call(["./streaming_extractor_archivemusic", "music/" + filenames[0], "audioTest"])
    # I know the following is roundabout, but it works...
    #songList = songList[:3]
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
        print("danceable is " + str(danceable))
        print("female is " + str(female))
        print("instrumental is " + str(instrumental))
        print("chord_scale is " + str(chord_scale))
        similarityList.append(chord_scale)
        genreList= ("alternative", "blues", "electronic", "funksoulrnb", "jazz", "pop", "raphiphop", "rock")
        for genre in genreList:
            item = data["highlevel"]["genre_dortmund"]["all"][genre]
            similarityList.append(item)
            print(genre + ": " + str(item))
        bigCharacteristicList.append(similarityList)

    for LIST in bigCharacteristicList:
        for item in LIST:
            print(item)

    numSongs = len(songList)
    similarityProfiles = np.empty((numSongs, numSongs))
    for song1 in songList:
        index1 = songList.index(song1)
        for song2 in songList:
            index2 = songList.index(song2)
            characteristicNum = 0
            similaritySum = 0
            while characteristicNum < numCharacteristics:
                print("index1 is " + str(index1))
                print("index2 is " + str(index2))
                print("characteristicNum is " + str(characteristicNum))
                similaritySum += pow(bigCharacteristicList[index1][characteristicNum], 2)
                similaritySum += pow(bigCharacteristicList[index2][characteristicNum], 2)
                characteristicNum += 1
            #only fill in top right triangle
            similaritySum = math.sqrt(similaritySum)
            if index1 > index2:
                similarityProfiles[index1][index2] = similaritySum
            #similarityProfiles[index2][index1] = similaritySum
    database = shelve.open(dbname)
    try:
        database['openYet?'] = True
        database['similarityMatrix'] = similarityProfiles
        database['songList'] = songList
        database['songStringList'] = songStringList
        database['bigCharacteristicList'] = bigCharacteristicList
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
        index+=1
       alternative = data["highlevel"]["genre_dortmund"]["all"]["alternative"]
        blues = data["highlevel"]["genre_dortmund"]["all"]["blues"]
        electronic = data["highlevel"]["genre_dortmund"]["all"]["electronic"]
        funksoul = data["highlevel"]["genre_dortmund"]["all"]["funksoulrnb"]
        jazz = data["highlevel"]["genre_dortmund"]["all"]["jazz"]"""
        #now can access any descriptors with data[key1][key2]
    #add all of these things to a shelve module
    #create a boolean within the shelve module that will explain that we have already made this list
        #sum of squared distances (Euclidean distance)

        #features: danceability, chords, instrumental, female, alternative, blues, electronic, folkcountry, funksoulrnb, jazz, pop, raphiphop, rock

"""
def playList(generatedList):
    for song in generatedList:
        play using mplayer"""

def createGenerationList(dbname, songName, mood, time):
    db = shelve.open(dbname)
    songList = db['songList']
    similarityMatrix = db['similarityMatrix']
    indexSongPlayed = songList.index(songName)
    totalSum = 0
    similarity = 0
    generationNumList = []
    generationSongList = []
    generationNumListToSave = []
    generationSongListToSave = []
    #create generation profile info for the similarity between the song being played and each other song
    for song in songList:
        indexSong2 = songList.index(song)
        if indexSongPlayed > indexSong2:
            similarity = similarityMatrix[indexSongPlayed][indexSong2]
        elif indexSongPlayed < indexSong2:
            similarity = similarityMatrix[indexSong2][indexSongPlayed]
        elif indexSongPlayed == indexSong2:
            continue
        print("adding song " + song + "to list")
        generationSongList.append(song)
        totalSum += similarity
        generationNum = totalSum
        generationNumList.append(generationNum)

    #add in songPicked to generationProfile to be saved
    generationSongListToSave = list(generationSongList)
    generationNumListToSave = list(generationNumList)
    totalSumToSave = totalSum
    songPlayed = songList[indexSongPlayed]
    generationSongListToSave.append(songPlayed)
    similaritySongPlayed = 5
    generationNumSongPlayed = totalSumToSave + similaritySongPlayed
    generationNumListToSave.append(generationNumSongPlayed)
    totalSumToSave += generationNumSongPlayed

    if mood != 'None':
        db[mood+'bool'] = True
        db[mood+'generationSongList'] = generationSongListToSave
        db[mood+'generationNumList'] = generationNumListToSave
        db[mood+'totalSum'] = totalSumToSave
    else:
        db[time + 'bool'] = True
        db[time+'generationSongList'] = generationSongListToSave
        db[time+'generationNumList'] = generationNumListToSave
        db[time+'totalSum'] = totalSumToSave
    print ("generation num list is: ")
    for num in generationNumList:
        print num
    generatedList = []
    helpindex = 1
    print("generation song list is: ")
    for song in generationSongList:
        print song
    print("total sum is: " + str(totalSum))
    helpindex2 = 1
    print ("generation num list is: ")
    for num in generationNumList:
        print(str(helpindex2) + " num: " + str(num))
        helpindex2 += 1
    while len(generationSongList) > 1:
        print ("try: " + str(helpindex))
        randomNum = random.uniform(0, totalSum)
        numInList = generationNumList[0]
        currIndex = 0
        print("randomNum is " + str(randomNum))
        print("numInList is: " + str(numInList))
        while randomNum > numInList:
            currIndex += 1
            numInList = generationNumList[currIndex]
            print("numInList is now: " + str(numInList))
        #now: numInList is just greater than the number generation
        print("currIndex is " + str(currIndex))
        print("numInList is " + str(numInList))
        
        if currIndex ==0:
            songPicked = generationSongList.pop(0)
        else:
            songPicked = generationSongList.pop(currIndex - 1)
        generatedList.append(songPicked)
        if currIndex ==0 and len(generationSongList) > 0:
            sumExtracted = generationNumList[currIndex + 1] - generationNumList[currIndex]
            numTakenOut = generationNumList.pop(currIndex + 1)
            indexToFix = currIndex + 1
            
        elif len(generationSongList) > 0:
            sumExtracted = generationNumList[currIndex] - generationNumList[currIndex - 1]
            print("sum Extracted was: "+ str(sumExtracted))
            numTakenOut = generationNumList.pop(currIndex)
            print("numTakenOut was " + str(numTakenOut))
            #indexToFix = currIndex
        for i in range (currIndex, len(generationNumList)):
            print("generationNumList[" + str(i) + "] was: " + str(generationNumList[i]))
            generationNumList[i] = generationNumList[i] - sumExtracted
            print("generationNumList[" + str(i) + "] is now: " + str(generationNumList[i]))
        totalSum = totalSum - sumExtracted
        print("total sum is " + str(totalSum))
        helpindex2 = 1
        print ("generation num list is: ")
        for num in generationNumList:
            print(str(helpindex2) + " num: " + str(num))
            helpindex2 += 1
        """print ("try: " + str(helpindex))
        for song in generationSongList:
            print song"""
        helpindex +=1
    generatedList.append(generationSongList[0])
    for song in generatedList:
        print(song)
    #playList(generatedList)



def onClickPlay(dbname, songName, mood, time):
    #first: play song
    #then: find other things to play
    #check to see whether there is already a generation list for this mood or time
    db = shelve.open(dbname)
    if mood != 'None':
        try:
            moodFound = db[mood]['bool']
        except:
            moodFound = False
            db.close()
            createGenerationList(dbname, songName, mood, time)
    else:
        try:
            timeFound = db[time]['bool']
        except:
            timeFound = False
            db.close()
            createGenerationList(dbname, songName, mood, time)
        
    

def printMatrix(testMatrix, songList):
    for i in range(len(songList)):
        for j in range(len(songList)):
            print("i: " + str(i) + " j: " + str(j))
            print(str(testMatrix[i][j]) + '\n')
        """print ' ',
        for i in range(len(testMatrix[1])):  # Make it work with non square matrices.
              print i,
        print
        for i, element in enumerate(testMatrix):
              print i, ' '.join(element)"""

main()


        

