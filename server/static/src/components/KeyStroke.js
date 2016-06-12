'use strict'
import React from 'react';

class KeyStroke extends React.Component {
  render() {
    return (
      <div id="div_key_stroke">
        <p>Key-stroke</p>
        <p style={{"margin-left":"15px", "margin-top":0}}>You have pressed key <span id="key">ctrl</span></p>
      </div>
    );
  }
}

export default KeyStroke;
