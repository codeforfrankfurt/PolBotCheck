/**
 * Created by peter on 04.03.17.
 */
import React, {Component} from 'react';
import {Col, Row, Panel} from 'react-bootstrap';
import PieChart from './PieChart';
import BarChart from './BarChart';

class MemberPage extends Component {

    state = {
        content: 'OVERVIEW'
    };

    fetchMemberData(memberName) {
        return require('../json/' + memberName + '.json');
    }

    componentWillMount() {
        console.log(this.props.params);
        let newData = this.fetchMemberData(this.props.params.name);
        this.setState(newData);
    }

    render() {
        return (
          <div>
            <Col className="App-profile" md={4}>
              <img className="Profile-picture" alt="Profilbild"
                   src={this.state.member.pictureURL}/>
              <Panel bsStyle="primary"
                     bsSize="large">
                <p>Name: {this.state.member.name ? this.state.member.name : '-'}</p>
                <p>Partei: {this.state.member.party ? this.state.member.party : '-'}</p>
              </Panel>
            </Col>
            <Col className="App-info" md={8}>
              <Row className="Info-diagram">
                <BarChart className="Info-topics" topics={this.state.member.wordCluster.topics}/>
                <p>Die meistbesprochenen Themen des Abgeordneten</p>
              </Row>
              <Row>
                <Col md={6}>
                  <PieChart className="Info-followers" numbers={this.state.member.followers}/>
                  <p>Follower: Verhältnis von Bots / Menschen</p>
                </Col>
                <Col md={6}>
                  <PieChart className="Info-retweets" numbers={this.state.member.retweets}/>
                  <p>Retweets: Verhältnis von Bots / Menschen</p>
                </Col>
              </Row>
            </Col>
          </div>
        )
  }
}

export default MemberPage;
