# README

This script uses Selenium to automate image scraping in the Chrome browser.

**REQUIREMENTS:**
Selenium: pip3 install selenium
Chromedriver: https://chromedriver.chromium.org/

_You will need to set the 'PATH' variable to the path of the Chromedriver executable after downloading it_

When run, the user will be prompted to enter a search term, the script will perform a Google image search with the specified term.
The user will also be prompted to enter the number of images they want to download.

When the two entries are made, the image URL's will be retreived from the image search then all downloaded in sequence to a directory in the same location as the script.
