from flask import Flask, request, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from json import loads, dumps

app = Flask(__name__)

class Site_Data:

    def __init__( self, url):
        self.url = url
        self.get_site()

    def process_article(self):
        # Get Schema
        self.schema = loads(self.soup.find('script', text=re.compile('schema.org')).string.split('\\n', 1)[1].rsplit('\\n', 1)[0].strip().replace("\\'", "'"))
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
        if 'video' in self.schema:
            print(self.schema)
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


    def totalWords(self):
        length = 0
        for text in self.getQuotes(False):
            length += len(self.text.split())
        return len

    def totalRating(self, authorScore, siteScore):
        score = 100
        citationScore = -1 * ( 200 / (citations() + 3 ) ) + 100
        opinionScore = ( 75 ) * ( 1.5 ^ ( ( -150 * opinion() ) / totalWords() ) + 25 )
        captionCount = 0
        for image in self.images:
            if image[1] != None:
                captionCount += 1
        captionScore = 1.032 * (-2 ^ ( (-5 * captionCount) / len(self.images) ) + 1 )

        citation = 1
        opinion = 1
        caption = 1
        score = ( citation * citationScore + opinion * opinionScore + caption * captionScore ) / ( citation + opinion + caption )
        
        return score


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
