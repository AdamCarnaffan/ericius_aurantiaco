import React from 'react';
import './App.css';
import {
  Container,
  Col,
  Card, CardImg, CardText, CardBody
} from 'reactstrap';
import Truncate from 'react-truncate';

function Thumbnail (props) {
  if ('image' in props && props.image != null) {
      return (
          <CardImg src={props.image.source} alt={props.image.alt} 
              className="card-img-right featured-card-thumbnail flex-auto d-none d-lg-block" />
      );
  }

  return (null);
}

function App() {
  return (
    <div className="App">
      <Container className="app-container py-3">
        <Col className="featured-card">
          <Card className="flex-md-row mb-4 shadow h-md-250 border-0">
            <CardBody className="d-flex flex-column align-items-start">
              <strong className="d-inline-block mb-2 text-danger">CNN</strong>
              <h3 className="d-inline-block mb-0 w-100">
                  New York AG exposes $1 billion in wire transfers by Sackler family
              </h3>
              <CardText tag="p" className="text-secondary mb-auto w-100 mt-3">
                <Truncate lines={3}>
                  The state attorney general's office is trying to find how much money the owners of pharmaceutical 
                  giant Purdue Pharma amassed and where it is.
                </Truncate>
              </CardText>
            </CardBody>
            <Thumbnail image={{
              source: "https://cdn.cnn.com/cnnnext/dam/assets/190312114823-20190312-opioid-v10-large-tease.jpg",
              alt: "Thumbnail"
            }} />
          </Card>
        </Col>
      </Container>
    </div>
  );
}

export default App;
