import React, { Component } from 'react'
import {
  Col, Row, Button,
  Card, CardImg, CardText, CardBody, CardTitle,
  Popover, PopoverHeader, PopoverBody
} from 'reactstrap';
import Truncate from 'react-truncate';
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
        <Card className="shadow border-0">
          <Row>
            <Col md="9" className="order-12">
            <CardBody>
              <strong className={"mb-2 " + this.props.source.className}>{this.props.source.name}</strong>
              <CardTitle className="mb-0 w-100" tag="h3">
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
            </Col>
          </Row>
          
          {/* <div className="featured-card-thumbnail">
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
          </div> */}
        </Card>
    )
  }
}
