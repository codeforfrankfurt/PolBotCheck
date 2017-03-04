import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to PolBotCheck</h2>
        </div>
        <div className="App-profile">
            <img className="Profile-picture" src="https://upload.wikimedia.org/wikipedia/commons/9/93/Angela_Merkel_2016.jpg" />
            <div>Angela Merkel</div>
        </div>
        <div className="App-info">
            <div className="Info-diagram">
                <img src="https://upload.wikimedia.org/wikipedia/commons/f/fd/Lowestbirthrates.svg" />
            </div>
            <div className="Info-followers">
                <img src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Tortendiagramm_Themen_Pabst.jpg" />
            </div>
            <div className="Info-retweeters">
                <img src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Tortendiagramm_Themen_Pabst.jpg" />
            </div>
        </div>
      </div>
    );
  }
}

export default App;
