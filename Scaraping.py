
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO  # <--- import this

#URL for the premier league table
standing_pl = "https://fbref.com/en/comps/9/Premier-League-Stats"

#request the pl page raw html
data = requests.get(standing_pl)
soup = BeautifulSoup(data.text, features="lxml")

#find the table with the class stats_table
standings_table = soup.select('table.stats_table')[0]
#Finds all the a-tags in the table
links = standings_table.find_all('a')

links = [l.get("href") for l in links]
#filters to only get the sqeuad links
links = [l for l in links if '/squads/' in l]

team_url = [f"https://fbref.com{l}" for l in links]

data = requests.get(team_url[0])
soup = BeautifulSoup(data.text, features="lxml")

matches = pd.read_html(StringIO(data.text), match="Scores & Fixtures")[0]  # <--- updated this line
print(matches.head())

links = soup.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if l and "all_comps/shooting/" in l]

data = requests.get(f"https://fbref.com{links[0]}")

shooting = pd.read_html(StringIO(data.text), match="Shooting")[0]  # <--- updated this line

#add more data than shooting and matches 

print(shooting.head())
shooting.columns = shooting.columns.droplevel()

team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
team_data.head()
print(team_data.head())
