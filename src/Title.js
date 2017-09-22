import React, {Component} from 'react'
import {Row} from 'react-bootstrap'
import logo from '../public/logo.png'
import './Title.css'

class Title extends Component {
    render() {
        return (<Row>
            <a href="http://codefor.de/frankfurt">
                <img className="App-logo" src={logo} alt="Logo von Code for Frankfurt"/>
            </a>
            <h1 className="main-title">BotOrNot hessische BTW-Kandidaten 2017</h1>
        </Row>)
    }
}

export default Title