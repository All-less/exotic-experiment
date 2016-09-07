'use strict'
import React from 'react';
import { connect } from 'react-redux';
import { toggleSetting } from '../redux';

import remote from '../socket';

const logout = () => {
  $.get('/logout', (res) => {
    const obj = JSON.parse(res)
    if (obj.redirect) {
      location.href = obj.redirect;
    }
  });
};

@connect(
  (state) => ({
    occupied: state.occupied
  }),
  {
    toggleSetting
  }
)
class Header extends React.Component {
  render() {
    return (
      <header>
        <span id="word_exotic">Exotic</span>
        <ul id="nav">
          <li><a onClick={this.props.toggleSetting}>Setting</a></li>
          <li>
            <a onClick={this.props.occupied ? remote.release : remote.acquire}>
             { this.props.occupied ? 'Release' : 'Acquire' }
            </a>
          </li>
          <li><a onClick={logout}>Logout</a></li>
          <li><a href="#">Help</a></li>
        </ul>
      </header>
    );
  }
}

export default Header;
