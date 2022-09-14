import requests
import json
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk
import datetime

def jprint(obj):
    #fait une string lisible de nos résultats
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    return(text)

#response = requests.get("http://ergast.com/api/f1/drivers.json")
#jprint(response.json())
#responsepre = requests.get("http://ergast.com/api/f1/2021/driverStandings.json?limit=1000")
#jprint(responsepre.json()["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"])

def RoundResults(Year,round) :
    #donne les résultats d'un round
    response = requests.get("http://ergast.com/api/f1/" + str(Year) + "/results.json?limit=1000")
    print("Round",(round),"results in",(Year),"are :")
    for k in range(len(response.json()["MRData"]["RaceTable"]["Races"][round]["Results"])) :
        print("P%d" %(k+1),
        (response.json()["MRData"]["RaceTable"]["Races"][(round-1)]["Results"][k]["Driver"]["givenName"]),
        (response.json()["MRData"]["RaceTable"]["Races"][(round-1)]["Results"][k]["Driver"]["familyName"]))
    Menu()

def SeasonResults(Year) :
    #donne les résultats d'une saison
    response = requests.get("http://ergast.com/api/f1/" + str(Year) + "/driverStandings.json?limit=1000")
    print("Season",(Year),"results are :")
    for k in range(len(response.json()["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"])) :
        print("P%d" %(k+1),
        (response.json()["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][k]["Driver"]["givenName"]),
        (response.json()["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][k]["Driver"]["familyName"]))
    Menu()

def FindDriverId() :
    print("Write the name of the driver you want to get infos on :")
    PiloteProp = str(input())
    if PiloteProp.find(" ") == -1 :
        print("Wrong orthograph, try again")
        print("lol")
        VictoryNumber()
    else :
        replaced = PiloteProp.replace(" ","_")
    response = requests.get("http://ergast.com/api/f1/drivers.json?limit=1000")
    for k in (response.json()["MRData"]["DriverTable"]["Drivers"]) :
        if  k["url"].find(replaced) != -1 :
            driverId = (k["driverId"])
    return driverId, PiloteProp

def VictoryNumber(driverId, PiloteProp) :
    #compte le nombre de victoires d'un pilote
    response = requests.get("http://ergast.com/api/f1/drivers/" + driverId + "/results/1.json?limit=1000")
    print(PiloteProp, "won", response.json()["MRData"]["total"], "races")
    Menu()

def CountVictoryPerYear(driverId, PiloteProp) :
    YearList = {}
    count = 0
    response = requests.get("http://ergast.com/api/f1/drivers/" + driverId + "/results/1.json?limit=1000")
    for l in range(1950,2022) :   
        for k in range(len(response.json()["MRData"]["RaceTable"]["Races"])) :
            if str(l) in (response.json()["MRData"]["RaceTable"]["Races"][k]["season"]) :
                count = count + 1
        if count >= 1 :
            YearList[l] = count
            count = 0
    for k in YearList :
        print(PiloteProp, "a gagné", YearList[k], "fois en", k)
    return YearList, PiloteProp

def VictoryPlot(PiloteProp, driverId) :
    YearListFull = {}
    count = 0
    startyear = 0
    response = requests.get("http://ergast.com/api/f1/drivers/" + driverId + "/results/1.json?limit=1000")
    for l in range(1950,2022) :   
        for k in range(len(response.json()["MRData"]["RaceTable"]["Races"])) :
            if str(l) in (response.json()["MRData"]["RaceTable"]["Races"][k]["season"]) :
                count = count + 1
        if count >= 1 :
            YearListFull[l] = count
            count = 0
        else :
            YearListFull[l] = 0
            count = 0
    TestList = list(YearListFull.items())
    while TestList[2][1] == 0 and TestList[1][1] == 0 and TestList[0][1] == 0 :
        DelVar = TestList[0][0]
        del YearListFull[DelVar]
        del TestList [0]
    while TestList[-3][1] == 0 and TestList[-2][1] == 0 and TestList[-1][1] == 0 :
        DelVar = TestList[-1][0]
        del YearListFull[DelVar]
        del TestList [-1]

    x = []
    for k in YearListFull :
        x.append(k)
    xmin = min(x)
    xmax = max(x)
    y = []
    for k in YearListFull :
        y.append(YearListFull[k])
    ymin = min(y)
    ymax = max(y)

    fig, ax=plt.subplots()

    ax.plot(x, y, linewidth = 2.0)

    ax.set(xlim=((x[0]-1),(x[len(x)-1]+1)), xticks=np.arange((x[0]-1), (x[len(x)-1]+2), 3),
            ylim=((ymin - 1),(ymax +1)), yticks=np.arange((ymin - 1),(ymax + 2),1))

    plt.title(PiloteProp + "'s win graph through his career")
    plt.show()
    Menu()

def TimePlot(PiloteProp, driverId) :
    TimeDico = {}
    response = requests.get("http://ergast.com/api/f1/current/last/drivers/" + driverId + "/laps.json?limit=100")
    for k in range(len(response.json()["MRData"]["RaceTable"]["Races"][0]["Laps"])) :
        TimeDico[response.json()["MRData"]["RaceTable"]["Races"][0]["Laps"][k]["number"]] = response.json()["MRData"]["RaceTable"]["Races"][0]["Laps"][k]["Timings"][0]["time"]

    x = []
    for k in TimeDico :
        x.append(k)
    xmin = min(x)
    xmax = max(x)
    print(x)

    y = []
    for k in TimeDico :
        a = int(TimeDico[k][0])
        b = int(TimeDico[k][2] + TimeDico[k][3])
        c = int(TimeDico[k][5] + TimeDico[k][6] + TimeDico[k][7] + "000")
        j = datetime.time(minute = a, second = b, microsecond = c)
        TimeDico[k] = j
        y.append(TimeDico[k])
    ymin = min(y)
    ymax = max(y)
    print(y)
    
    plt.plot_date(x,y)

def Round() :
    Year = int((input("Which year do you want to know the results of ? ")))
    if Year < 1950 or Year > 2021 :
        print("Please type a year between 1950 and 2021")
        Round()
    else :
        round = int(input("Which round of " + str(Year) + " do you want to get results of ? "))
        RoundResults(Year,round)

def Season() :
    Year = int(input("Which season do you want to get the results of ? "))
    if Year < 1950 or Year > 2021 :
        Season()
    else :
        SeasonResults(Year)

def Menu() :
    print("What do you want to see ?")
    print("1 - Results of a certain round")
    print("2 - Results of a certain season")
    print("3 - Find the number of victories of a driver")
    print("4 - Know the number of wins of a driver for each year")
    print("5 - If you want to see the laptimes of a driver in a certain round")
    menu = input()
    if menu == "1" :
        Round()
    elif menu == "2" :
        Season()
    elif menu == "3" :
        driverId, PiloteProp = FindDriverId()
        VictoryNumber(driverId, PiloteProp)
    elif menu == "4" :
        driverId, PiloteProp = FindDriverId()
        VictoryPlot(PiloteProp, driverId)
    elif menu == "5" :
        driverId, PiloteProp = FindDriverId()
        TimePlot(PiloteProp, driverId)
    else :
        print("Please choose one of the options below by typing a number between 1 and 5")

Menu()
print("It's alive !")