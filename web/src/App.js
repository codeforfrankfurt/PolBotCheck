import React, { Component } from 'react';
import {Grid, Row, Col} from 'react-bootstrap';
import logo from './logo.svg';
import './App.css';

class App extends Component {
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
                            <Col className="Info-followers" md={6}>
                                <img src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Tortendiagramm_Themen_Pabst.jpg" />
                            </Col>
                            <Col className="Info-retweeters" md={6}>
                                <img src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Tortendiagramm_Themen_Pabst.jpg" />
                            </Col>
                        </Row>
                    </Col>
                </Row>
            </Grid>
        );
    }
}

export default App;
