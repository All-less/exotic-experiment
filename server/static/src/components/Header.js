'use strict'
import React from 'react';

class Header extends React.Component {
  render() {
    return (
      <header>
        <span id="word_exotic">Exotic</span>
        <ul id="nav">
          <li><a href="#">Setting</a></li>
          <li><a href="#">Apply</a></li>
          <li><a href="#">Logout</a></li>
          <li><a href="#">Help</a></li>
        </ul>
      </header>
    );
  }
}

export default Header;
