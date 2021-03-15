import requests
from bs4 import BeautifulSoup

#Pull down Tubi Series webpage
r = requests.get("https://tubitv.com/series/2067/yu-gi-oh?start=true")

# Create BS4 Object
soup = BeautifulSoup(r.text, 'html.parser')

# Get all the script tags and put them in a dictonary:
scripts = soup.find_all('script')

# See if the data we need to parse has been found
for script in scripts:
    unicode_string = str(script.string)
    if("window.__data" in unicode_string):
        print("Found")


