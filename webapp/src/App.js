import React, { Component } from 'react';
import './App.css';
import { Container } from 'reactstrap';
import NewsCard from './components/NewsCard';
import moment from 'moment';
import articleExtractor from 'unfluff';

class App extends Component {
  constructor(props) {
    super(props);
    this.setState({
      articles: null
    });
  }
  
  componentDidMount() {
    let articles = [];
    fetch('https://honesty-matters-news.appspot.com/pleasegivemedatamylordplease', {method: 'post'})
      .then(response => response.json())
      .then(responseJson => {
        for (let i = 0; i < responseJson.length; ++i) {
          let article = {
            citationScore: responseJson[i]['citation_score'],
            headline: decodeURI(responseJson[i]['headline']).replace(/\\/g, ''),
            mediaScore: responseJson[i]['media_score'],
            opinionScore: responseJson[i]['opinion_score'],
            rating: responseJson[i]['rating'],
            thumbnail: responseJson[i]['thumbnail'],
            timestamp: responseJson[i]['timestamp'],
            url: responseJson[i]['url'],
            authorReliability: responseJson[i]['author_reliability'],
            siteReliability: responseJson[i]['site_reliability']
          };

          let articleContent = '';
          fetch(article.url)
            .then(response => response.text())
            .then(responseText => {
              articleContent = articleExtractor(responseText).text;
            })
            .catch(error => console.error(error));
  
          article['content'] = articleContent;
          articles.push(article);
        }

        articles.sort((a, b) => new Date(b.timestamp) >= new Date(a.timestamp) ? 1 : -1);
        this.setState({
          articles: articles
        });
      })
      .catch(error => {
        console.error(error);
        this.setState({
          articles: null
        });
      });
  }

  render() {
    if (this.state === null) return null;
    const articleCards = this.state.articles.map((article) => {
      const honestyMetric = Math.round((article.rating + article.authorReliability + article.siteReliability) / 3);
      return (
        <Container className="app-container py-3" key={article.url}>
          <NewsCard source={{ name: moment(article.timestamp).format('MMMM Do YYYY, h:mm:ss a') }}
            honestyMetric={honestyMetric} userHonestyMetric={70}
            title={article.headline}
            content={article.content}
            thumbnail={{ source: article.thumbnail, alt: "Thumbnail" }}
            url={article.url}
            breakdownFactors={[
              { name: "Presence of Citations", value: article.citationScore },
              { name: "Objectivity", value: article.opinionScore },
              { name: "Media Score", value: article.mediaScore},
              { name: "Author Reliability", value: article.authorReliability },
              { name: "Site Reliability", value: article.siteReliability },
            ]} />
        </Container>
      );
    });
    return (
      <div className="App">
        {articleCards}
      </div>
    );
  }
}

export default App;