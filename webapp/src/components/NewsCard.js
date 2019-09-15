import React, { Component } from 'react';
import {
  Col, Row, Button,
  Card, CardImg, CardText, CardBody, CardTitle,
  Modal, ModalHeader, ModalBody, ModalFooter,
  UncontrolledTooltip, Progress 
} from 'reactstrap';
import Truncate from 'react-truncate';
import lerpColour from 'color-interpolate';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSmileBeam, faSmile, faMeh, faFrown, faSadCry, faUsers, faPoll } from '@fortawesome/free-solid-svg-icons';
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
      rateSurveyModal: false,
      showMetricBreakdown: false
    }

    this.onCardClick = this.onCardClick.bind(this);
    this.onStatusButtonClicked = this.onStatusButtonClicked.bind(this);
    this.showSurveyModal = this.showSurveyModal.bind(this);
  }

  onCardClick() {
    window.open(this.props.url, '_blank');
  }

  onStatusButtonClicked() {
    this.setState({
      showMetricBreakdown: !this.state.showMetricBreakdown
    });
  }

  showSurveyModal() {
    this.setState(prevState => ({
      rateSurveyModal: !prevState.rateSurveyModal
    }));
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
    const rateButtonAnimationClass = this.state.showMetricBreakdown ? 'animate-rate-button' : '';

    const breakdownFactorBars = this.props.breakdownFactors.map((factor) => (
      <Col md="6" className="pl-0">  
        <div className="text-left">{factor.name}</div>
        <Progress value={factor.value} max="100" />
      </Col>
    ));

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
              <div className="w-100"></div>
              <Col className="d-flex flex-row justify-content-end align-bottom">
                <Button size="md" color="dark" className={"m-3 news-card-score-button rate-button " + rateButtonAnimationClass}
                  onClick={this.showSurveyModal}>
                    <div className="w-100 h-100 align-self-center">
                      <FontAwesomeIcon icon={faPoll} className="mr-2" />
                      <strong>Rate</strong>
                    </div>
                </Button>
                <Modal isOpen={this.state.rateSurveyModal} toggle={this.showSurveyModal}>
                  <ModalHeader toggle={this.showSurveyModal}>Rate it yourself!</ModalHeader>
                  <ModalBody>
                  {/* <script>(function(t,e,s,n){var o,a,c;t.SMCX=t.SMCX||[],e.getElementById(n)||(o=e.getElementsByTagName(s),a=o[o.length-1],c=e.createElement(s),c.type="text/javascript",c.async=!0,c.id=n,c.src=["https:"===location.protocol?"https://":"http://","widget.surveymonkey.com/collect/website/js/tRaiETqnLgj758hTBazgd7WnuXmrKllSQSuChpOpd0loMeAHVCg1FaiaEsk547HF.js"].join(""),a.parentNode.insertBefore(c,a))})(window,document,"script","smcx-sdk");</script> */}
                  </ModalBody>
                  <ModalFooter>
                    <Button color="primary" onClick={this.showSurveyModal}>Done!</Button>{' '}
                  </ModalFooter>
                </Modal>
              </Col>
            </Row>
          </div>

          <Card className={"ripple-overlay w-100 metric-breakdown-content " + metricBreakdownAnimationClass}>
            <CardBody>
              <CardTitle className="news-card-title mb-0 w-100" tag="h5">
                How was this rated?
              </CardTitle>
              <Col md="9" sm="9" xs="8">
                <Row className="mt-2">
                  {breakdownFactorBars}
                </Row>
              </Col>
            </CardBody>
          </Card>
        </Row>
      </Card>
    )
  }
}
