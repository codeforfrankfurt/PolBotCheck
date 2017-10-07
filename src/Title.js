import React, {Component} from 'react'
import {Row, Col} from 'react-bootstrap'
import logo from './logo.png'
import './Title.css'

class Title extends Component {
    render() {
        return (<Row><Col xs={12} className="main-title">
            <a href="http://codefor.de/frankfurt">
                <img className="App-logo" src={logo} alt="Logo von Code for Frankfurt"/>
            </a>
            <h1>BotOrNot</h1>
            <p>hessische BTW-Kandidaten 2017</p>
        </Col></Row>)
    }
}

export default Title
