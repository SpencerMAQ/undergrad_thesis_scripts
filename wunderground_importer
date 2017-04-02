import urllib.request

x, y = 13, 32

with open("pythonfromwebVER2.txt", "w") as file:
    #zz = file.readlines()
    #print(zz)
    for i in range(x):
        for j in range(y):
            if i == 0 or j ==0:
                continue

            elif i == 2 and (j == 29 or j == 30 or j == 31): #Feb28
                continue

            elif i == 4 and (j == 31): #Apr30 (Apr = 4)
                continue

            elif i == 6 and (j == 31): #Jun30 (Jun = 6)
                continue

            elif i == 9 and (j == 31): #Sep30 (Sep = 9)
                continue

            elif i == 11 and (j == 31): #Nov30 (Nov = 11)
                continue

            else:
                site = "https://www.wunderground.com/history/airport/RPLL/2013/{}/{}/DailyHistory.html?format=1".format(i, j)

            data = urllib.request.urlopen(site)

            for l in data.readlines():
               file.writelines(str(l) + "\n")
