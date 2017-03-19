import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, browserHistory } from 'react-router'
import App from './App';
import MemberPage from './MemberPage';
import './index.css';

ReactDOM.render(
    <Router history={browserHistory}>
        <Route path="/" component={App}/>
        <Route path="/politicians/:name" component={MemberPage}/>
    </Router>,
    document.getElementById('root')
);
