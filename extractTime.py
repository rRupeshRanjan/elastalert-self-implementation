import sys, os

def getExtractedTime(timeVar, timeVarName):
    if timeVar[len(timeVar)-1] in ['h','m','s']:
        extractedTime = timeVar[:len(timeVar)-1]
        if timeVar[len(timeVar)-1]=='h':
            extractedTime = int(extractedTime)*3600
        elif timeVar[len(timeVar)-1]=='m':
            extractedTime = int(extractedTime)*60
        elif timeVar[len(timeVar)-1]=='s':
            extractedTime = int(extractedTime)
        else:
            print("Incorrect timestamp passed for " + timeVarName + ": ", timeVar)
            exit()
    else:
        print("Incorrect timestamp passed for " + timeVarName +": ", timeVar)
        exit()

    return extractedTime