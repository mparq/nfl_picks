import urllib.request
import re
import csv

DATE = "09/13"

NUM_STATS = 12

ESPN_REGEX = 'href="([^"]+)"><span><span class="team-names">(.*?)</span><abbr .*?>(.*?)</abbr></span></a></td>' + '<td .*?>(.*?)</td>' * NUM_STATS + '</tr>'

# Fragile
STAT_LISTING = [
    "ESPN_LINK",
    "TEAM_NAME",
    "TEAM_NAME_ABBR",
    "W",
    "L",
    "T",
    "PCT",
    "HOME",
    "ROAD",
    "DIV",
    "CONF",
    "PF",
    "PA",
    "DIFF",
    "STRK"
]

STAT_MAP = {stat: i for i, stat in enumerate(STAT_LISTING)}

FLOCKS_REGEX = '<TR>[^<]*<TD>(.*?)</TD>[^<]*<TD>(.*?)</TD>[^<]*<TD>(.*?)</TD>[^<]*<TD>(.*?)</TD>[^<]*<TD>(.*?)</TD>'

OUT_DIR = "generated-data"

def convertTeamNameToCity(name):
    if name.startswith("New York"):
        return "NY" + name[8:]
    print(name)
    city = name.split()
    city = city[:len(city)-1]
    return " ".join(city)

def writeFile(rows, file_name="NFLpicks", file_type=".csv"):
    out = open(OUT_DIR + "/" + file_name + file_type, 'w')
    headers = rows[0]
    del rows[0]

    if file_type == ".csv":
        writer = csv.writer(out)
        writer.writerow(headers)
        writer.writerows(rows)

    elif file_type == ".html":
        out.write("<table>")
        out.write("<tr>")
        for column in headers:
            out.write("<th>{}</th>".format(column))
        out.write("</tr>")
        for row in rows:
            out.write("<tr>")
            for column in row:
                out.write("<td>{}</td>".format(column))
            out.write("</tr>")
        out.write("</table>")

    out.close()

def pickEm(date): # date = str(MM/DD)

    stats = {}

    month = int(date[:2])
    day = int(date[3:])
    if (month%2!=0 and day==30) or (month%2==0 and day==31):
        monDate = str(month+1)+'/01'
    else:
        monDate = str(month) + '/' + str(day+1)
    htmlStr = str(urllib.request.urlopen('http://www.footballlocks.com/nfl_lines.shtml').read())
    rows = re.findall(FLOCKS_REGEX, htmlStr) 

    #print(rows)
    #self.date.delete(0,END)
    #var = IntVar()
    
    
    lists = []
    for tup in rows:
        lists.append(list(tup))
    #print(lists)
    

    homeFirst = []
    teams = [] # list for use in grabbing records
    for date, first, line, last, ou in lists: # row = [favorite, line, underdog]
        
        if first.startswith('At'): #if favored team is home
            first = first[3:]
        else: #if underdog is home
            last = last[3:]
            first, last = last, first
        
        homeFirst.append([date, first, line, last, ou])
    
    #print(homeFirst)

    records = {}
    espnUrl = 'http://espn.go.com/nfl/standings'
    espnStr = urllib.request.urlopen(espnUrl).read().decode()

    for row in re.findall(ESPN_REGEX, espnStr):
        stats[convertTeamNameToCity(row[STAT_MAP["TEAM_NAME"]])] = row
    #print(records)

    print(homeFirst)
    print(sorted(stats.keys()))

    for i in range(len(homeFirst)): #use homeFirst instead of teams to append the record to homeFirst
        homeFirst[i][1] = homeFirst[i][1]+' ('+stats[homeFirst[i][1]][3]+'-'+stats[homeFirst[i][1]][4]+'-'+stats[homeFirst[i][1]][5]+')' #first element of each row. 
        homeFirst[i][3] = homeFirst[i][3]+' ('+stats[homeFirst[i][3]][3]+'-'+stats[homeFirst[i][3]][4]+'-'+stats[homeFirst[i][3]][5]+')'
    #print(homeFirst)

    headers = ['Date', 'Home','Line','Away', 'O/U']

    writeFile([headers] + homeFirst)
    writeFile([headers] + homeFirst, file_type = ".html")

    return len(lists)

date = DATE
if pickEm(date) > 2:
    print("Everything went smoothly. Check NFLpicks.csv file")
else:
    print("Something went wrong. Uncomment print statements")

    






