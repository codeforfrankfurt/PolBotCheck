/**
 * Created by peter on 04.03.17.
 */
import React, {Component} from 'react';
import {Panel} from 'react-bootstrap';

export class PartyPage extends Component {
  state = {
    items: ['']
  };

  render() {
    const innerButton =
      <Button bsSize="large"
              onClick={()=>console.log('inner button')}>
        hello</Button>;
    return (
      <div>
        <PageHeader>
          Create Task
        </PageHeader>
        <this.SortableList
          items={this.state.items}
          onSortEnd={this.onSortEnd}
          useDragHandle={true}/>

        <Button bsStyle="primary"
                bsSize="large"
                onClick={this.addElement.bind(this)}
        >Add new question</Button>
        {' '}
        <Button bsStyle="primary"
                bsSize="large"
                onClick={this.createTask.bind(this)}
        >Create Task</Button>
        <Panel bsStyle="primary"
               bsSize="large"
               onClick={()=>console.log('outerButton')}
        >just a button {innerButton}</Panel>

      </div>
    )

  }
}