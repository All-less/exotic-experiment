'use strict'
import React from 'react';
import remote from '../../socket';

import style from './style';

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

const handleKey = (event) => {
  if (event.keyCode === 13)
    handleClick();
};

class Comment extends React.Component {

  render() {
    return (
      <div id="div_discuss">
        <p>讨论</p>
        <div className={style.discuss_contain}>
          <div className={style.text}><input type="text" className={style.input_biu} onKeyDown={handleKey}/></div>
          <div className={style.biu} onClick={handleClick}>发送</div>
        </div>
      </div>
    );
  }
}

export default Comment;
