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

# NOTE: this is reusing the fileList from the directory walk above and expects it to have not changed
for playlist in fileList:
    print(playlist)
    for s in songtoplaylists:
        if playlist in songtoplaylists[s]:
            print("%s IN %s" % (playlist, s))

sys.exit()

# We want to turn each song to playlists in a set
# then produce a set so that we have a unqiue list of all playlist paths
# which we can then convert into a tree
uniqueset = set()
psetcount = 0
for playlists in newsongtoplaylists.values():
    psetcount += 1
    pset = frozenset(playlists)
    if pset not in uniqueset:
        uniqueset.add(pset)
print("Playlists sets =", psetcount)
print("Unique Playlists sets =", len(uniqueset))

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

rootnode = NodePlaylist("Root")

# we want to classify the playlists by size
# use a list [length][playlists,...]
maxplaylistlength = 0
for playlists in uniqueset:
    if len(playlists) > maxplaylistlength:
        maxplaylistlength = len(playlists)
print("MAXPLAYLISTLENGTH =", maxplaylistlength)

# we have a root node by default there for maxplaylistslength and the root node
sizetoplaylists = [None] * (maxplaylistlength + 1)
for i in range(maxplaylistlength + 1):
    sizetoplaylists[i] = []
print(sizetoplaylists)
for playlists in uniqueset:
    print(len(playlists))
    sizetoplaylists[len(playlists)].append(playlists)

for i in range(len(sizetoplaylists)):
    print("Length %d PLS %s" % (i, sizetoplaylists[i]))

walktree(rootnode, printnode)
