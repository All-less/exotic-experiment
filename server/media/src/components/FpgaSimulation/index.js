'use strict';
import React from 'react';

import style from './style';

const seg_styles = [
  {fill: 'white'},
  {fill: 'tomato', filter: 'url(#glow)'}
];

class FpgaSimulation extends React.Component {

  render() {
    const { led, segs } = { led: 0x1234, segs: [1, 2, 4, 8, 16, 32, 64, 128] };
    return (
      <div className={style.media}>
        <img className={style.logo} alt="ZJU LOGO" src="/static/images/zju-logo.png"/>
        <svg className={style.board} width="548" height="448" xmlns="http://www.w3.org/2000/svg" version="1.1">
          <defs>
            <filter id="glow">
              <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          {/* base board of SWORD */}
          <rect x="0" y="0" width="548" height="448" fill="#233387"/>
          {
            /* PMOD */
            Array(5).fill(0).map((e, i) => (
              <g key={i}>
                <rect x="0" y={48 + i * 80} width="20" 
                      height="40" fill="black"/>
                {
                  /* PMOD pins */
                  Array(5).fill(0).map((e, j) => (
                    <rect key={j} x="20" y={48 + i * 80 + 5 + j * 7} 
                          width="4" height="2" fill="gray"/>
                  ))
                }
              </g>
            ))
          }
          {/* VGA display */}
          <rect x="238" y="50" width="260" height="200" fill="black"/>
          <rect x="248" y="60" width="60" height="180" fill="red"/>
          <rect x="308" y="60" width="60" height="180" fill="limegreen"/>
          <rect x="368" y="60" width="60" height="180" fill="blue"/>
          <rect x="428" y="60" width="60" height="180" fill="white"/>
          {
            /* seven-seg display */
            Array(8).fill(0).map((e, i) => (
              <g key={i} transform={`translate(${60 + 40 * i},300)`}>
                <rect x="0" y="0" width="30" height="60" fill="gray"/>
                <polygon points="6,5 8.5,7 21.5,7 24,5 21.5,3 8.5,3" 
                         style={seg_styles[(segs[i] & Math.pow(2, 0)) >> 0]}/>
                <polygon points="25,6 23,8.5 23,26.5 25,29 27,26.5 27,8.5" 
                         style={seg_styles[(segs[i] & Math.pow(2, 1)) >> 1]}/>
                <polygon points="25,31 23,33.5 23,51.5 25,54 27,51.5 27,33.5"
                         style={seg_styles[(segs[i] & Math.pow(2, 2)) >> 2]}/>
                <polygon points="6,55 8.5,57 21.5,57 24,55 21.5,53 8.5,53" 
                         style={seg_styles[(segs[i] & Math.pow(2, 3)) >> 3]}/>
                <polygon points="5,31 3,33.5 3,51.5 5,54 7,51.5 7,33.5" 
                         style={seg_styles[(segs[i] & Math.pow(2, 4)) >> 4]}/>
                <polygon points="5,6 3,8.5 3,26.5 5,29 7,26.5 7,8.5" 
                         style={seg_styles[(segs[i] & Math.pow(2, 5)) >> 5]}/>
                <polygon points="6,30 8.5,32 21.5,32 24,30 21.5,28 8.5,28"
                         style={seg_styles[(segs[i] & Math.pow(2, 6)) >> 6]}/>
              </g>
            ))
          }
          {
            /* LED and switches */
            Array(16).fill(0).map((e, i) => (
              <g key={i}>
                {
                  (led & Math.pow(2, i)) >> i ? [
                    <rect key="1" x={62.5 + 20 * i} y="380" width="3" height="5" fill="lawngreen"/>,
                    <rect key="2" x={62.5 + 20 * i - 2} y="378" width="7" height="9" fill="lawngreen" 
                          filter="url(#glow)" fillOpacity="0.4" rx="2" ry="2"/>
                  ] : (
                    <rect x={62.5 + 20 * i} y="380" width="3" height="5" style={{fill: 'white'}}/>
                  )
                }
                <rect x={60 + 20 * i} y="400" width="8" height="20" fill="gray"/>
                <rect x={61.5 + 20 * i} y="405" width="5" height="10" fill="black"/>
              </g>
            ))
          }
          {
            /* Buttons */
            Array(4).fill(0).map((e, i) => (
              <g key={i}>
                {
                  Array(5).fill(0).map((e, j) => (
                    <g key={j}>
                      <rect x={400 + i * 30} y={303 + j * 25} width="15" height="15" fill="grey"/>
                      <circle cx={400 + i * 30 + 7.5} cy={303 + j * 25 + 7.5} r="5" fill="black"/>
                    </g>
                  ))
                }
              </g>
            ))
          }
        </svg>
      </div>
    );
  }
}

export default FpgaSimulation;
