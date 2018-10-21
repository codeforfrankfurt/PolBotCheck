import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter, Route } from 'react-router-dom'
import App from './App'
import MemberPage from './MemberPage'
import PartyPage from './PartyPage'
import DistrictPage from './DistrictPage'

ReactDOM.render(
  <BrowserRouter>
    <div>
      <Route exact path="/" component={App}/>
      <Route path="/politicians/:slug" component={MemberPage}/>
      <Route path="/parties/:slug" component={PartyPage}/>
      <Route path="/districts/:slug" component={DistrictPage}/>
    </div>
  </BrowserRouter>,
  document.getElementById('root')
)
