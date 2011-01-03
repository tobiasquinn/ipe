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
    __songnames = []
    __index = 0

    def __init__(self, playlistfilename):
        filename = os.path.join(INPUT_DIR, playlistfilename)
        f = open(filename)
        for line in f.readlines():
            if line[0] != '#' and line.startswith("http://") != True:
                self.__songnames.append(line.strip())
        f.close()
        self.__index = len(self.__songnames)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index == 0:
            raise StopIteration
        self.__index = self.__index - 1
        return self.__songnames[self.__index]


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
pdone = 0
pinc = 100 / len(fileList)
for playlist in fileList:
    pl = Playlist(playlist)
    for song in pl:
        if song not in songtoplaylists:
            songtoplaylists[song] = [playlist]
        else:
            songtoplaylists[song].append(playlist)
    pdone = pdone + pinc
    status(pdone)

print("Found %d songs" % (len(songtoplaylists)))
# search for the common start string (path to the original files)
fcs = FindCommonStart()
pdone = 0
pinc = 100 / len(songtoplaylists)
for key in songtoplaylists.keys():
    fcs.processString(key)
    pdone = pdone + pinc
    status(pdone)
print("Common Start: %s" % (fcs.getCommon()))
