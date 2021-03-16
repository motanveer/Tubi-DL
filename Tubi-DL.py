import json
import requests
import yaml
from bs4 import BeautifulSoup

# This function will build a list of all the episode IDs:
def extractIDs(seasons):
    episodeIds = []
    for season in seasons:
        title = season['title']
        for episode in season['episodeIds']:
            episodeIds.append(episode)
    return episodeIds


#Pull down Tubi Series webpage
#r = requests.get("https://tubitv.com/series/2067/yu-gi-oh?start=true")

r = requests.get("https://tubitv.com/series/4/transformers-cybertron?start=true")

# Create BS4 Object
soup = BeautifulSoup(r.text, 'html.parser')

# Get all the script tags and put them in a dictonary:
scripts = soup.find_all('script')

# Data Script, this variable holds the data of the script tag that contains the JSON data we need
dataScript = ""

# See if the data we need to parse has been found, and if so assign it to a variable
for script in scripts:
    unicode_string = str(script.string)
    if("window.__data" in unicode_string):
        dataScript = unicode_string;

# Remove the the following substring from the script tag so we can begin the prcoess of parsing the data
dataScript = dataScript.split("window.__data=")


dataScript = dataScript[1]  # Split generates a dictornary, so we need to chose the correct element.
dataScript = dataScript[:-1] # Remove a weird semi colon at the end 

dataScript =  yaml.load(dataScript) # Since this data isn't actually JSON we need to load it as YAML which at least allw us to build a strcutured data type arround it


dataScript = [dataScript['video']['byId']['04']['seasons']] # Drilling down into the element which contains the information about episode IDs
dataScript = dataScript[0];  #This element contains all the seasons of a TV Show


episodeID = extractIDs(dataScript)

for episode in episodeID:
    episode = "https://tubitv.com/tv-shows/" + episode + "\n"
    f = open("episodes.txt", "a")
    f.write(episode)
    f.close()