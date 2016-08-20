'use strict'
import React from 'react';

class Setting extends React.Component {
  render() {
    return (
      <div id="buttons_contain">
        <p className="classNameify">Input using</p>
        <div className="setting">
          <div className="button_border">
            <div className="button"></div>
          </div>
          <div className="setting_word">buttons & switches</div>
        </div>
        <div className="setting">
          <div className="button_border">
            <div className="button button_choosen"></div>
          </div>
          <div className="setting_word">script input</div>
        </div>
        <p className="classNameify">Key-stroke should be</p>
        <div className="setting">
          <div className="button_border">
            <div className="button"></div>
          </div>
          <div className="setting_word">read and simulated</div>
        </div>
        <div className="setting">
          <div className="button_border">
            <div className="button"></div>
          </div>
          <div className="setting_word">ignored</div>
        </div>
        <p className="classNameify">Switch to</p>
        <div id="device_contain">
          <select name="device" id="device">
          <option value="1">Device 0</option>
          <option value="2">Device 1</option>
          <option value="3">Device 2</option>
          <option value="4">Device 3</option>
          </select>
        </div>
        <div id="confirm_cancel">
          <ul id="about_button">
            <li id="upload" className="click_button">CONFIRM</li>
            <li id="program" className="click_button">CANCEL</li>
          </ul>
        </div>
      </div>
    );
  }
}

export default Setting;
