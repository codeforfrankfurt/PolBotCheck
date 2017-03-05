import React, {Component} from 'react';
import {Grid, Row} from 'react-bootstrap';
import logo from './logo.svg';
import './App.css';
import {Jumbotron} from 'react-bootstrap';
import MemberPage from './Member.js';

class App extends Component {

  state = {
    content: 'MEMBER'
  };

  fetchMemberData() {
    let data = require('../json/member.json');
    return data;
  }

  componentWillMount() {
    let newData = this.fetchMemberData();
    this.setState(newData);
  }

  render() {
    return (
      <Grid className="App">
        <Row>
          <img src={logo} className="App-logo" alt="logo"/>
          <h2>Welcome to PolBotCheck</h2>
        </Row>
        <Row>
          <Jumbotron>
            <p>Introduction and description</p>
          </Jumbotron>
        </Row>
        <Row>
          {(()=> {
            switch (this.state.content) {
              case 'MEMBER':
                return <MemberPage member={this.state.member}/>;
                break;
              case 'PARTY':
                return <p>PartyPage</p>;
              case 'TOPIC':
                return <p>TopicPage</p>;
              default:
                return <p>Unknown Page!</p>;
            }
          })()}

        </Row>
      </Grid>
    );
  }
}

export default App;
