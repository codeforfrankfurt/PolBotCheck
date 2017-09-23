import React, {Component} from 'react';
import { Link } from 'react-router'
import {Row, Col, Panel} from 'react-bootstrap';
import Title from './Title'
import { parties, getFullName } from './Utils'

class DistrictPage extends Component {
    state = {
        district: {
            name: '',
            candidates: []
        }
    }

    componentWillMount() {
        let self = this;
        const url = 'https://botornot-hessen-api.herokuapp.com/pbc/districts/' + this.props.params.slug;
        fetch(url, {mode: 'cors', headers: {'Accept': 'application/json'}})
            .then(res => {
                return res.json().then(data => {
                    self.state = data;
                    console.log(data);
                    self.setState(self.state);
                });
            })
            .catch(e => console.log("error fetching " + url, e));
    }

    render() {
        let candidates = this.state.district.candidates.map(candidate => {
            const fullName = getFullName(candidate.name);
            const party = parties[candidate.election.party];
            return (
                <li key={candidate.id}>
                    <Link to={'/politicians/' + candidate.slug}>{fullName + " (" + party + ") "}</Link>
                </li>
            );
        }, this)

        return (<div className="container">
            <Title />
            <div><Link to="/" className="btn btn-default">« Zurück</Link></div>

            <Panel bsStyle="primary" className="App-profile" bsSize="large">
                <p>Wahlkreis: {this.state.district.name ? this.state.district.name : '-'}</p>
            </Panel>

            <Row className="App-info">
                <Col xs={12}>
                    <h3>Mitglieder im Wahlkreis</h3>
                    {candidates}
                </Col>
            </Row>
        </div>)
    }
}

export default DistrictPage;
