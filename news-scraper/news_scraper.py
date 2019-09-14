from bs4 import BeautifulSoup
import requests

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
    content_url = BeautifulSoup(requests.get(root_url).text, features='html.parser') \
        .find_all('a', { 'class': 'rdp59b' })[0]['href']

    # Resolve the content_url if it is a relative URL
    from urllib.parse import urljoin
    content_url = urljoin(root_url, content_url)
    content = BeautifulSoup(requests.get(content_url).text, features='html.parser')
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

        article_data.append({
            'source': article_source,
            'url': article_url,
            'datetime': article_datetime,
            'thumbnail': article_thumbnail
        })

    return article_data

# example usage 
print(headlines('CA', 10))
