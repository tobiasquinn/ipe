#!/usr/bin/python

# Traverse the directory and read in all playlist to generate a file which has
# the hierarchy of the playlist described in it

# This only looks at the top directory structure and expects all the playlists
# dumped from itunes - a utility to do this is available at:
# http://www.ericdaugherty.com/dev/itunesexport/

# For now the format of the file will be a null means an indent
# FIXME: this should be changed for unicode

import os, sys, string
from findcommon import FindCommonStart

INPUT_DIR = "playlists"

# FIXME: this ignores http references
class Playlist:
    def __init__(self, playlistfilename):
        self._songnames = []    
        filename = os.path.join(INPUT_DIR, playlistfilename)
        f = open(filename)
        for line in f.readlines():
            if line[0] != '#' and line.startswith("http://") != True:
                self._songnames.append(line.strip())
        f.close()
        self._index = len(self._songnames)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index == 0:
            raise StopIteration
        self._index = self._index - 1
        return self._songnames[self._index]


#pl = Playlist("Jazz Masters 41.m3u")
#for song in pl:
#    print(song)
#sys.exit()

print ("Input directory: %s" % (INPUT_DIR))
fileList = []
for root, sub, files in os.walk(INPUT_DIR):
    for file in files:
        fileList.append(file)

print ("Found %d playlists" % (len(fileList)))

# find the unique part of each song name
# this assumes all the music is stored from the same root path
def status(percent):
    sys.stderr.write("%3d%%\r" % percent)
    sys.stdout.flush()

uniquepath = ''
songtoplaylists = {}

# map songs to all the playlists they are in
# this is done by creating a dictionary of songname to playlist name
for playlist in fileList:
    pl = Playlist(playlist)
    for song in pl:
        if song not in songtoplaylists:
            songtoplaylists[song] = [playlist]
        else:
            songtoplaylists[song].append(playlist)

print("Found %d songs" % (len(songtoplaylists)))
# search for the common start string (path to the original files)
fcs = FindCommonStart()
for key in songtoplaylists.keys():
    fcs.processString(key)
commonsongstart = fcs.getCommon()
print("Common Start: %s" % (commonsongstart))

# remove the common start string from each song entry
renamesong = lambda songname: songname[len(commonsongstart):]
newsongtoplaylists = dict((renamesong(key), value) for (key, value) in songtoplaylists.items())

testsong = ["Diana Krall/Love Scenes [Europe]/11 My Love Is.m4a",
           "Compilations/I Hear Music - Cleo Laine & John Dankworth - A Celebration Of Their Life & Work - [Disc 2] John - Big Band & The Movies/2-06 African Waltz.m4a",
           "Alicia De Larrocha/Albéniz (I)_ Iberia, Navarra, Suite Española [Disc 2]/2-12 Albéniz (I)_ Suite Española - Castilla (Seguidillas).m4a"]
for song in testsong:
    print("SONG: %s" % song)
    print("\t%s" % newsongtoplaylists[song])

# now there is a map of songs to playlists which we can build the playlist tree
# from as a child of a parent playlist contains all the songs of the node
# underneath

