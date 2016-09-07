'use strict';
import React from 'react';

import FpgaSimulation from '../FpgaSimulation';
import style from './style';

class Simulation extends React.Component {

  render() {
    return (
      <div className={style.right}>
        <div className={style.border}>
          <FpgaSimulation />
          <div className={style.bullet} />
        </div>
      </div>
    );
  }
}

export default Simulation;
