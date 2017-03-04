import React, {Component} from 'react';
import {Grid, Row, Col} from 'react-bootstrap';
import PieChart from './PieChart';
import logo from './logo.svg';
import './App.css';
import {Button, Panel} from 'react-bootstrap';

class App extends Component {
    state = {
        member: {
            name: "max meister",
            pictureURL: "http://www.billboard.com/files/styles/article_main_image/public/media/donald-trump-thumbs-up-aug-2015-billboard-650.jpg",
            party: "Die Linke",
            followers: {
                numFollowers: 3141592653,
                ratioBots: "22%"
            },
            retweets: {
                numRetweets: 1248653,
                ratioBots: "47%"
            },
            wordCluster: {
                hashTags: [
                    "#fakeNews",
                    "#letsBuildAWall"
                ],
                topics: [
                    "immigration",
                    "freeSpeech"
                ]
            }
        }
    };

    render() {
        return (
            <Grid className="App">
                <Col className="App-header" xs={12}>
                    <img src={logo} className="App-logo" alt="logo"/>
                    <h2>Welcome to PolBotCheck</h2>
                </Col>
                <Row>
                    <Col className="App-profile" md={4}>
                        <img className="Profile-picture"
                            src="https://upload.wikimedia.org/wikipedia/commons/9/93/Angela_Merkel_2016.jpg"/>
                        <div>Angela Merkel</div>
                    </Col>
                    <Col className="App-info" md={8}>
                        <Col className="Info-diagram">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/f/fd/Lowestbirthrates.svg"/>
                        </Col>
                        <Row>
                            <PieChart className="Info-followers col-md-6"></PieChart>
                            <PieChart className="Info-retweeters col-md-6"></PieChart>
                        </Row>
                    </Col>
                </Row>
                <div className="master">
                    <Button onClick={ ()=> {
                        location.replace('http://localhost:3000/PartyPage');
                    }
                        }>Partei
                    </Button>
                </div>
                <div>
                    <Panel bsStyle="primary"
                        bsSize="large"
                    >Name: {this.state.member.name}</Panel>

                </div>
            </Grid>
        );
    }
}

export default App;
