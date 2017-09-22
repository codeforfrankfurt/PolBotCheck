import React, {Component} from 'react'
import { Link } from 'react-router'
import {Grid, Row, Col, Jumbotron} from 'react-bootstrap'
import logo from './logo.svg'
import './App.css'

class App extends Component {

  state = {
      politicians: [],
      parties: [],
      districts: {candidates_by_district: []}
  };

  load(what, url) {
      let self = this;
      fetch(url)
          .then(res => res.json())
          .then(data => {
              self.state[what] = data.data || data;
              self.setState(self.state);
          })
          .catch(e => console.log(e))
  }

  componentWillMount() {
    this.load('parties', 'https://trustfact.dilab.co/api/v2/parties');
    this.load('districts', 'http://localhost:6755/pbc');
    this.load('politicians', 'http://localhost:3000/candidates.json');
  }

  getFullName(name) {
    let fullName = [];
    if(name['titles']) {
      fullName = fullName.concat(name['titles']+ ' ')
    }
    if(name['forename']){
      fullName = fullName.concat(name['forename']+ ' ')
    }
    if(name['surname']){
      fullName = fullName.concat(name['surname']+ ' ')
    }
    if(name['affix']){
      fullName = fullName.concat(name['affix'])
    }
    return fullName
  }

  render() {
    const districts = this.state.districts.candidates_by_district;
    if (districts[0]) {
        districts[0].district = "Landesliste"
    }
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
                We use information from <a href="http://truthy.indiana.edu/botornot/">Truthy BotOrNot</a>, a project
                from Indiana University, which calculates a probability of a Twitter account being a bot or a human.
                We check that on retweeters of a politician and calculate a score for each topic (aka hashtag) he or
                she is talking about. This helps to identify, if a tweet is really interesting to the public or if it
                is only interesting for certain bots.
            </p>
            <p>
                The list of politicians was loaded from <a href="https://github.com/okfde/wahldaten">github.com/okfde/wahldaten</a>.
            </p>
          </Jumbotron>
        </Row>
          <Row>
              <Col md={4}>
                  <h3>Politiker</h3>
                  <ul>
                    {this.state.politicians.map(function(value) {
                        return <li key={value.id}>
                          <Link to={'/politicians/' + value.slug}>
                            {this.getFullName(value.name)}</Link></li>
                    },this)}
                  </ul>
              </Col>
              <Col md={4}>
                  <h3>Parteien</h3>
                  <ul>
                      {this.state.parties.map(function(value) {
                          return <li key={value.id}><Link to={'/parties/' + value.name}>{value.name} - {value.longName}</Link></li>;
                      })}
                  </ul>
              </Col>
              <Col md={4}>
                  <h3>Wahlkreise</h3>
                  <ul>
                      {districts.map(function(districtObject) {
                          return <li key={districtObject.district}><Link to={'/pbc/district/' + districtObject.district}>{districtObject.district}</Link></li>;
                      })}
                  </ul>
              </Col>
          </Row>
      </Grid>
    );
  }
}

export default App;
