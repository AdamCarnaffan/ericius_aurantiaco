import React, { Component } from 'react'
import {
  Col, Button,
  Card, CardImg, CardText, CardBody,
  Popover, PopoverHeader, PopoverBody
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
  constructor(props) {
    super(props);

    this.toggleScorePopover = this.toggleScorePopover.bind(this);
    this.state = {
      scorePopoverOpen: false
    };
  }

  toggleScorePopover() {
    this.setState({
      scorePopoverOpen: !this.state.scorePopoverOpen
    });
  }  

  render() {
    return (
      <Col className="featured-card p-0">
        <Card className="d-flex flex-md-row shadow border-0">
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
              <Button size="lg" color="success" id="scoreButton"
                className="news-card-score-button m-3 rounded-circle">
                <strong>51</strong>
              </Button>
              <Popover placement="left" isOpen={this.state.scorePopoverOpen} 
                target="scoreButton" toggle={this.toggleScorePopover} trigger="focus">
                <PopoverHeader>Score Breakdown</PopoverHeader>
                <PopoverBody>
                  <ul className="pl-3">
                    <li>Citations</li>
                    <li>Relevancy</li>
                    <li>Lack of Author</li>
                  </ul>
                </PopoverBody>
              </Popover>
            </div>
          </div>
        </Card>
      </Col>
    )
  }
}
