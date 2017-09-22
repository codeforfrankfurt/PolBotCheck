import React, {Component} from 'react'
import { Link } from 'react-router'
import {Grid, Row, Col, Jumbotron, Panel} from 'react-bootstrap'
import './App.css'
import Title from './Title'

class App extends Component {

  state = {
      politicians: [],
      parties: [
        {name: "AfD", slug: 'afd'},
        {name: "CDU", slug: 'cdu'},
        {name: "Grüne", slug: 'gruene'},
        {name: "Linke", slug: 'linke'},
        {name: "SPD", slug: 'spd'}
      ],
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
                Reichweite anderer Accounts die sie voranbringen wollen. Gut wäre da nun Einblick, wieviele Retweets der
                Politiker von Bots sind, um besser einschätzen zu können, ob da nachgeholfen wird.  Zur Erkennung ob ein
                Twitter Account ein Bot ist, verlassen wir uns auf die mehrjährige Recherche-Arbeit des Projekts&nbsp;
                <a href="http://truthy.indiana.edu/botornot/">Botometer</a> (früher Truthy BotOrNot). Es wurde 2014 von
                der Indiana University aus den USA ins Leben gerufen. Über deren Web-Dienst kann man die
                Wahrscheinlichkeit einholen, mit der ein Twitter Account ein Bot ist. Wir gehen ab 70% Prozent davon aus,
                dass es sich um einen Bot handelt.
            </p>
            <p>
                Für jeden Politiker zu dem wir die Daten einholen konnten (siehe Quellen unten), zeigen wir hier nun den&nbsp;
                <strong>Anteil der Follower die Bots sind, den Anteil der Retweets die von Bots stammen und wieviel
                Prozent der Retweeter Bots sind.</strong>
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
                          return <li key={value.slug}><Link to={'/parties/' + value.slug}>{value.name}</Link></li>;
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
          <Panel id="footer" header="Quellen">
            <p>
                Die Liste der Politiker und die Infos über sie, u.a. die Twitter-Profile haben wir über
                <a href="https://github.com/okfde/wahldaten/tree/master/kandidierende">github.com/okfde/wahldaten</a> eingeholt.
            </p>
            <p>
                Die Wahrscheinlichkeit ob ein Account ein Bot ist, holen wir uns über&nbsp;
                <a href="http://truthy.indiana.edu/botornot/">Botometer</a> (früher Truthy BotOrNot) von der
                Indiana University aus den USA ein.
            </p>
            <p>
                Die Follower und Retweet Daten sind über die Twitter-API von Twitter selbst eingeholt worden.
            </p>
          </Panel>
        </Row>
      </Grid>
    );
  }
}

export default App;
