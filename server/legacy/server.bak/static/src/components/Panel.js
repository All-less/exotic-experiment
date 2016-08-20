'use strict'
import React from 'react';
import { connect } from 'react-redux';

import Buttons from './Buttons';
import Switches from './Switches';
import Upload from './Upload';
import KeyStroke from './KeyStroke';
import Comment from './Comment';
import Setting from './Setting';

@connect(
  (state) => ({
    setting: state.setting
  })
)
class Panel extends React.Component {
  render() {
    return (
      <div id="left">
        { !this.props.setting ? 
            <div id="left_contain">
              <Buttons />
              <Switches />
              <Upload />
              <Comment />
              {/*
              <KeyStroke />
              */}
            </div>
          :
            <div id="left_contain">
              <Setting />
            </div>
        }
      </div>
    );
  }
}

export default Panel;
