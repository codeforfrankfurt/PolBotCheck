/**
 * Created by peter on 04.03.17.
 */
import React, {Component} from 'react';
import {Col, Row, Panel} from 'react-bootstrap';
import PieChart from './PieChart';


export default class MemberPage extends Component {

  render() {
    return (
      <div>
        <Col className="App-profile" md={4}>
          <img className="Profile-picture"
               src={this.props.member.pictureURL}/>
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
            <PieChart className="Info-followers col-md-6" numbers={this.props.member.followers}/>
            <PieChart className="Info-retweeters col-md-6" numbers={this.props.member.retweets}/>
          </Row>
        </Col>
      </div>
    )
  }
}