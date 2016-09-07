'use strict';
import React from 'react';
import { asyncConnect } from 'redux-connect';

import { loadStatus } from '../../redux/account';

@asyncConnect(
  [{
    promise: ({ store: { dispatch, getState }}) => {
      return dispatch(loadStatus());
    } 
  }]
)
class App extends React.Component {

  render() {
    return (
      <div>{this.props.children}</div>
    );
  }
}

export default App;
