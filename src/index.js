import React from 'react'
import ReactDOM from 'react-dom'
import { Router, Route, browserHistory } from 'react-router'
import App from './App'
import MemberPage from './MemberPage'
import PartyPage from './PartyPage'
import DistrictPage from './DistrictPage'
import './index.css'

ReactDOM.render(
    <Router history={browserHistory}>
        <Route path="/" component={App}/>
        <Route path="/politicians/:slug" component={MemberPage}/>
        <Route path="/parties/:slug" component={PartyPage}/>
        <Route path="/districts/:slug" component={DistrictPage}/>
    </Router>,
    document.getElementById('root')
)
