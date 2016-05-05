'use strict'
import React from 'react';
import Buttons from './Buttons';
import Switches from './Switches';
import Upload from './Upload';
import KeyStroke from './KeyStroke';
import Comment from './Comment';

class Panel extends React.Component {
  render() {
    return (
      <div id="left">
        <div id="left_contain">
          <Buttons />
          <Switches />
          <Upload />
          <Comment />
          {/*
          <KeyStroke />
          */}
        </div>
      </div>
    );
  }
}

export default Panel;
