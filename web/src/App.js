import React, {Component} from 'react';
import {Grid, Row, Col} from 'react-bootstrap';
import logo from './logo.svg';
import './App.css';
import {Jumbotron, Tabs, Tab} from 'react-bootstrap';
import MemberPage from './Member.js';

class App extends Component {

    state = {};

    fetchMemberData() {
        let data = require('../json/member.json');
        return data;
    }

    componentWillMount() {
        let newData = this.fetchMemberData();
        this.setState(newData);
    }

    handleSelect() {
        this.setState(this.state);
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
                        <p>Introduction and description....</p>
                    </Jumbotron>
                </Row>
                <Row>
                    <Tabs defaultActiveKey={1}
                        id="tab"
                        onSelect={this.handleSelect}>
                        <Tab eventKey={1} title="Member">
              {<MemberPage member={this.state.member}/>}</Tab>
                        <Tab eventKey={2} title="Party">Tab 2 content</Tab>
                        <Tab eventKey={3} title="Topic">Tab 3 content</Tab>
                    </Tabs>
                </Row>
            </Grid>
        );
    }
}

export default App;
