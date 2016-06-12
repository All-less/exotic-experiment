'use strict'
import React from 'react';
import Header from './Header';
import Panel from './Panel';
import Video from './Video';

class App extends React.Component {
  render() {
    return (
      <div>
        <Header />
        <div id="main">
          <Panel />
          <Video />
        </div>
      </div>
    );
  }
}

export default App;
