import urllib.request
import re
import csv
import bs4
import requests


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
    
    r = requests.get('http://www.footballlocks.com/nfl_lines.shtml')


    soup = bs4.BeautifulSoup(r.text, "html.parser")

    lines = []

    for table in soup.find_all('table', cols='5'):
        for tr in table.find_all('tr'):
            line = []
            for td in tr.find_all('td'):
                line.append(td.get_text())

            # need condition to ignore blank styling row
            if '' not in line:
                lines.append(line)    

    homeFirst = []
    teams = [] # list for use in grabbing records
    for date, first, line, last, ou in lines[1:]: # row = [favorite, line, underdog]
        
        if first.startswith('At '): #if favored team is home
            first = first[3:]
        else: #if underdog is home

            # fucking london
            if '(at London)' in last:
                last = last[:last.find('(at London)')]
            else:
                last = last[3:]

            first, last = last, first
            line = str(-float(line)).strip(".0")
        if not line.startswith("-"):
            line = "+" + line
        print(line)
        homeFirst.append([date, first, line, last, ou])
    
    records = {}
    espnUrl = 'http://espn.go.com/nfl/standings'
    espnStr = urllib.request.urlopen(espnUrl).read().decode()

    for row in re.findall(ESPN_REGEX, espnStr):
        stats[convertTeamNameToCity(row[STAT_MAP["TEAM_NAME"]])] = row

    errors = 0

    for i in range(len(homeFirst)): #use homeFirst instead of teams to append the record to homeFirst
        try:
            homeFirst[i][1] = homeFirst[i][1]+' ('+stats[homeFirst[i][1]][3]+'-'+stats[homeFirst[i][1]][4]+'-'+stats[homeFirst[i][1]][5]+')' #first element of each row. 
            homeFirst[i][3] = homeFirst[i][3]+' ('+stats[homeFirst[i][3]][3]+'-'+stats[homeFirst[i][3]][4]+'-'+stats[homeFirst[i][3]][5]+')'
        except:
            errors += 1
            print('Error: {}'.format(homeFirst[i]))

    headers = ['Date', 'Home','Line','Away', 'O/U']

    writeFile([headers] + homeFirst)
    writeFile([headers] + homeFirst, file_type = ".html")

    return errors

date = DATE

errors = pickEm(date)
if errors == 0:
    print("Everything went smoothly. Check NFLpicks.csv file")
else:
    print("There were {} errors in this run. Check print statements".format(errors))





