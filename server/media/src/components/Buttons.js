'use strict'
import React from 'react';
import { connect } from 'react-redux'
import remote from '../socket'; 
import { state } from '../redux/device';

/* BTN_UP, BTN_DOWN和BTN_WAIT对应的尺寸*/
const size = [5, 9, 7];

@connect(
  (state) => ({
    status: state.buttons,
    occupied: state.occupied,
    buttons: state.buttons
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
        <p style={{color: occupied ? '#fff' : '#777' }}>Button</p>
        <ul id="button_contain">
          {
            Array(4).fill(0).map((e, i) => (
              <li key={i} className="button_border" 
                  style={{borderColor: occupied ? '#fff' : '#777' }}>
                <div id={`button${i+1}`}
                     className="button" 
                     onClick={this.getClickCallback(i)}
                     style={{ 
                      height: size[status[i]] * 2,
                      width: size[status[i]] * 2,
                      borderRadius: size[status[i]],
                      margin: 13 - size[status[i]],
                      backgroundColor: occupied ? '#fff' : '#777'
                     }}/>
              </li>
            ))
          }
        </ul>
      </div>
    );
  }
}

export default Buttons;
