import urllib.request
import re
import csv

# (favorite, line, underdog)
 



def pickEm(date): # date = str(MM/DD)

    month = int(date[:2])
    day = int(date[3:])
    if (month%2!=0 and day==30) or (month%2==0 and day==31):
        monDate = str(month+1)+'/1'
    else:
        monDate = str(month) + '/' + str(day+1)
    htmlStr = str(urllib.request.urlopen('http://www.footballlocks.com/nfl_lines.shtml').read())# get page, and convert html to string
    rows = re.findall('<TD>(?:{0}|{1}).*?</TD>.*?<TD>(.*?)</TD>.*?<TD>(.*?)</TD>.*?<TD>(.*?)</TD>'.format(date,monDate),htmlStr) #gets only sundays... for now

    #self.date.delete(0,END)
    #var = IntVar()
    
    
    lists = []
    for tup in rows:
        lists.append(list(tup))
    #print(lists)
    

    homeFirst = []
    teams = [] # list for use in grabbing records
    for row in lists: # row = [favorite, line, underdog]
        if row[0][:3] == 'At ': #if favored team is home
            homeFirst.append([row[0][3:],row[1],row[2]])
            teams.append(row[0][3:])
            teams.append(row[2])
        else: #if underdog is home
            homeFirst.append([row[2][3:],row[1].lstrip('-'),row[0]]) #make underdog first; flip line
            teams.append(row[2][3:])
            teams.append(row[0])
    #print(teams)     
    #print(homeFirst)

    records = {}
    espnUrl = 'http://espn.go.com/nfl/standings'
    espnStr = str(urllib.request.urlopen(espnUrl).read())

    for team in teams: 
        records[team] = re.findall('>{0}</a>.*?<td>(\d+)</td><td>(\d+)</td><td>(\d+)'.format(team),espnStr)[0] #tuple: (win,loss)
    #print(records)

    for i in range(len(homeFirst)): #use homeFirst instead of teams to append the record to homeFirst
        homeFirst[i][0] = homeFirst[i][0]+' ('+records[homeFirst[i][0]][0]+'-'+records[homeFirst[i][0]][1]+'-'+records[homeFirst[i][0]][2]+')' #first element of each row. 
        homeFirst[i][2] = homeFirst[i][2]+' ('+records[homeFirst[i][2]][0]+'-'+records[homeFirst[i][2]][1]+'-'+records[homeFirst[i][2]][2]+')'
    #print(homeFirst)

    espnUrl = 'http://espn.go.com/nfl/standings'
    out = open('NFLpicks.csv','w')
    writer=csv.writer(out)
    writer.writerow(['Home','Line','Away'])
    writer.writerows(homeFirst)

    out.close()

    return len(lists)

date = input("Enter NFL Sunday's date: ")
if pickEm(date) > 2:
    print("Everything went smoothly. Check NFLpicks.csv file")
else:
    print("Something went wrong. Uncomment print statements")

    






