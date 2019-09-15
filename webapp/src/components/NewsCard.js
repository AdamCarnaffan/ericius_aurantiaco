import React, { Component } from 'react';
import {
  Col, Row, Button,
  Card, CardImg, CardText, CardBody, CardTitle,
  UncontrolledTooltip
} from 'reactstrap';
import Truncate from 'react-truncate';
import lerpColour from 'color-interpolate';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSmileBeam, faSmile, faMeh, faFrown, faSadCry } from '@fortawesome/free-solid-svg-icons';
import './NewsCard.css';

function MetricStatusButton(props) {
  return (
    <div className="news-card-score-overlay">
      <MetricStatusButtonInner className={props.className} statusColour={props.statusColour} 
        onStatusButtonClicked={props.onStatusButtonClicked} statusIcon={props.statusIcon} 
        honestyMetric={props.honestyMetric} />
    </div>
  );
}

function MetricStatusButtonInner(props) {
  const shadowClass = 'shadow' in props && props.shadow ? 'shadow' : '';
  return (
    <Button size="md" style={{background: props.statusColour, borderColor: props.statusColour}} 
      className={"news-card-score-button " + shadowClass + " " + props.className} onClick={props.onStatusButtonClicked}
      id={props.id}>
        <div className="w-100 h-100 align-self-center">
          <FontAwesomeIcon icon={props.statusIcon} className="mr-2" />
          <strong>{props.honestyMetric}</strong>
        </div>
    </Button>
  );
}

function GetMetricStatusIcon(metric) {
    // Determine the status icon.
    let statusIcon = faSadCry;
    if (metric >= 90) {
      // If honesty metric is between 100 and 90, use the faSmileBeam icon.
      statusIcon = faSmileBeam;
    }
    // Use the smile icon in the [70, 90) interval.
    if (metric < 90 && metric >= 70) {
      statusIcon = faSmile;
    }
    // Use the meh icon in the [40, 70) interval.
    else if (metric < 70 && metric >= 40) {
      statusIcon = faMeh;
    }
    // Use the frown icon in the [20, 40) interval.
    else if (metric < 40 && metric >= 20) {
      statusIcon = faFrown;
    }

    return statusIcon;
}

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
  
    const statusIcon = GetMetricStatusIcon(this.props.honestyMetric);
    const userStatusIcon = GetMetricStatusIcon(this.props.userHonestyMetric);

    const rippleAnimationClass = this.state.showMetricBreakdown ? 'animate-ripple' : '';
    const rippleOverlayBlockEventsClass = this.state.showMetricBreakdown ? 'block-events' : '';
    const metricBreakdownAnimationClass = this.state.showMetricBreakdown ? 'animate-metric-breakdown-content' : '';
    const userMetricStatusAnimationClass = this.state.showMetricBreakdown ? 'animate-user-metric-status' : '';

    return (
      <Card className="news-card shadow border-0">
        <Row>
          <Col md="9" className="order-12">
            <CardBody className={"callout " + rippleOverlayBlockEventsClass}
               style={{borderLeftColor: statusColour}}>
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
            <MetricStatusButton statusColour={statusColour} statusIcon={statusIcon}
              onStatusButtonClicked={this.onStatusButtonClicked} honestyMetric={this.props.honestyMetric} 
              className="m-3" shadow />
          </Col>
        </Row>
        <Row className="ripple-overlay">
          <div className={"ripple " + rippleAnimationClass} style={{background: statusColour}} />
          <div className="ripple-overlay w-100">
            <Row>
              <Col className="d-flex flex-row justify-content-end">           
                <MetricStatusButtonInner statusColour={statusColour} statusIcon={statusIcon}
                  onStatusButtonClicked={this.onStatusButtonClicked} honestyMetric={this.props.honestyMetric}
                  className="m-3" />
              </Col>
              <div className="w-100"></div>
              <Col className="d-flex flex-row justify-content-end">           
                <MetricStatusButtonInner statusColour={statusColour} statusIcon={userStatusIcon} 
                  honestyMetric={this.props.userHonestyMetric} id="userMetricStatusButton"
                  className={"user-metric-status mx-3 " + userMetricStatusAnimationClass} />
                  <UncontrolledTooltip placement="right" target="userMetricStatusButton">
                    This is how users have rated this source.
                  </UncontrolledTooltip>
              </Col>
            </Row>
          </div>


          <Card className={"ripple-overlay w-100 metric-breakdown-content " + metricBreakdownAnimationClass}>
            <CardBody>
              <CardTitle className="news-card-title mb-0 w-100" tag="h5">
                How was this rated?
              </CardTitle>
            </CardBody>
          </Card>
        </Row>
      </Card>
    )
  }
}
