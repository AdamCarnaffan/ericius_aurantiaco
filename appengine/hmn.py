# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, send_from_directory
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager import chrome
from json import loads, dumps
from apscheduler.schedulers.background import BackgroundScheduler
from firebase_admin import credentials, firestore, datetime
import firebase_admin
import requests
import time
import re
import os
import math
import decimal
from datetime import timedelta, date, datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Background Scheduler
cron = BackgroundScheduler()

# Database
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)


class Site_Data:

    def __init__( self, url):
        self.url = url
        self.get_site()

    def process_article(self):
        # Get Schema
        try:
            schemaSearch = self.soup.find('script', text=re.compile('schema.org'))
            # print(re.sub(r'\\x..', '', re.sub('^[^{]*', '', re.sub('[^}]*$', '', schemaSearch.string)).replace("\\'", "'")))
            self.schema = loads(re.sub(r'\\x..', '', re.sub('^[^{]*', '', re.sub('[^}]*$', '', schemaSearch.string)).replace("\\'", "'").replace('\\n', '').replace('\\\\"', ''))) if schemaSearch is not None else None
        except:
            self.schema = None
        # Get Site
        self.site = self.url.split('/')[2]
        # Get title
        title = self.soup.title
        self.title = title.string if title is not None else None
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
            if len(popImages) == 1 and len(popImages['%&%']) < 1:
                self.images = []
            else:
                for key in popImages:
                    if len(popImages[key]) > largest[1]:
                        largest[0] = key
                        largest[1] = len(popImages[key])
                self.images = []
                for img in popImages[largest[0]]:
                    try:
                        self.images += [[img['src'], img.get('alt')]]
                    except:
                        pass
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
                bodies['%&%'] += " " + entry.string
        longest = ['', 0]
        for key in bodies:
            if len(bodies[key]) >= longest[1]:
                longest[0] = key
                longest[1] = len(bodies[key])
        self.body = bodies[longest[0]]
        return self

    def get_site(self):

        request_headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "http://thewebsite.com",
            "Connection": "keep-alive" 
        }
        req = Request(self.url, headers=request_headers)
        self.page = str(urlopen(req).read())
        self.soup = BeautifulSoup(self.page, features='html.parser')
        return self

    def dump(self):
        dp = self.__dict__
        del dp['soup']
        return dumps(dp)

    def export(self):
        data = {}
        data['citation_score'] = self.citationScore
        data['headline'] = self.title
        data['media_score'] = self.mediaScore
        data['opinion_score'] = self.opinionScore
        data['rating'] = self.rating
        data['thumbnail'] = self.images[0][0] if len(self.images) > 0 else None
        data['timestamp'] = self.publish
        data['url'] = self.url
        data['authors'] = self.authors
        data['site'] = self.site
        data['timestamp'] = datetime.now()
        return data

    def insert(self):
        dt = self.export()
        cl = firestore.client().collection('articles')
        dup = False
        for row in cl.where('title', '==', self.title).stream():
            dup = True
        if not dup:
            firestore.client().collection('articles').add(dt)
        return self

    #####################
    # RATINGS FUNCTIONS #
    #####################

    def getQuotes(self, isQuote):
        # count sections of body between quotation marks
        c1 = 0
        quotes = []
        notQuotes = []
        # print(self.body)
        for partition in re.split('["“”]', self.body.rjust(1).replace('\\xe2\\x80\\x9c', '“').replace('\\xe2\\x80\\x9d', '”')):
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
   
    def total_words(self):
        length = 0
        for text in self.getQuotes(False):
            length += len(text.split())
        return length

    # determine number of citations in page
    def citations(self):
        citationScore = len(self.getQuotes(True))
        return citationScore

    # COMBAK: we need to define fluff
    #def fluff(self):
    #    fluffScore = 0
    #    return fluffScore

    def opinion(self):
        # count first person pronouns not in quotes
        text = self.getQuotes(False)
        pronouns = 0
        for words in text:
            pronouns += len(re.findall(r'(\Wi\W|\Wme\W|\Wwe\W|\Wus\W|\Wmyself\W|\Wmy\W|\Wour\W|\Wours\W)', words.lower()))
        opinionScore = pronouns
        return opinionScore

    def video_ref(self):
        textRef = 0
        videoRef = 100
        for text in self.getQuotes(False):
            textRef += len(re.findall(r'((\Wvideo\W)(?!game)|\Wfilm\W|\Wclip\W|\Wmedia\W)', text.lower()))
        if textRef > 2 and self.video is None:
            videoRef = 0
        return videoRef

    def total_rating(self, authorScore=None, siteScore=None):
        score = 100
        if self.total_words() < 1: 
            citationScore = 0
            opinionScore = 0
        else:
            citationScore = 25 * math.exp( -( ( self.citations() / ( self.total_words() / 150 ) ) - 1.3 ) ** 10 ) + 25 * math.exp( -( ( self.citations() / ( self.total_words() / 150 ) ) - 1.3 ) ** 4 ) + 50 * math.exp( -( ( self.citations() / ( self.total_words() / 13.5 ) ) - 1.005 ) ** 1000 )
            opinionScore = ( 75 ) * ( 1.5 ** ( ( -150 * self.opinion() ) / self.total_words() )) + 25
        captionCount = 0
        for image in self.images:
            if image[1] != None:
                captionCount += 1
        if len(self.images) < 1:
            captionScore = 100
        else:
            captionScore = (1.032 * (-2 ** ( (-5 * captionCount) / len(self.images) ) + 1 )) * 100
        videoScore = self.video_ref()

        citation = 1
        opinion = 1.5
        caption = 0.6
        video = 0.2
        # print(self.video)
        score = ( citation * citationScore + opinion * opinionScore + caption * captionScore + video * videoScore ) / ( citation + opinion + caption + video)
        
        self.citationScore = citationScore
        self.opinionScore = opinionScore
        self.mediaScore = (caption * captionScore + video * videoScore) / (caption + video)
        self.rating = score

        return self


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
    for site in res:
        news = Site_Data(res['url'])
        news.process_article()
        news.total_rating()
        news.insert()
    return

