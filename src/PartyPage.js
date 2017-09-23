import React, {Component} from 'react';
import { Link } from 'react-router'
import {Row, Col, Panel} from 'react-bootstrap';
import Title from './Title'
import { parties, getFullName } from './Utils'
import picPlaceholder from '../public/Portrait_placeholder.png'

class PartyPage extends Component {
    state = {
        party: {
            name: parties[this.props.params.slug]
        },
        candidates: []
    }

    componentWillMount() {
        let self = this;
        const url = 'https://botornot-hessen-api.herokuapp.com/pbc/parties/' + this.props.params.slug;
        fetch(url, {mode: 'cors', headers: {'Accept': 'application/json'}})
            .then(res => {
                return res.json().then(data => {
                    self.state.candidates = data.candidates_by_party;
                    console.log(data);
                    self.setState(self.state);
                });
            })
            .catch(e => console.log("error fetching " + url, e));
    }

    render() {
        let members = this.state.candidates.map(member => (
            <li key={member.id}>
                <Link to={'/politicians/' + member.slug}>{getFullName(member.name)}</Link>
            </li>
        ), this)

        return (<div className="container">
            <Title />
            <div><Link to="/" className="btn btn-default">« Zurück</Link></div>

            <img className="Profile-picture" alt="Parteilogo" src={picPlaceholder} />
            <Panel bsStyle="primary" className="App-profile" bsSize="large">
                <p>Name: {this.state.party.name ? this.state.party.name : '-'}</p>
            </Panel>

            <Row className="App-info">
                <Col xs={12}>
                    <h3>Mitglieder auf den Listen</h3>
                    {members}
                </Col>
            </Row>
        </div>)
    }
}

export default PartyPage;
