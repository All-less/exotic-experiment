'use strict'
import React from 'react';

class Comment extends React.Component {
  render() {
    return (
      <div id="div_discuss">
        <p>Discuss</p>
        <div id="discuss_contain">
          <li id="text"><input type="text" /></li>
          <li id="biu" className="click_button">BIU</li>
        </div>
      </div>
    );
  }
}

export default Comment;
