import requests #make sure your python env has requests installed
import json 
from bs4 import BeautifulSoup #make sure your python env has BeautifulSoup installed

# Headers for website requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Slack webhook URL
slack_webhook_url = "" #add your slack webhook url here


# list of websites to monitor. This is a list variable that contains a set a dictionary key:value pair for each website to check
# the url key is for the individual website and the search_text value is the piece of text we are searching for on that webpage
websites = [
    {"url": "https://example.com", "search_text": "enter your search text here..."},
    {"url": "https://example.com", "search_text": "Copyright © 2025"} # a good example of a solid search text...this should be in the footer
    {"url": "https://example.com", "search_text": ".css-selector"} # if you have a css selector that you want to search for, that works too!
    # Add more websites as neededs
]

# Using session for persistent connection
session = requests.Session()
session.headers.update(headers)


# Function to send a message to Slack
def send_to_slack(message):
    data = {'text': message}
    response = requests.post(slack_webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        print(f"Failed to send notification to Slack: {response.status_code}, {response.text}")
#check dem websites
def check_website(websites):
    try:
        # Fetch the response code from the website 
        response = session.get(websites["url"], verify=True,timeout=(15, 30))

        # If response code is 200, then proceed to chceck if the search string is found in the page. 
        # If the search string is found, then the function will exit and move on to the next website in the list of websites
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            status_message = f"Website {websites['url']} is up (Status Code: 200)"

            if websites["search_text"] in text:
                return
            else:
                status_message += f" but text something is WRONG...'{websites['search_text']}' was NOT found."
        else:
            status_message = f"Website Down!! {websites['url']} returned a Status Code of: {response.status_code})"
        
        print(status_message)
        send_to_slack(status_message)

    except requests.RequestException as e:
        error_message = f"Error pinging website {websites['url']}: {e}"
        print(error_message)
        send_to_slack(error_message)

# Check each website in the list
for site in websites:
    check_website(site)

#game blouses..
