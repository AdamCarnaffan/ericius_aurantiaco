import React, { Component } from 'react'
import {
  Col,
  Card, CardImg, CardText, CardBody
} from 'reactstrap';
import Truncate from 'react-truncate';
import './NewsCard.css';

function Thumbnail(props) {
  if ('image' in props && props.image != null) {
    return (
      <CardImg src={props.image.source} alt={props.image.alt}
        className="card-img-right featured-card-thumbnail flex-auto d-none d-lg-block" />
    );
  }

  return (null);
}

export default class NewsCard extends Component {
  render() {
    return (
      <Col className="featured-card">
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
          <Thumbnail image={this.props.thumbnail} />
        </Card>
      </Col>
    )
  }
}
