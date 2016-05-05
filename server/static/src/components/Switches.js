'use strict'
import React from 'react';

class Switches extends React.Component {
  render() {
    return (
      <div>
        <p>Switch</p>
        <ul id="switch_contain">
          <li className="switch_border">
            <div id="switch1" className="switch"></div>
          </li>
          <li className="switch_border">
            <div id="switch2" className="switch"></div>
          </li>
          <li className="switch_border">
            <div id="switch3" className="switch"></div>
          </li>
          <li className="switch_border">
            <div id="switch4" className="switch"></div>
          </li>
        </ul>
      </div>
    );
  }
}

export default Switches;
