import React, {Component} from 'react'
import { Link } from 'react-router-dom'
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
                Wer folgt unseren Bundestagswahl-Kandidaten wirklich?
            </h2>
            <p>Sind es Bots oder echte Menschen, die den Kandidaten folgen? Das finden wir hier für euch heraus,
                damit klar wird, was echt ist und was nicht.
            </p>

            <h3>Was sind das für Bots, um die es geht?</h3>
            <p>
                Twitter Bots sind computergesteuerte Programme die sich automatisiert auf dem Social Network bewegen
                und verschiedene Ziele verfolgen. Die meisten betreiben Marketing und folgen allen möglichen
                Accounts und erzeugen so Aufmerksamkeit. Andere sorgen mit Retweets für eine größere
                Reichweite anderer Accounts, die sie voranbringen wollen.
            </p>
            <p>
                Eigentlich ist es noch kein Problem, wenn Bots dem Account eines Kandidaten folgen. Problematisch wird
                es, wenn wir als Wähler die Meldungen eines Kandidaten häufiger zu sehen bekommen, weil sie angeblich
                viele andere interessieren (und daher auch mich interessieren könnten), aber hauptsächlich Bots diese
                Retweets erzeugt haben.
            </p>

            <h3>Und wie erkenne ich, welche Retweets "echt" sind, und was von Bots künstlich erzeugt wird?</h3>
            <p>
                Wir geben dir einen Einblick, wieviele Retweets der Politiker von Bots sind, um besser einschätzen zu können,
                ob nachgeholfen wird. Zur Erkennung ob ein Twitter Account ein Bot ist, verlassen wir uns auf die
                mehrjährige Recherche-Arbeit des <span className="dl"><span className="dd">Projekts&nbsp;
                <a href="http://truthy.indiana.edu/botornot/">Botometer</a></span><span className="dt">früher Truthy BotOrNot</span></span>.
                Es wurde 2014 von der Indiana University aus den USA ins Leben gerufen. Über deren Web-Dienst kann man die
                Wahrscheinlichkeit einholen, mit der ein Twitter Account ein Bot ist.
            </p>
            <p>
                Wir gehen ab 70% Prozent davon aus, dass es sich um einen Bot handelt.
            </p>
            <p>
                Für jeden <span className="dl"><span className="dd">Politiker, zu dem wir die Daten einholen konnten</span>
                <span className="dt">die Datenlage ist recht
                eingeschränkt, siehe Quellen ganz unten, daher auch die fehlenden Parteien und Wahlkreise</span></span>&nbsp;
                zeigen wir hier nun den <strong>Anteil der Follower die Bots sind, den Anteil der Retweets die von Bots
                stammen und wieviel Prozent der Retweeter Bots sind.</strong>
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
            <p>Der Quellcode dieses Projekts ist zu finden auf&nbsp;
                <a href="https://github.com/codeforfrankfurt/PolBotCheck">github</a>.
            </p>
          </Panel>
        </Row>
      </Grid>
    );
  }
}

export default App;
