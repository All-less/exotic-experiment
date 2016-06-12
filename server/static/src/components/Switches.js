'use strict'
import React from 'react';
import { connect } from 'react-redux';
import remote from '../socket';

/* SW_ON, SW_OFF, SW_WAIT对应的margin-top */
const margins = [20, 0, 10];

@connect(
  (state) => ({
    status: state.switches,
    occupied: state.occupied
  })
)
class Switches extends React.Component {
  render() {
    const { status, occupied } = this.props;
    return (
      <div>
        <p style={{color: occupied ? '#fff' : '#777' }}>Switch</p>
        <ul id="switch_contain">
          {
            Array(4).fill(0).map((e, i) => (
              <li key={i} className="switch_border"
                  style={{borderColor: occupied ? '#fff' : '#777' }}>
                <div className="switch"
                     onClick={ 
                       !this.props.occupied ? null : 
                       status[i] === 0/* SW_OFF */ ? remote.openSwitch.bind(undefined, i) :
                       status[i] === 1/* SW_ON  */ ? remote.closeSwitch.bind(undefined, i) : 
                       undefined}
                     style={{
                       marginTop: margins[status[i]],
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

export default Switches;
