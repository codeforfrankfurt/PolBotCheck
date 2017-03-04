import React from 'react';
import ReactDOM from 'react-dom';
import Routes from './routes.js';
import {browserHistory} from 'react-router';
import './index.css';

ReactDOM.render(
  <Routes history={browserHistory}>
  </Routes>,
  document.getElementById('root')
);
