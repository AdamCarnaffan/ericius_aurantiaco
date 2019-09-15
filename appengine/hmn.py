from flask import Flask, request, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager import chrome
from json import loads, dumps
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import time
import re

app = Flask(__name__)

# Background Scheduler
cron = BackgroundScheduler()

class Site_Data:

    def __init__( self, url):
        self.url = url
        self.get_site()

    def process_article(self):
        # Get Schema
        schemaSearch = self.soup.find('script', text=re.compile('schema.org'))
        self.schema = loads(re.sub(r'\\x..', '', schemaSearch.string.split('\\n', 1)[-1].rsplit('\\n', 1)[0].strip().replace("\\'", "'"))) if schemaSearch is not None else None
        # Get title
        self.title = self.soup.title.string
        ttl = self.soup.find("meta", property='og:title')
        self.title = ttl.get('content') if self.title is None and ttl is not None else self.title
        # Fetch all meta data
        pb = self.soup.find("meta", property='article:published_time')
        self.publish = pb.get('content') if pb is not None else None
        # Process author
        self.authors = []
        authorTagline = self.soup.find("meta", property='author')
        authorTagline = authorTagline.get('content') if authorTagline is not None else None
        if authorTagline is not None:
            authorSplit = authorTagline.split(' and ')
            finalAuthorSplit = []
            for line in authorSplit: finalAuthorSplit += line.split(', ')
            for author in finalAuthorSplit:
                self.authors += [author]
        # Get embedded content information
        # Images
        imgs = self.soup.findAll('img')
        if imgs is not None:
            popImages = {'%&%': []}
            for entry in imgs:
                clsses = entry.get('class')
                if clsses is not None:
                    for cl in entry.get('class'):
                        if cl in popImages:
                            popImages[cl] += [entry]
                        else:
                            popImages[cl] = [entry]
                else:
                    popImages['%&%'] += [entry]
            largest = ['', 0]
            for key in popImages:
                if len(popImages[key]) > largest[1]:
                    largest[0] = key
                    largest[1] = len(popImages[key])
            self.images = []
            for img in popImages[largest[0]]:
                self.images += [[img['src'], img.get('alt')]]
        else:
            self.images = []
        # Fetch video info
        if self.schema is not None and 'video' in self.schema:
            self.video = self.schema['video']
        else:
            self.video = None
        # Fetch article main body
        bodies = {'%&%': ''}
        for entry in self.soup.findAll('p') + self.soup.findAll('div'):
            if entry.string is None: continue
            clsses = entry.get('class')
            if clsses is not None:
                for cl in entry.get('class'):
                    if cl in bodies:
                        bodies[cl] += " " + entry.string
                    else:
                        bodies[cl] = entry.string
            else:
                bodies['%&%'] += entry.string
        longest = ['', 0]
        for key in bodies:
            if len(bodies[key]) >= longest[1]:
                longest[0] = key
                longest[1] = len(bodies[key])
        self.body = bodies[longest[0]]
        return self

    def get_site(self):
        self.page = str(urlopen(self.url).read())
        self.soup = BeautifulSoup(self.page, features='html.parser')
        return self

    def dump(self):
        dp = self.__dict__
        del dp['soup']
        return dumps(dp)

    #####################
    # RATINGS FUNCTIONS #
    #####################

    def getQuotes(self, isQuote):
        # count sections of body between quotation marks
        c1 = 0
        quotes = []
        notQuotes = []
        for partition in self.body.rjust(1).split('"'):
            c1 += 1
            if c1 % 2 == 0:
                # confirm quote is longer than 5 words
                if len(partition.split()) > 5:
                    quotes.append(partition)
            else:
                notQuotes.append(partition)

        if (isQuote):
            return quotes
        else:
            return notQuotes
   
    # determine number of citations in page
    def citations(self):
        citations = len(self.getQuotes(True))
        return citations

    # COMBAK: we need to define fluff
    def fluff(self):
        fluff = 0
        return fluff

    def opinion(self):
        # count first person pronouns not in quotes
        text = self.getQuotes(False)
        pronouns = 0
        for words in text:
            pronouns += len(re.findall(r'(\Wi\W|\Wme\W|\Wwe\W|\Wus\W|\Wmyself\W|\Wmy\W|\Wour\W|\Wours\W)', words.lower()))
        return pronouns

###############
# AUTO-PARSER #
###############

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
    chrome_options.add_argument('--log-level=3')

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


def trigger_headline_collect():
    res = headlines('CA')
    print(res)
    return

##########
# ROUTES #
##########

@app.route("/")
def test():
    return render_template('tester.html')

@app.route("/request", methods=['POST'])
def get_page_data(url=None):
    if url is None:
        url = request.form.get('url')
    newdt = Site_Data(url)
    newdt.process_article()
    return newdt.dump()

# Maintenance

# Schedule jobs
cron.add_job(func=trigger_headline_collect, trigger='interval', minutes=2)
cron.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')

