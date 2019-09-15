import React, { Component } from 'react';
import './App.css';
import { Container } from 'reactstrap';
import NewsCard from './components/NewsCard';
import moment from 'moment';

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
          const article = {
            citationScore: responseJson[i]['citation_score'],
            headline: responseJson[i]['headline'],
            mediaScore: responseJson[i]['media_score'],
            opinionScore: responseJson[i]['opinion_score'],
            rating: responseJson[i]['rating'],
            thumbnail: responseJson[i]['thumbnail'],
            timestamp: responseJson[i]['timestamp'],
            url: responseJson[i]['url']
          };
  
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
      return (
        <Container className="app-container py-3">
          <NewsCard source={{ name: moment(article.timestamp).format('MMMM Do YYYY, h:mm:ss a') }}
            honestyMetric={article.rating} userHonestyMetric={70}
            title={article.headline}
            content={"test"}
            thumbnail={{ source: article.thumbnail, alt: "Thumbnail" }}
            url={article.url}
            breakdownFactors={[
              { name: "Presence of Citations", value: article.citationScore },
              { name: "Objectivity", value: article.opinionScore },
              { name: "Media Score", value: article.mediaScore},
              { name: "Author Reliability", value: 86 },
              { name: "Site Reliability", value: 100 },
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