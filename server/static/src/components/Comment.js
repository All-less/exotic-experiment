'use strict'
import React from 'react';

class Comment extends React.Component {

  handleChange(e) {
    console.log(e);
  }

  render() {
    return (
      <div id="div_discuss">
        <p>Discuss</p>
        <div id="discuss_contain">
          <li id="text"><input type="text" onChange={this.handleChange}/></li>
          <li id="biu" className="click_button">BIU</li>
        </div>
      </div>
    );
  }
}

export default Comment;
