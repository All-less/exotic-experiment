'use strict'
import React from 'react';
import Header from '../Header';
import Panel from '../Panel';
import Simulation from '../Simulation';

import './reset';
import style from './style';

class DevicePage extends React.Component {
  render() {
    return (
      <div>
        <Header />
        <div id="main">
          <Panel />
          <Simulation />
        </div>
      </div>
    );
  }
}

export default DevicePage;
