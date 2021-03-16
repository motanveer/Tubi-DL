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


# This function will build a list of all the episode IDs:
def extractIDs(seasons):
    episodeIds = []
    for season in seasons:
        title = season['title']
        for episode in season['episodeIds']:
            episodeIds.append(episode)
    return episodeIds


tubiURL = args.seriesURL
seriesID = "0" + tubiURL.split('/')[4]
print(seriesID)


#=====================================================================================

def build(episodeID):
    os.mkdir(seriesID);
    for episode in episodeID:
        if(args.concurrent):
            episode = "youtube-dl " +  " https://tubitv.com/tv-shows/" + episode + " &" "\n"
        else:
            episode = "youtube-dl " +  " https://tubitv.com/tv-shows/" + episode + " &&" "\n"
        
        f = open(fileName, "a")
        f.write(episode)
        f.close()

#=====================================================================================


#Pull down Tubi Series webpage
r = requests.get(tubiURL)


#r = requests.get("https://tubitv.com/series/4/transformers-cybertron?start=true")

# Create BS4 Object
soup = BeautifulSoup(r.text, 'html.parser')

fileName = seriesID+"/"+ soup.find('title').text + ".sh"

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


dataScript = [dataScript['video']['byId'][seriesID]['seasons']] # Drilling down into the element which contains the information about episode IDs
dataScript = dataScript[0];  #This element contains all the seasons of a TV Show


build(episodeID = extractIDs(dataScript))