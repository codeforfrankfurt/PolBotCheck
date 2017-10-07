import React, {Component} from 'react'
import BrowserHistory from 'react-router/lib/browserHistory'
import './Breadcrumbs.css'

class Breadcrumbs extends Component {
  render() {
    return (<div className="breadcrumbs">
      <button onClick={BrowserHistory.goBack} className="btn btn-default">« Zurück</button>
    </div>
    )
  }
}

export default Breadcrumbs