def json_serial(obj):
   """JSON serializer for non JSON serializable objects"""

   if isinstance(obj, (datetime, date)):
      return obj.isoformat()
   elif isinstance(obj, (timedelta)):
      return ':'.join(str(obj).split(':')[:2])
   elif isinstance(obj, (decimal.Decimal)):
      return float(obj)
   elif type(obj) == 'DatetimeWithNanoseconds':
      return int(obj)
   raise TypeError ("Type {} is not serializable".format(type(obj)))

##########
# ROUTES #
##########

@app.route("/", defaults={'path': ''})
@app.route('/<path:path>')
def react_app(path):
    if path != "" and os.path.exists(app.static_folder + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route("/submit")
def test():
    return render_template("tester.html")

@app.route("/request", methods=['POST'])
def get_page_data(url=None):
    if url is None:
        url = request.form.get('url')
        if url is None: return "An error occured loading the URL"
    newdt = Site_Data(url)
    newdt.process_article()
    newdt.total_rating()
    newdt.insert()
    return str(newdt.rating) + " - O {}, M {}, C {}".format(newdt.opinionScore, newdt.mediaScore, newdt.citationScore)

@app.route("/pleasegivemedatamylordplease", methods=['POST'])
def give_data_to_react():
    dt = []
    cl = firestore.client().collection('articles')
    for row in cl.order_by('timestamp').limit(100).stream():
        rowDict = row.to_dict()
        # Get author bias
        authScore = 0
        count = 0
        for auth in cl.order_by('timestamp').limit(20).where('authors', '==', rowDict['authors']).stream():
            count = count + 1
            authScore += auth.to_dict()['rating']
        finalAuth = authScore / count
        # Get site bias
        siteScore = 0
        count = 0
        for st in cl.order_by('timestamp').limit(20).where('site', '==', rowDict['site']).stream():
            count = count + 1
            siteScore += st.to_dict()['rating']
        finalSite = siteScore / count
        dt += [{'authors': rowDict['authors'], 'citation_score': rowDict['citation_score'], 'headline': rowDict['headline'], 
                'media_score': rowDict['media_score'], 'opinion_score': rowDict['opinion_score'], 'rating': rowDict['rating'],
                'site': rowDict['site'], 'thumbnail': rowDict['thumbnail'], 'timestamp': rowDict['timestamp'],
                'url': rowDict['url'], 'author_reliability': finalAuth, 'site_reliability': finalSite}]
    return dumps(dt, default=json_serial)

# Maintenance

# Schedule jobs
cron.add_job(func=trigger_headline_collect, trigger='interval', minutes=10)
cron.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')

