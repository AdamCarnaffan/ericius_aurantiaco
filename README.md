# HonestNews

## Inspiration

Finding reliable and credible news sources has become an increasingly more difficult task to accomplish. Being able to judge whether a news article is honest is often overlooked, especially when the headlines of articles are written less for accuracy, and more to attract clicks. 

## What it is 

This web application and chrome extension displays a figure from 0-100 on a sliding colour scale of red to green, along with a sad-meh-happy emoji beside the headline of every news article from a google search.

## Goal

To give a quantifiable measure of reliability and honesty, allowing users to compare articles to obtain only the most reliable, credible, and honest sources of information. 

## How it works
First, we web-scraped Google News for news articles and processed the information using Google's Cloud's app engine. Each news article found was then scraped and judged for honesty/reliability against the following criteria:

- Presence of citations
- Presence of "opinion" words such as "I think"
- Referencing of image captions
- Embedded video links if references to videos are present
- Site reliability (taken from average scores of articles from the same news source) 
- Author reliability (taken from average scores from the same author) 
- Image originality (e.g. clipart/stock photos versus authentic photographs)

Each criteria above contributes to a weighted mean and results in an overall honesty rating of the news article. Each rating is saved into Google Firebase, to reduce the amount of times scraping needs to be done for a unique article in the web app.

Additionally, we incorporated a user-honesty score powered by SurveyMonkey to allow users to provide their feedback for the community.

## Challenges we ran into


## Accomplishments that we're proud of


## What we learned


## What's next for HonestNews?

- Incorporate the Facebook API to automatically post the top rated HonestNews articles to the HonestNews facebook page, to allow those who follow the page to have a reliable newsource from hourly/daily updates.

- Incorporate the Voiceflow API to ask a Google Home "Tell us the honest news today", to output a filtered list of news articles for the user to choose from.

- Using machine learning and sentiment analysis to detect bias in news articles.
