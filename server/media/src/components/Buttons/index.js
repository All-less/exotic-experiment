'use strict'
import React from 'react';
import { connect } from 'react-redux'
import remote from '../../socket'; 
import { state } from '../../redux/device';

import style from './style';

/* BTN_UP, BTN_DOWN和BTN_WAIT对应的尺寸*/
const size = [5, 9, 7];

@connect(
  (state) => ({
    status: state.device.buttons,
    occupied: state.device.occupied,
    buttons: state.device.buttons
  })
)
class Buttons extends React.Component {

  getClickCallback = (i) => {
    if (!this.props.occupied)
      return null;
    if (this.props.buttons[i] === state.BTN_UP) {
      return remote.pressButton.bind(undefined, i);
    } else if (this.props.buttons[i] === state.BTN_DOWN) {
      return remote.releaseButton.bind(undefined, i);
    } else {
      return null;
    }
  }

  render() {
    const { status, occupied } = this.props;
    return (
      <div>
        <p style={{color: occupied ? '#fff' : '#777' }}>虚拟按钮</p>
        <div id="button_contain">
          {
            Array(4).fill(0).map((e, i) => (
              <div key={i} className={style.button_border}
                   onClick={this.getClickCallback(i)}
                   style={{borderColor: occupied ? '#fff' : '#777' }}>
                <div id={`button${i+1}`}
                     className={style.button}
                     style={{ 
                      height: size[status[i]] * 2,
                      width: size[status[i]] * 2,
                      borderRadius: size[status[i]],
                      margin: 13 - size[status[i]],
                      backgroundColor: occupied ? '#fff' : '#777'
                     }}/>
              </div>
            ))
          }
        </div>
      </div>
    );
  }
}

export default Buttons;
