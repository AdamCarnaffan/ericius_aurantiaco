import React, { Component } from 'react'
import {
  Col, Row, Button,
  Card, CardImg, CardText, CardBody, CardTitle
} from 'reactstrap';
import Truncate from 'react-truncate';
import lerpColour from 'color-interpolate';
import './NewsCard.css';

function Thumbnail(props) {
  if ('image' in props && props.image != null) {
    return (
      <CardImg src={props.image.source} alt={props.image.alt}
        className="card-img-top card-thumbnail" />
    );
  }

  return (null);
}

export default class NewsCard extends Component {
  constructor(props) {
    super(props);
    this.onCardClick = this.onCardClick.bind(this);
  }

  onCardClick() {
    window.open(this.props.url, '_blank');
  }

  render() {
    const statusColour = lerpColour(['#d9534f', '#f0ad4e', '#28a745'])(this.props.honestyMetric / 100);
    return (
        <Card className="news-card shadow border-0">
          <Row>
            <Col md="9" className="order-12">
            <CardBody className="callout" style={{borderLeftColor: statusColour}}>
              <strong className="mb-2 text-secondary">{this.props.source.name}</strong>
              <CardTitle className="news-card-title mb-0 w-100" tag="h3" onClick={this.onCardClick}>
                {this.props.title}
              </CardTitle>
              <CardText tag="p" className="text-secondary mb-auto w-100 mt-3">
                <Truncate lines={3}>
                  {this.props.content}
                </Truncate>
              </CardText>
            </CardBody>
            </Col>
            <Col md="3" className="order-1 order-md-12 card-thumbnail-col">
              <Thumbnail image={this.props.thumbnail} />
              <div className="news-card-score-overlay">
                <Button size="md" style={{background: statusColour, borderColor: statusColour}} 
                  className="m-3 news-card-score-button shadow">
                  <strong>{this.props.honestyMetric}</strong>
                </Button>
              </div>
            </Col>
          </Row>
        </Card>
    )
  }
}
