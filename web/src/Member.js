/**
 * Created by peter on 04.03.17.
 */
import React, {Component} from 'react';
import {Col, Row, Panel} from 'react-bootstrap';
import PieChart from './PieChart';
import BarChart from './BarChart';

export default class MemberPage extends Component {

  render() {
    return (
      <div>
        <Col className="App-profile" md={4}>
          <img className="Profile-picture"
               src={this.props.member.pictureURL}/>
          <Panel bsStyle="primary"
                 bsSize="large">
            <p>Name: {this.props.member.name ? this.props.member.name : '-'}</p>
            <p>Partei: {this.props.member.party ? this.props.member.party : '-'}</p>
          </Panel>
        </Col>
        <Col className="App-info" md={8}>
          <Row className="Info-diagram">
            <BarChart className="Info-topics" topics={this.props.member.wordCluster.topics}/>
            <p>Die meistbesprochenen Themen des Abgeordneten</p>
          </Row>
          <Row>
            <Col md={6}>
              <PieChart className="Info-followers" numbers={this.props.member.followers}/>
              <p>Follower: Verhältnis von Bots / Menschen</p>
            </Col>
            <Col md={6}>
              <PieChart className="Info-retweets" numbers={this.props.member.retweets}/>
              <p>Retweets: Verhältnis von Bots / Menschen</p>
            </Col>
          </Row>
        </Col>
      </div>
    )
  }
}