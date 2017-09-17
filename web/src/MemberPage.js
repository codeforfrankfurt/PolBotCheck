/**
 * Created by peter on 04.03.17.
 */
import React, {Component} from 'react';
import { Link } from 'react-router'
import {Col, Row, Panel} from 'react-bootstrap';
import PieChart from './PieChart';
import BarChart from './BarChart';

class MemberPage extends Component {

    state = {
        content: 'MEMBER',
        member: {
        },
        followers: {
            numHumans: null,
            numBots: null
        },
        retweets: {
            numHumans: null,
            numBots: null
        },
        retweeters: {
            numHumans: null,
            numBots: null
        },
        wordCluster: {
            topics: []
        }
    };

    componentWillMount() {
        let self = this;
        const url = 'http://localhost:6755/pbc/user/' + this.props.params.slug;
        fetch(url, {mode: 'cors', headers: {'Accept': 'application/json'}})
            .then(res => {
                return res.json().then(data => {
                    self.state = data;
                    console.log(data);
                    self.setState(self.state);
                });
            })
            .catch(e => console.log("error fetching " + url, e));
    }

    render() {
        const followerCount = this.state.followers.numHumans + this.state.followers.numBots;
        const retweetCount = this.state.retweets.numHumans + this.state.retweets.numBots;
        const retweetersCount = this.state.retweeters.numHumans + this.state.retweeters.numBots;
        return (
          <div>
            <div><Link to="/">Zurück</Link></div>
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
                <BarChart className="Info-topics" topics={this.state.wordCluster.topics}/>
                <p>Die meistbesprochenen Themen des Abgeordneten</p>
              </Row>
              <Row>
                <Col md={4}>
                  <h3>Follower (Count {followerCount})</h3>
                  <PieChart className="Info-followers" numbers={this.state.followers}/>
                </Col>
                <Col md={4}>
                  <h3>Retweets (Count {retweetCount})</h3>
                  <PieChart className="Info-retweets" numbers={this.state.retweets}/>
                </Col>
                <Col md={4}>
                  <h3>Retweeters (Count {retweetersCount})</h3>
                  <PieChart className="Info-retweeters" numbers={this.state.retweeters}/>
                </Col>
              </Row>
            </Col>
          </div>
        )
    }
}

export default MemberPage;
