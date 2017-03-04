/**
 * Created by peter on 04.03.17.
 */
import React, {Component} from 'react';
import {Col, Row, Panel} from 'react-bootstrap';

export default class MemberPage extends Component {

  componentWillMount() {
    this.state = this.props;
  }

  componentWillReceiveProps() {
    this.setState(this.props);
  }

  render() {
    return (
      <div>
        <Col className="App-profile" md={4}>
          <img className="Profile-picture"
               src="https://upload.wikimedia.org/wikipedia/commons/9/93/Angela_Merkel_2016.jpg"/>
          <Panel bsStyle="primary"
                 bsSize="large">
            <p>Name: {this.props.member.name ? this.props.member.name : '-' + '\n'}</p>
            <p>Partei: {this.props.member.party ? this.props.member.party : '-'}</p>
          </Panel>
        </Col>
        <Col className="App-info" md={8}>
          <Col className="Info-diagram">
            <img src="https://upload.wikimedia.org/wikipedia/commons/f/fd/Lowestbirthrates.svg"/>
          </Col>
          <Row>
            <Col className="Info-followers" md={6}>
              <img src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Tortendiagramm_Themen_Pabst.jpg"/>
            </Col>
            <Col className="Info-retweeters" md={6}>
              <img src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Tortendiagramm_Themen_Pabst.jpg"/>
            </Col>
          </Row>
        </Col>
      </div>
    )
  }
}