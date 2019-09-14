import React from 'react';
import './App.css';
import { Container } from 'reactstrap';
import NewsCard from './components/NewsCard';

function App() {
  return (
    <div className="App">
      <Container className="app-container py-3">
        <NewsCard source={{ name: "CNN", className: "text-danger" }} honestyMetric={100}
          title="New York AG exposes $1 billion in wire transfers by Sackler family"
          content="The state attorney general's office is trying to find how much money the owners of pharmaceutical giant Purdue Pharma amassed and where it is."
          thumbnail={{ source: "https://cdn.cnn.com/cnnnext/dam/assets/190312114823-20190312-opioid-v10-large-tease.jpg", alt: "Thumbnail" }}
          url="https://www.cnn.com/2019/09/13/us/sackler-family-purdue-pharma-case/index.html" />
      </Container>
    </div>
  );
}

export default App;
