# HonestyMatters

## TRY IT OUT

http://honesty-matters-news.appspot.com/

## Inspiration

Finding reliable and credible news sources has become an increasingly more difficult task to accomplish. Being able to judge whether a news article is honest is often overlooked, especially when the headlines of articles are written less for accuracy, and more to attract clicks.

## What it does

This web application displays a figure from 0-100 on a red-green sliding scale beside the headline of every news article from a google news search. This is done to give a quantifiable measure of reliability and credibility of news articles, allowing users to compare articles to obtain only the most honest sources of information. Users can also provide their own ratings as feedback for the community based on their perception of an article's reliability.

## How we built it

First, we web-scraped Google News for news articles and processed the information using Google's Cloud's app engine. Each news article found was then scraped and judged for honesty/reliability against the following criteria:

- Presence of quotations
- Presence of opinionated terms such as "I think"
- Referencing of image captions
- Embedded video links if references to videos are present
- Site reliability (taken from average scores of articles from the same news source)
- Author reliability (taken from average scores from the same author)

Each criteria above contributes to a weighted mean and results in an overall honesty rating of the news article. Each rating is saved into Google Firebase, to reduce the amount of times scraping needs to be done for a unique article in the web app.

## Challenges we ran into

- Coming up with multi-variable functions to model the citations, opinion, and image captioning scenarios correctly
- Spending large amounts of time gathering training data for Google Cloud's AutoML Natural Language UI, to make the model as accurate as possible

## Accomplishments that we're proud of

- The smooth transitions and displays related to the web-app design!
- Successfully aggregating multi-variable functions to come up with an accurate rating system
- Being able to detect with an especially high success rate of opinionated articles

## What we learned

- There are so many tools available to make the project run smoothly and efficiently, such as Google's Firebase and React. We learned how to add Firebase's features to our web-app to bring our ideas to reality!
- How to pay great attention to detail when designing the web-app to ensure that it's user-friendly and aesthetically pleasing

## What's next for HonestyMatters?

- Incorporate a user-honesty score powered by SurveyMonkey to allow users to provide their own rating about news articles as feedback for the community
- Incorporate the Facebook API to automatically post the top rated HonestNews articles to the HonestNews facebook page, to allow those who follow the page to have a reliable newsource from hourly/daily updates.
- Incorporate the Voiceflow API to ask a Google Home "Tell us the honest news today", to output a filtered list of news articles for the user to choose from
- Additionally, we used machine learning and sentiment analysis to detect bias in news articles. Specifically, we used Google Cloud's AutoML Natural Language UI to create machine learning models to classify news articles according to political leaning and bias. Training data included taking the headings of articles, and scanning the body text to train and test our model.
