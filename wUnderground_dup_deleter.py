# Deletes duplicated values in sequence

import csv

with open("try_DELETEEQUAL.txt", "r") as fileIn, open("try_DELETE_out.txt", "w") as fileOut:

    fileIn = csv.reader(fileIn, delimiter = "\t")
    #fileOut = csv.writer(fileOut)
    allTimes = []
    all = []

    for line in fileIn:
        allTimes.append(line[0])
        all.append(line)

    ctr = 0
    numOfDups = 0

    for time in allTimes:

        if ctr == 11651:
            ctr -= 1

        elif time != allTimes[ctr + 1]:
            #numOfDups += 1
            #print(time)
            fileOut.write(str(all[ctr]) + "\n")

        ctr += 1

    #print(allTimes.__len__())
    print(numOfDups)
