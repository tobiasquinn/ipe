class FindCommonStart:
    # feed a number of strings in and allow the return of the common start string
    __common = None

    def processString(self, string):
        if self.__common == None:
            self.__common = string
        elif string.startswith(self.__common):
            return
        else:
            print("New common start current count is %d" % (len(self.__common)))
            # search for the common start string

    def getCommon(self):
        return self.__common
