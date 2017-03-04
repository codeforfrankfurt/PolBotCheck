import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import {Button,Panel} from 'react-bootstrap';

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
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo"/>
          <h2>Welcome to PolBotCheck</h2>
        </div>
        <div className="App-profile">
          <img className="Profile-picture"
               src="https://upload.wikimedia.org/wikipedia/commons/9/93/Angela_Merkel_2016.jpg"/>
          <div>Angela Merkel</div>
        </div>
        <div className="App-info">
          <div className="Info-diagram">
            <img src="https://upload.wikimedia.org/wikipedia/commons/f/fd/Lowestbirthrates.svg"/>
          </div>
          <div className="Info-followers">
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Tortendiagramm_Themen_Pabst.jpg"/>
          </div>
          <div className="Info-retweeters">
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Tortendiagramm_Themen_Pabst.jpg"/>
          </div>
        </div>
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
      </div>

    );
  }


}

export default App;
