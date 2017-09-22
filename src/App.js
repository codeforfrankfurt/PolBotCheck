import React, {Component} from 'react'
import { Link } from 'react-router'
import {Grid, Row, Col, Jumbotron, Panel} from 'react-bootstrap'
import logo from '../public/logo.png'
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
    this.load('districts', 'https://botornot-hessen-api.herokuapp.com/pbc');
    this.load('politicians', '/candidates.json');
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
          <a href="http://codefor.de/frankfurt">
            <img src={logo} className="App-logo" alt="Logo von Code for Frankfurt"/>
          </a>
          <h1>BotOrNot hessische BTW-Kandidaten 2017</h1>
        </Row>
        <Row>
          <Jumbotron>
            <h2>
                Twitter Bots folgen vielen Accounts, wieviele sind unter den Followern unserer BTW-Kandidaten 2017?
            </h2>
            <p>
                Twitter Bots sind computergesteuerte Programme die sich automatisiert auf dem Social Network bewegen
                und verschiedene Ziele verfolgen. Die meisten betreiben quasi Marketing und folgen wild allen möglichen
                Accounts und tauchen so in deren Benachrichtigungen auf. Andere sorgen aber mit Retweets für eine größere
                Reichweite anderer Accounts die sie voranbringen wollen. Gut wäre da nun Einblick, wieviele Retweets der
                Politiker von Bots sind, um besser einschätzen zu können, ob da nachgeholfen wird.  Zur Erkennung ob ein
                Twitter Account ein Bot ist, verlassen wir uns auf die mehrjährige Recherche-Arbeit des Projekts
                <a href="http://truthy.indiana.edu/botornot/">Botometer</a> (früher Truthy BotOrNot). Es wurde 2014 von
                der Indiana University aus den USA ins Leben gerufen. Über deren Web-Dienst kann man die
                Wahrscheinlichkeit einholen, mit der ein Twitter Account ein Bot ist. Wir gehen ab 70% Prozent davon aus,
                dass es sich um einen Bot handelt.
            </p>
            <p>
                <strong>
                Für jeden Politiker zu dem wir die Daten einholen konnten, zeigen wir hier nun den Anteil der Follower
                die Bots sind, den Anteil der Retweets die von Bots stammen und wieviel Prozent der Retweeter Bots sind.
                </strong>
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
        <Row>
          <Panel header="Quellen">
            Die Liste der Politiker und die Infos über sie, u.a. die Twitter-Profile haben wir über
            <a href="https://github.com/okfde/wahldaten/tree/master/kandidierende">github.com/okfde/wahldaten</a> eingeholt.

            Die Wahrscheinlichkeit ob ein Account ein Bot ist, holen wir uns über
            <a href="http://truthy.indiana.edu/botornot/">Botometer</a> (früher Truthy BotOrNot) von der
            Indiana University aus den USA ein.

            Die Follower und Retweet Daten sind über die Twitter-API von Twitter selbst eingeholt worden.
          </Panel>
        </Row>
      </Grid>
    );
  }
}

export default App;
