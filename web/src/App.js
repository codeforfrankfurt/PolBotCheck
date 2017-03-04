import React, { Component } from 'react';
import {Grid, Row, Col} from 'react-bootstrap';
import PieChart from './PieChart';
import logo from './logo.svg';
import './App.css';

class App extends Component {
    componentDidMount() {
        var script = document.createElement('script');
        script.setAttribute('src', '//d3js.org/d3.v3.min.js');
        document.body.appendChild(script)
    }

    render() {
        return (
            <Grid className="App">
                <Col className="App-header" xs={12}>
                    <img src={logo} className="App-logo" alt="logo" />
                    <h2>Welcome to PolBotCheck</h2>
                </Col>
                <Row>
                    <Col className="App-profile" md={4}>
                        <img className="Profile-picture" src="https://upload.wikimedia.org/wikipedia/commons/9/93/Angela_Merkel_2016.jpg" />
                        <div>Angela Merkel</div>
                    </Col>
                    <Col className="App-info" md={8}>
                        <Col className="Info-diagram">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/f/fd/Lowestbirthrates.svg" />
                        </Col>
                        <Row>
                            <PieChart className="Info-followers col-md-6"></PieChart>
                            <PieChart className="Info-retweeters col-md-6"></PieChart>
                        </Row>
                    </Col>
                </Row>
            </Grid>
        );
    }
}

export default App;
