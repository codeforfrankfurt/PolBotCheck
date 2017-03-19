import React, {Component} from 'react'
import { Link } from 'react-router'
import {Grid, Row, Col, Jumbotron} from 'react-bootstrap'
import logo from './logo.svg'
import './App.css'

class App extends Component {

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
                      <li><Link to="/politicians/AngelaMerkel">Angela Merkel</Link></li>
                      <li>Martin Schulz</li>
                      <li>Dietmar Bartsch</li>
                      <li>Sahra Wagenknecht</li>
                      <li>Katrin Göring-Eckardt</li>
                      <li>Cem Özdemir</li>
                      <li>Christian Lindner</li>
                  </ul>
              </Col>
              <Col md={4}>
                  <h3>Parteien</h3>
                  <ul>
                      <li>CDU</li>
                      <li>SPD</li>
                      <li>Linke</li>
                      <li>Grüne</li>
                      <li>FDP</li>
                      <li>AfD</li>
                  </ul>
              </Col>
              <Col md={4}>
                  <h3>Themen</h3>
                  <ul>
                      <li>Flüchtlinge</li>
                      <li>Steuern</li>
                      <li>Renten</li>
                      <li>Agenda</li>
                  </ul>
              </Col>
          </Row>
      </Grid>
    );
  }
}

export default App;
