import requests
from bs4 import BeautifulSoup
import json
import time
from prettytable import PrettyTable

def scrape_wikipedia_article(url, visited, link_count):
    if url in visited:
        print(f"\033[93mAlready visited: {url}\033[0m")
        return link_count
    print(f"\033[92mVisiting: {url}\033[0m")
    visited.add(url)

    start_time = time.time()
    response = requests.get(url)
    response_time = time.time() - start_time
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title of the page
    title = soup.find('h1').text
    print(f"Title: {title} (Response Code: {response.status_code}, Time: {response_time:.2f}s)")

    # Find all links to other Wikipedia articles
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/wiki/') and ':' not in href:
            links.append(f"https://en.wikipedia.org{href}")

    print(f"Found {len(links)} new links on {title}")

    # Store the data
    data[title] = links
    link_count += len(links)

    # Save to JSON file every 1000 links
    if link_count >= 1000:
        with open('wikipedia_links.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"\033[94mSaved data to wikipedia_links.json after {link_count} links\033[0m")
        link_count = 0

    # Display links in a table
    table = PrettyTable(['Link'])
    for link in links:
        table.add_row([link])
    print(table)

    # Recursively scrape linked articles
    for link in links:
        link_count = scrape_wikipedia_article(link, visited, link_count)
    
    return link_count

# Initialize
start_url = "https://en.wikipedia.org/wiki/Wikipedia"
visited = set()
data = {}
link_count = 0

print("Starting scraping...")
# Start scraping
link_count = scrape_wikipedia_article(start_url, visited, link_count)

# Final save to JSON file
with open('wikipedia_links.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Scraping completed. Data saved to wikipedia_links.json.")