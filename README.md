# NFL Picks

## Context

Each week, oddsmakers will hash out "lines" on football games based on how people are betting on each team. These lines indicate how much one team is favored by over the other. For example, if the Falcons are playing the panthers and the Falcons are favored by a touchdown, the line would be Falcons -7. 7 points will be subtracted from the Falcons' final score and that score will be compared to the Panthers' score to determine which team "won" the line. The goal of the lines is to make it so that "winning" is a 50/50 affair. Obviously, since these lines are set based on how people bet on the games, this does not always occur. Our goal with this little game is to send out "picks" each week to a number of our friends. Each of them will choose 9 games of the 13-14 possible games that week and pick the team they think will win the line for each game. At the end of the year, everybody's ratios are calculated so we can see how well we can beat the line. So far, not well.

## Usage

`python3 NFLpicks.py`

Enter next Sunday's date (this will probably change). A result .csv file will be created in the root directory as a table with rows as each game with the betting lines for each game.

## Code

I whipped up a quick script in python after one of my 2316 classes Sophomore year. The script scrapes ESPN's website as well as an NFL odds website which polls betting line data for NFL games each week. I then combine the two sources and create a formatted CSV file which I then send to my friend to further manually format and send out as an email to all our other friends.

## Upcoming

1. I want to provide some automation. Instead of manually running the script every week, I'd rather have an automated process boot up and send an email to my friend with the updated information at a certain time each week. This will involve some computer-specific code (maybe a cron job), but I will also need to implement the emailing, which shouldn't be too hard using the smtp module.

2. Spin up a little web-client on gh-pages.

  * Don't need to have anything fancy at first, just a simple web-page which displays the data with a button to update (or automatic) and download both as CSV and as HTML table as requested by Alex

  * After we get this working, we can look into providing functionality for the group to log into the website and input their picks directly onto the website. This will require looking into setting up a database to handle storing info per user. game.
