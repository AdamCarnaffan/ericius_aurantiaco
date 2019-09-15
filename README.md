# HonestyMatters

## Inspiration

Finding reliable and credible news sources has become an increasingly more difficult task to accomplish. Being able to judge whether a news article is honest is often overlooked, especially when the headlines of articles are written less for accuracy, and more to attract clicks. 

## What it does

This web application displays a figure from 0-100 on a red-green sliding scale beside the headline of every news article from a google news search. This is done to give a quantifiable measure of reliability and credibility of news articles, allowing users to compare articles to obtain only the most honest sources of information. Users can also provide their own ratings as feedback for the community based on their perception of an article's reliability.

## How we built it

First, we web-scraped Google News for news articles and processed the information using Google's Cloud's app engine. Each news article found was then scraped and judged for honesty/reliability against the following criteria:

- Presence of citations
- Presence of opinion words such as "I think"
- Referencing of image captions
- Embedded video links if references to videos are present
- Site reliability (taken from average scores of articles from the same news source) 
- Author reliability (taken from average scores from the same author) 
- Image originality (e.g. clipart/stock photos versus authentic photographs)

Each criteria above contributes to a weighted mean and results in an overall honesty rating of the news article. Each rating is saved into Google Firebase, to reduce the amount of times scraping needs to be done for a unique article in the web app.

Additionally, we incorporated a user-honesty score powered by SurveyMonkey to allow users to provide their rating about news articles as feedback for the community.

## Challenges we ran into

- Coming up with multi-variable functions to model the citations, opinion, and image captioning senarios correctly.
- Embedding the SurveyMonkey implementation code on the react platform due to overlays 

## Accomplishments that we're proud of

- The smooth transitions and displays related to the web-app design!
- Successfully aggregating multi-variable functions to come up with an accurate rating system

## What we learned

- There are so many tools available to make the project run smoothly and efficiently, such as Google's Firebase and React. We learned how to add Firebase's features to our web-app to bring our ideas to reality
- How to pay great attention to detail when designing the web-app to ensure that it's user-friendly and aesthetically pleasing

## What's next for HonestyMatters?

- Incorporate the Facebook API to automatically post the top rated HonestNews articles to the HonestNews facebook page, to allow those who follow the page to have a reliable newsource from hourly/daily updates.
- Incorporate the Voiceflow API to ask a Google Home "Tell us the honest news today", to output a filtered list of news articles for the user to choose from
- Using machine learning and sentiment analysis to detect bias in news articles
