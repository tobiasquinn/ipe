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
from nodes import NodePlaylist

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
        self._index -= 1
        return self._songnames[self._index]

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
# FIXME: How to deal with songs in more than one playlist...
for playlist in fileList:
    pl = Playlist(playlist)
    for song in pl:
        if song not in songtoplaylists:
            songtoplaylists[song] = set([playlist])
        else:
            songtoplaylists[song] |= set([playlist])

for s in songtoplaylists:
    print("%s : %s" % (s, songtoplaylists[s]))

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

# now we have a set of songs that describe the unique set that each song belongs to
# from this we can examine each playlist name and work out the child and parent ordering

# choose one song from each set description
uniquesongtoset = {}
psetcount = 0
for song in newsongtoplaylists.keys():
    psetcount += 1
    pset = frozenset(newsongtoplaylists[song])
    if pset not in uniquesongtoset.values():
        uniquesongtoset[song] = pset
print("Playlists sets =", psetcount)
print("Unique Playlists sets =", len(uniquesongtoset))

for p in newsongtoplaylists.values():
    print(p)
for p in uniquesongtoset.values():
    print(p)

# we want to classify the playlists by size
# use a list [length][playlists,...]
maxplaylistlength = 0
for playlists in uniquesongtoset.values():
    if len(playlists) > maxplaylistlength:
        maxplaylistlength = len(playlists)
print("MAXPLAYLISTLENGTH =", maxplaylistlength)
# classify each node
playlistslengthtoplaylists = [None] * (maxplaylistlength)
for i in range(maxplaylistlength):
    playlistslengthtoplaylists[i] = []
print(playlistslengthtoplaylists)
for playlists in uniquesongtoset.values():
    playlistslengthtoplaylists[len(playlists) - 1].append(playlists)

for i in range(maxplaylistlength):
    print("L%d:%s" % (i, playlistslengthtoplaylists[i]))

# create nodes for all our playlists
labeltonode = {}
for bigindex, pls in enumerate(playlistslengthtoplaylists):
    for s in playlistslengthtoplaylists[bigindex]:
        print("%d %s" % (bigindex, s))
        parentset = set(s)
        for t in playlistslengthtoplaylists[bigindex + 1]:
            print("Test against:", t)
#        while parentset:
#            pl = parentset.pop()
#            print("PL: ", pl)

# print out all nodes from the root node

def walktree(rootnode, visit):
    cur = rootnode
    nextChildIndex = 0

    while True:
        visit(cur)

        while nextChildIndex >= cur.getNumberOfChildren() and cur is not rootnode:
            nextChildIndex = cur.getParent().getIndex(cur) + 1
            cur = cur.getParent()

        if nextChildIndex >= cur.getNumberOfChildren():
            break

        cur = cur.getChild(nextChildIndex)
        nextChildIndex = 0

def printnode(node):
    d = node.getDepth()
    s = ''
    if (d != 0):
        s += '\\'
        s += ('==' * (d + 1))
        s += '>'
    print("%s%s" % (s, node.getLabel()))

#walktree(rootnode, printnode)
