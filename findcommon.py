#!/usr/bin/python

class FindCommonStart:
    # feed a number of strings in and allow the return of the common start string
    __common = None

    def processString(self, string):
        if self.__common == None:
            self.__common = string
        elif string.startswith(self.__common):
            return
        else:
            # find the furthest common piece of the input string
            slicepoint = len(self.__common)
            while (string.find(self.__common[:slicepoint]) != 0):
                slicepoint -= 1
            self.__common = self.__common[:slicepoint]

    def getCommon(self):
        return self.__common

if __name__ == '__main__':
    def runTest(strings):
        fcs = FindCommonStart()
        c = 0
        for s in strings:
            fcs.processString(s)
            print ("T%d:%s" % (c, fcs.getCommon()))
            c += 1
        print("Result:%s" % (fcs.getCommon()))

    print("FindCommonStart Tests")
    testStrings = ["This is a test blah blah deblah",
                  "This is a ",
                  "This",
                  "This is a test blah blah"]
    runTest(testStrings)
    testStrings.reverse()
    runTest(testStrings)
