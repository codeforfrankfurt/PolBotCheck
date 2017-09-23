import React, {Component} from 'react'
import { Link } from 'react-router'
import {Grid, Row, Col, Jumbotron, Panel} from 'react-bootstrap'

import './App.css'
import Title from './Title'
import { parties, getFullName } from './Utils'

class App extends Component {

  state = {
      politicians: [],
      parties: parties,
      districts: {districts: []}
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
    this.load('districts', 'https://botornot-hessen-api.herokuapp.com/pbc/districts');
    this.load('politicians', '/candidates.json');
  }

  getCandidateEntry(candidate) {
    const fullName = getFullName(candidate.name);
    return fullName.concat(" (" + this.state.parties[candidate.election.party] + ")");
  }

  render() {
    const politicians = this.state.politicians.sort((a, b) => a.name.surname.localeCompare(b.name.surname));
    const parties = this.state.parties;
    const districts = this.state.districts.districts;
    return (
      <Grid className="App">
        <Title />
        <Row>
          <Jumbotron>
            <h2>
                Twitter Bots folgen vielen Accounts, wieviele sind unter den Followern unserer BTW-Kandidaten 2017?
            </h2>
            <p>
                Twitter Bots sind computergesteuerte Programme die sich automatisiert auf dem Social Network bewegen
                und verschiedene Ziele verfolgen. Die meisten betreiben quasi Marketing und folgen wild allen möglichen
                Accounts und erzeugen so Aufmerksamkeit. Andere sorgen aber mit Retweets für eine größere
                Reichweite anderer Accounts die sie voranbringen wollen.
            </p>
            <p>
                Gut wäre da nun Einblick, wieviele Retweets der
                Politiker von Bots sind, um besser einschätzen zu können, ob da nachgeholfen wird.  Zur Erkennung ob ein
                Twitter Account ein Bot ist, verlassen wir uns auf die mehrjährige Recherche-Arbeit des Projekts&nbsp;
                <a href="http://truthy.indiana.edu/botornot/">Botometer</a> (früher Truthy BotOrNot). Es wurde 2014 von
                der Indiana University aus den USA ins Leben gerufen. Über deren Web-Dienst kann man die
                Wahrscheinlichkeit einholen, mit der ein Twitter Account ein Bot ist. Wir gehen ab 70% Prozent davon aus,
                dass es sich um einen Bot handelt.
            </p>
            <p>
                Für jeden Politiker zu dem wir die Daten einholen konnten (die Datenlage ist recht eingeschränkt, siehe
                Quellen ganz unten, daher auch die fehlenden Parteien und Wahlkreise), zeigen wir hier nun den <strong>Anteil
                der Follower die Bots sind, den Anteil der Retweets die von Bots stammen und wieviel Prozent der
                Retweeter Bots sind.</strong>
            </p>
          </Jumbotron>
        </Row>
          <Row>
              <Col md={4}>
                  <h3>Politiker</h3>
                  <ul>
                    {politicians.map(function(value) {
                        return <li key={value.id}>
                          <Link to={'/politicians/' + value.slug}>
                            {this.getCandidateEntry(value)}</Link></li>
                    },this)}
                  </ul>
              </Col>
              <Col md={4}>
                  <h3>Parteien</h3>
                  <ul>
                      {Object.keys(parties).map(function(key) {
                            const value = parties[key];
                            return <li key={key}><Link to={'/parties/' + key}>{value}</Link></li>;
                      })}
                  </ul>
              </Col>
              <Col md={4}>
                  <h3>Wahlkreise</h3>
                  <ul>
                      {districts.map(function(districtObject) {
                          return <li key={districtObject.id}><Link to={'/districts/' + districtObject.id}>{districtObject.name}</Link></li>;
                      })}
                  </ul>
              </Col>
        </Row>
        <Row>
          <Panel id="footer" header="Quellen">
            <p>
                Die Liste der Politiker und die Infos über sie, u.a. die Account-Namen der Twitter-Profile haben wir über&nbsp;
                <a href="https://github.com/okfde/wahldaten/tree/master/kandidierende">github.com/okfde/wahldaten</a> eingeholt.
            </p>
            <p>
                Die Wahrscheinlichkeit ob ein Account ein Bot ist, holen wir uns über&nbsp;
                <a href="http://truthy.indiana.edu/botornot/">Botometer</a> (früher Truthy BotOrNot) von der
                Indiana University aus den USA ein.
            </p>
            <p>
                Die Follower und Retweet Daten sind über die <a href="https://dev.twitter.com/rest/public">Twitter-API</a>
                &nbsp;von Twitter selbst eingeholt worden.
            </p>
            <p>
                Die Namen der Wahlkreise haben wir über die&nbsp;
                <a href="https://www.abgeordnetenwatch.de/api/">Abgeordnetenwatch API</a> abgerufen.
            </p>
          </Panel>
        </Row>
      </Grid>
    );
  }
}

export default App;
