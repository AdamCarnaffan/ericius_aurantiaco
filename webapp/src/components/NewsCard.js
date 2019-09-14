import React, { Component } from 'react'
import {
  Col,
  Card, CardImg, CardText, CardBody,
  Button
} from 'reactstrap';
import Truncate from 'react-truncate';
import './NewsCard.css';

function Thumbnail(props) {
  if ('image' in props && props.image != null) {
    return (
      <CardImg src={props.image.source} alt={props.image.alt}
        className="card-img-right featured-card-thumbnail-image flex-auto d-none d-lg-block" />
    );
  }

  return (null);
}

export default class NewsCard extends Component {
  render() {
    return (
      <Col className="featured-card p-0">
        <Card className="flex-md-row mb-4 shadow h-md-250 border-0">
          <CardBody className="d-flex flex-column align-items-start">
            <strong className={"d-inline-block mb-2 " + this.props.source.className}>{this.props.source.name}</strong>
            <h3 className="d-inline-block mb-0 w-100">
              {this.props.title}
          </h3>
            <CardText tag="p" className="text-secondary mb-auto w-100 mt-3">
              <Truncate lines={3}>
                {this.props.content}
            </Truncate>
            </CardText>
          </CardBody>
          <div className="featured-card-thumbnail">
            <Thumbnail image={this.props.thumbnail} />            
            <div className="news-card-score-overlay">
              <Button size="lg" color="success" className="news-card-score-button m-3 rounded-circle">
                <strong>51</strong>
              </Button>
            </div>
          </div>
        </Card>
      </Col>
    )
  }
}
