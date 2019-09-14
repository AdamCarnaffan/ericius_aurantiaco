from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager import chrome

import time
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) ' + \
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def scroll_browser(browser):
    return browser.execute_script('window.scrollTo(0, document.body.scrollHeight);var page_length=' + \
        'document.body.scrollHeight;return page_length;')

def headlines(country_code, max=100):
    """
    Gets the top news headlines from Google News in the country
    with the specified ``country_code``.

    :param country_code:
        The ISO ALPHA-2 country code.
    :param max:
        The number of news headlines to extract.
    """

    # Technically, we should resolve the language code from the country code;
    # however, this is a prototype (and we aren't using anything but English)...
    language_code = 'en'
    root_url = 'https://news.google.com/?hl={0}-{1}&gl={1}&ceid={1}:{0}'.format(language_code, country_code)
    
    # Find the "more headline" link...
    content_url = BeautifulSoup(requests.get(root_url, headers=HEADERS).text, features='html.parser') \
        .find_all('a', { 'class': 'rdp59b' })[0]['href']

    # Resolve the content_url if it is a relative URL
    from urllib.parse import urljoin
    content_url = urljoin(root_url, content_url)

    # Use selenium to scroll down to the bottom of the page
    chrome_options = Options()  
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent={}'.format(HEADERS['User-Agent']))
    
    browser = webdriver.Chrome(chrome.ChromeDriverManager().install(), options=chrome_options)
    browser.get(content_url)
    page_length = scroll_browser(browser)
    while True:
        previous_length = page_length
        # Wait a few seconds for the data to load...
        time.sleep(3)
        page_length = scroll_browser(browser)

        # If there has been no change in the page length,
        # we have finished scrolling...therefore, we're done!
        if previous_length == page_length:
            break

    # Parse the articles
    content = BeautifulSoup(browser.page_source, features='html.parser')
    articles = content.find_all('div', { 'class': 'xrnccd F6Welf R7GTQ keNKEd j7vNaf' }, limit=max)

    article_data = []
    for article in articles:
        # Check if article is from a valid source (i.e. is it a video?)
        # Look for YouTube video icon beside article source text with classes that hides
        # the icon. If no such element is found, that means the YouTube icon is visible.
        article_subtitle = article.find('div', { 'class': 'SVJrMe' })
        if len(article_subtitle.find_all('span', { 'class': 'DPvwYc N3ElHc gQtGhf eLNT1d uQIVzc' })) == 0:
            continue
        
        article_source = article_subtitle.find('a', { 'class': 'wEwyrc AVN2gc uQIVzc Sksgp' }).text
        article_url = requests.head(urljoin(root_url, article.find('a')['href']), allow_redirects=True).url
        article_datetime = article_subtitle.find('time', { 'class': 'WW6dff uQIVzc Sksgp' })['datetime']
        article_thumbnail = article.find('img', { 'class': 'tvs3Id QwxBBf' }, recursive=True)['src']
        article_headline = article.find('h3', { 'class': 'ipQwMb ekueJc RD0gLb' }).find('a', { 'class': 'DY5T1d' }).text

        article_data.append({
            'source': article_source,
            'url': article_url,
            'datetime': article_datetime,
            'thumbnail': article_thumbnail,
            'headline': article_headline
        })

    return article_data

# example usage 
print(headlines('CA', 10))
