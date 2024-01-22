import os
import json
import requests
import yaml
import argparse
from bs4 import BeautifulSoup



parser = argparse.ArgumentParser(description= "Tubi-DL is a wrapper for YouTube that allows you to downloaod all the episodes of a series from Tubi")
parser.add_argument('seriesURL', help="Example URL: https://tubitv.com/series/1098/sabrina-the-animated-series?start=true")
#parser.add_argument('-y', "--youtubedl", help="Enter any standard YouTube-DL arguments")
parser.add_argument('-c', '--concurrent', action="store_true", help="Using this flag will start the downloads of ALL the episodes at the same time") 

args = parser.parse_args()


tubiURL = args.seriesURL
seriesID = "0" + tubiURL.split('/')[4]
print(seriesID)


def extractIDs(seasons):
    episodeIds = []
    for season in seasons:
        for episode in season['episodes']:
            episodeId = episode['id']
            episodeIds.append(episodeId)
    return episodeIds

#=====================================================================================

def build(episodeID):
    os.mkdir(seriesID)
    for i, episode in enumerate(episodeID):
        if args.concurrent:
            separator = "&" if i < len(episodeID) - 1 else ""
        else:
            separator = "&&" if i < len(episodeID) - 1 else ""

        episode_cmd = f"youtube-dl https://tubitv.com/tv-shows/{episode} {separator}\n"

        with open(fileName, "a") as f:
            f.write(episode_cmd)

#=====================================================================================


#Pull down Tubi Series webpage
r = requests.get(tubiURL)


#r = requests.get("https://tubitv.com/series/4/transformers-cybertron?start=true")

# Create BS4 Object
soup = BeautifulSoup(r.text, 'html.parser')

# Get the first word of the title
shortened_title = soup.find('title').text.split()[0].lower()

# Use the shortened title in the file name
fileName = seriesID + "/" + shortened_title + ".sh"

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

dataScript =  yaml.safe_load(dataScript) # Since this data isn't actually JSON we need to load it as YAML which at least allw us to build a strcutured data type arround it


dataScript = [dataScript['video']['byId'][seriesID]['seasons']] # Drilling down into the element which contains the information about episode IDs
dataScript = dataScript[0];  #This element contains all the seasons of a TV Show


build(episodeID = extractIDs(dataScript))