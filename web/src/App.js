import React, {Component} from 'react'
import { Link } from 'react-router'
import {Grid, Row, Col, Jumbotron} from 'react-bootstrap'
import logo from './logo.svg'
import './App.css'

class App extends Component {

  state = {
      politicians: [],
      parties: [],
      topics: []
  };

  componentWillMount() {
    this.setState({
        politicians: require('../json/politicians.json'),
        parties: require('../json/parties.json'),
        topics: require('../json/topics.json')
    })
  }

  render() {
    return (
      <Grid className="App">
        <Row>
          <img src={logo} className="App-logo" alt="logo"/>
          <h1>Welcome to PolBotCheck</h1>
        </Row>
        <Row>
          <Jumbotron>
            <h2>
                Our goal is to show information about politicians regarding who is retweeting their Twitter tweets,
                if it is humans or bots.
            </h2>
            <p>
                We use information from Truthy BotOrNot, a project from Indiana University, which calculates a
                probability of a Twitter account being a bot or a human. We check that on retweeters of a politician
                and calculate a score for each topic (aka hashtag) he or she is talking about. This helps to identify,
                if a tweet is really interesting to the public or if it is only interesting for certain bots.
            </p>
          </Jumbotron>
        </Row>
          <Row>
              <Col md={4}>
                  <h3>Politiker</h3>
                  <ul>
                    {this.state.politicians.map(function(value) {
                        return <li key={value.screenname}><Link to={'/politicians/' + value.screenname}>{value.name}</Link></li>
                    })}
                  </ul>
              </Col>
              <Col md={4}>
                  <h3>Parteien</h3>
                  <ul>
                      {this.state.parties.map(function(value) {
                          return <li key={value.name}><Link to={'/parties/' + value.name}>{value.name} - {value.longName}</Link></li>;
                      })}
                  </ul>
              </Col>
              <Col md={4}>
                  <h3>Themen</h3>
                  <ul>
                      {this.state.topics.map(function(value) {
                          return <li key={value}><Link to={'/topics/' + value}>{value}</Link></li>;
                      })}
                  </ul>
              </Col>
          </Row>
      </Grid>
    );
  }
}

export default App;
