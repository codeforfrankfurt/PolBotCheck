import React, {Component} from 'react'
import { withRouter } from 'react-router-dom'
import './Breadcrumbs.css'

class Breadcrumbs extends Component {
  render() {
    return (<div className="breadcrumbs">
      <button onClick={this.props.history.goBack} className="btn btn-default">« Zurück</button>
    </div>
    )
  }
}

export default withRouter(Breadcrumbs)
