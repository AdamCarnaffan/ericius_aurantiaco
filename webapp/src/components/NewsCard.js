import React, { Component } from 'react';
import {
  Col, Row, Button,
  Card, CardImg, CardText, CardBody, CardTitle
} from 'reactstrap';
import Truncate from 'react-truncate';
import lerpColour from 'color-interpolate';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSmileBeam, faSmile, faMeh, faFrown, faSadCry } from '@fortawesome/free-solid-svg-icons';
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

    this.state = {
      showMetricBreakdown: false
    }

    this.onCardClick = this.onCardClick.bind(this);
    this.onStatusButtonClicked = this.onStatusButtonClicked.bind(this);
  }

  onCardClick() {
    window.open(this.props.url, '_blank');
  }

  onStatusButtonClicked() {
    this.setState({
      showMetricBreakdown: !this.state.showMetricBreakdown
    });
  }

  render() {
    const t = this.props.honestyMetric / 100;
    let statusColour;
    if (this.props.honestyMetric <= 50) {
      statusColour = lerpColour(['#d9534f', '#f0ad4e'])(t * 2);
    }
    else {
      statusColour = lerpColour(['#f0ad4e', '#50a847', '#28a745'])(t / 2);
    }
    
    // Determine the status icon.
    let statusIcon = faSadCry;
    if (this.props.honestyMetric >= 90) {
      // If honesty metric is between 100 and 90, use the faSmileBeam icon.
      statusIcon = faSmileBeam;
    }
    // Use the smile icon in the [70, 90) interval.
    if (this.props.honestyMetric < 90 && this.props.honestyMetric >= 70) {
      statusIcon = faSmile;
    }
    // Use the meh icon in the [40, 70) interval.
    else if (this.props.honestyMetric < 70 && this.props.honestyMetric >= 40) {
      statusIcon = faMeh;
    }
    // Use the frown icon in the [20, 40) interval.
    else if (this.props.honestyMetric < 40 && this.props.honestyMetric >= 20) {
      statusIcon = faFrown;
    }

    const rippleAnimationClass = this.state.showMetricBreakdown ? 'animate-ripple' : '';

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
                  className="m-3 news-card-score-button shadow" onClick={this.onStatusButtonClicked}>
                    <div className="w-100 h-100 align-self-center">
                      <FontAwesomeIcon icon={statusIcon} className="mr-2" />
                      <strong>{this.props.honestyMetric}</strong>
                    </div>
                </Button>
            </div>
          </Col>
        </Row>
        <Row className="ripple-overlay">
          <div className={"ripple " + rippleAnimationClass} style={{background: statusColour}} />
        </Row>
      </Card>
    )
  }
}
