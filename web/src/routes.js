/**
 * Created by peter on 04.03.17.
 */
import React from 'react';
import {Route, Router} from 'react-router';
import App from './App';
import PartyPage from './Party';

const Routes = (props) => (
  <Router {...props}>
    <Route path="/" component={App}/>
    <Route path="/PartyPage" component={PartyPage}/>
  </Router>
);

export default Routes;