'use strict'
import React from 'react';

import style from './style';

class Setting extends React.Component {
  render() {
    return (
      <div>
       {/*
        <p className={style.title}>Input using</p>
        <div className={style.item}>
          <div className={style.button_border}>
            <div className={style.button}></div>
          </div>
          <div className={style.option}>buttons & switches</div>
        </div>
        <div className={style.item}>
          <div className={style.button_border}>
            <div className={`${style.button} ${style.button_chosen}`}></div>
          </div>
          <div className={style.option}>script input</div>
        </div>
        <p className={style.title}>Key-stroke should be</p>
        <div className={style.item}>
          <div className={style.button_border}>
            <div className={style.button}></div>
          </div>
          <div className={style.option}>read and simulated</div>
        </div>
        <div className={style.item}>
          <div className={style.button_border}>
            <div className={style.button}></div>
          </div>
          <div className={style.option}>ignored</div>
        </div>
        */}
        <p className={style.title}>切换设备</p>
        <div className={style.device_wrapper}>
          <select name="device" className={style.device_selector}>
          <option value="1">Device 0</option>
          <option value="2">Device 1</option>
          <option value="3">Device 2</option>
          <option value="4">Device 3</option>
          </select>
        </div>
        <div className={style.button_wrapper}>
          <ul className={style.buttons}>
            <li className="click_button">确认</li>
            <li className="click_button">取消</li>
          </ul>
        </div>
      </div>
    );
  }
}

export default Setting;
