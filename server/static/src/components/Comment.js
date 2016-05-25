'use strict'
import React from 'react';
import remote from '../socket';

const handleClick = () => {
  const content = $("#input_biu").val();
  remote.broadcast(content);
  $("#danmu").danmu("addDanmu", {
    text: content,
    color: "white", 
    size: 1, 
    position: 0, 
    time: $('#danmu').data("nowTime") + 5
  });
  $("#input_biu").val('');
};

class Comment extends React.Component {

  render() {
    return (
      <div id="div_discuss">
        <p>Discuss</p>
        <div id="discuss_contain">
          <li id="text"><input type="text" id="input_biu"/></li>
          <li id="biu" className="click_button" onClick={handleClick}>BIU</li>
        </div>
      </div>
    );
  }
}

export default Comment;
