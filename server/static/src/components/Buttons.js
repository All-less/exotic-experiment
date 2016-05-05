'use strict'
import React from 'react';

class Buttons extends React.Component {
  render() {
    return (
      <div>
        <p>Button</p>
        <ul id="button_contain">
          <li className="button_border">
            <div id="button1" className="button"></div>
          </li>
          <li className="button_border">
            <div id="button2" className="button"></div>
          </li>
          <li className="button_border">
            <div id="button3" className="button"></div>
          </li>
          <li className="button_border">
            <div id="button4" className="button"></div>
          </li>
        </ul>
      </div>
    );
  }
}

export default Buttons;
