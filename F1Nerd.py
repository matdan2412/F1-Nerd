import requests
import json
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk
import datetime
import fastf1
fastf1.Cache.enable_cache('.\cache')
import fastf1.core
import fastf1.plotting
import pandas
from timple.timedelta import strftimedelta
fastf1.plotting.setup_mpl()
import ipywidgets

def jprint(obj):
    #fait une string lisible de nos résultats
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    return(text)

#FastF1
"""
#recover session infos
session = fastf1.get_session(2022,18,'Q')
session.load()
VerLap = session.laps.pick_driver('VER')
VerFastest = VerLap.pick_fastest().get_car_data().add_distance()

LecLap = session.laps.pick_driver('LEC')
LecFastest = LecLap.pick_fastest().get_car_data().add_distance()
#LapListVer = LapListVer.loc[LapListVer['IsAccurate'] == True]

#plot
fig, ax = plt.subplots(4)

ax[0].plot(VerFastest['Distance'], VerFastest['Throttle'], color=fastf1.plotting.driver_color('ver'))
ax[0].plot(LecFastest['Distance'], LecFastest['Throttle'], color=fastf1.plotting.driver_color('lec'))
ax[0].set(xlabel = 'Distance', ylabel = 'Throttle')
ax[0].legend(loc="upper center")

ax[1].plot(VerFastest['Distance'], VerFastest['Brake'], color=fastf1.plotting.driver_color('ver'))
ax[1].plot(LecFastest['Distance'], LecFastest['Brake'], color=fastf1.plotting.driver_color('lec'))
ax[1].set(xlabel = 'Distance', ylabel = 'Braking')
ax[1].legend(loc="upper center")

ax[2].plot(VerFastest['Distance'], VerFastest['Speed'], color=fastf1.plotting.driver_color('ver'))
ax[2].plot(LecFastest['Distance'], LecFastest['Speed'], color=fastf1.plotting.driver_color('lec'))
ax[2].set(xlabel = 'Distance', ylabel = 'Speed')
ax[2].legend(loc="upper center")

ax[3].plot(VerFastest['Distance'], VerFastest['RPM'], color=fastf1.plotting.driver_color('ver'))
ax[3].plot(LecFastest['Distance'], LecFastest['RPM'], color=fastf1.plotting.driver_color('lec'))
ax[3].set(xlabel = 'Distance', ylabel = 'RPM')
ax[3].legend(loc="upper center")

plt.suptitle(f"Fastest lap comparison between Leclerc and Verstappen \n "
             f"{session.event['EventName']} {session.event.year}")

plt.show()
"""
#api ergast
"""
#response = requests.get("http://ergast.com/api/f1/drivers.json")
#jprint(response.json())
#responsepre = requests.get("http://ergast.com/api/f1/2021/driverStandings.json?limit=1000")
#jprint(responsepre.json()["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"])
"""

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

def TimePlotOld(PiloteProp, driverId) :
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

def QualiPlot() :
    Year = int(input("From which year do you want to see the results ? "))
    Round = int(input("From which round ? "))
    
    #recover session infos
    session = fastf1.get_session(Year,Round,'Q')
    session.load()
    drivers = pandas.unique(session.laps['Driver'])
    print(drivers)
    
    #recover fastest lap for each driver
    fastest_laps = []
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        fastest_laps.append(drvs_fastest_lap)
    fastest_laps = fastf1.core.Laps(fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
    print(fastest_laps)
    
    #create the delta with the pole_lap
    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']
    print(fastest_laps)
    
    #set bar colors with team colors
    team_colors = []
    for index, lap in fastest_laps.iterlaps():
        color = fastf1.plotting.team_color(lap['Team'])
        team_colors.append(color)
        
    #plot
    fig, ax = plt.subplots()
    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
            color=team_colors, edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])

    # show fastest at the top
    ax.invert_yaxis()

    # draw vertical lines behind the bars
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

    #set the title
    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')
    plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
                f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

    plt.show()
    
def AbuDhabiPlot() :
    
    #recover session infos
    session = fastf1.get_session(2021,'Abu Dhabi','R')
    session.load()
    LapListHam = session.laps.pick_driver('HAM')
    LapListHamLap1 = LapListHam.loc[LapListHam['LapNumber']==58].get_car_data().add_distance()
    #LapListHam = LapListHam.loc[LapListHam['IsAccurate'] == True]

    LapListVer = session.laps.pick_driver('VER')
    LapListVerLap1 = LapListVer.loc[LapListVer['LapNumber']==58].get_car_data().add_distance()
    #LapListVer = LapListVer.loc[LapListVer['IsAccurate'] == True]

    #plot
    fig, ax = plt.subplots(4)

    ax[0].plot(LapListHamLap1['Distance'], LapListHamLap1['Throttle'], color=fastf1.plotting.driver_color('ham'))
    ax[0].plot(LapListVerLap1['Distance'], LapListVerLap1['Throttle'], color=fastf1.plotting.driver_color('ver'))
    ax[0].set(xlabel = 'Distance', ylabel = 'Throttle')
    ax[0].legend(loc="upper center")

    ax[1].plot(LapListHamLap1['Distance'], LapListHamLap1['Speed'], color=fastf1.plotting.driver_color('ham'))
    ax[1].plot(LapListVerLap1['Distance'], LapListVerLap1['Speed'], color=fastf1.plotting.driver_color('ver'))
    ax[1].set(xlabel = 'Distance', ylabel = 'Speed')
    ax[1].legend(loc="upper center")

    ax[2].plot(LapListHamLap1['Distance'], LapListHamLap1['RPM'], color=fastf1.plotting.driver_color('ham'))
    ax[2].plot(LapListVerLap1['Distance'], LapListVerLap1['RPM'], color=fastf1.plotting.driver_color('ver'))
    ax[2].set(xlabel = 'Distance', ylabel = 'RPM')
    ax[2].legend(loc="upper center")

    ax[3].plot(LapListHam['LapNumber'], LapListHam['LapTime'], color=fastf1.plotting.driver_color('ham'))
    ax[3].plot(LapListVer['LapNumber'], LapListVer['LapTime'], color=fastf1.plotting.driver_color('ver'))
    ax[3].set(xlabel = 'Lap Number', ylabel = 'Lap Time')
    ax[3].legend(loc="upper center")

    plt.suptitle(f"Lap 58 Comparison between Hamilton Verstappen \n "
                f"And all race lap by lap timing comparison \n "
                f"during the {session.event['EventName']} {session.event.year} Race")

    plt.show()

def Menu() :
    print("What do you want to see ?")
    print("1 - Results of a certain round")
    print("2 - Results of a certain season")
    print("3 - Find the number of victories of a driver")
    print("4 - Know the number of wins of a driver for each year")
    print("5 - See Qualification delta from a round")
    print("6 - Know the number of points finishing of a driver for each year")
    print("leave - If you want to leave")
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
        QualiPlot()
    elif menu == "6" :
        driverId, PiloteProp = FindDriverId()
        print("Work in progress...")
    elif menu == "leave" :
        print("Bye bye !")
    else :
        print("Please choose one of the options below by typing a number between 1 and 6")

Menu()
print("It's alive !")