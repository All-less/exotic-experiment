const TOGGLE_SETTING = 'Exotic/TOGGLE_SETTING';
const PRESS_BTN = 'Exotic/TRY_PRESS_BTN';
const PRESS_BTN_SUCC = 'Exotic/PRESS_BTN_SUCC';
const PRESS_BTN_FAIL = 'Exotic/PRESS_BTN_FAIL';
const RELEASE_BTN = 'Exotic/RELEASE_BTN';
const RELEASE_BTN_SUCC = 'Exotic/RELEASE_BTN_SUCC';
const RELEASE_BTN_FAIL = 'Exotic/RELEASE_BTN_FAIL';
const OPEN_SWITCH = 'Exotic/OPEN_SWITCH';
const OPEN_SWITCH_SUCC = 'Exotic/OPEN_SWITCH_SUCC';
const OPEN_SWITCH_FAIL = 'Exotic/OPEN_SWITCH_FAIL';
const CLOSE_SWITCH = 'Exotic/CLOSE_SWITCH';
const CLOSE_SWITCH_SUCC = 'Exotic/CLOSE_SWITCH_SUCC';
const CLOSE_SWITCH_FAIL = 'Exotic/CLOSE_SWITCH_FAIL';
const FPGA_ACQUIRED = 'Exotic/FPGA_ACQUIRED';
const FPGA_RELEASED = 'Exotic/FPGA_RELEASED';

const BTN_DOWN = 0;
const BTN_UP = 1;
const BTN_WAIT = 2;
const SW_OFF = 0;
const SW_ON = 1;
const SW_WAIT = 2;

const init = {
  buttons: [BTN_UP, BTN_UP, BTN_UP, BTN_UP],
  switches: [SW_OFF, SW_OFF, SW_OFF, SW_OFF],
  setting: false,
  occupied: false
};

export const toggleSetting = () => ({
  type: TOGGLE_SETTING
});

export const pressButton = (id) => ({
  type: PRESS_BTN,
  id
});

export const pressButtonSucc = (id) => ({
  type: PRESS_BTN_SUCC,
  id
});

export const pressButtonFail = (id) => ({
  type: PRESS_BTN_FAIL,
  id
});

export const releaseButton = (id) => ({
  type: RELEASE_BTN,
  id
});

export const releaseButtonSucc = (id) => ({
  type: RELEASE_BTN_SUCC,
  id
});

export const releaseButtonFail = (id) => ({
  type: RELEASE_BTN_FAIL,
  id
});

export const openSwitch = (id) => ({
  type: OPEN_SWITCH,
  id
});

export const openSwitchSucc = (id) => ({
  type: OPEN_SWITCH_SUCC,
  id
});

export const openSwitchFail = (id) => ({
  type: OPEN_SWITCH_FAIL,
  id
});

export const closeSwitch = (id) => ({
  type: CLOSE_SWITCH,
  id
});

export const closeSwitchSucc = (id) => ({
  type: CLOSE_SWITCH_SUCC,
  id
});

export const closeSwitchFail = (id) => ({
  type: CLOSE_SWITCH_FAIL,
  id
});

export const fpgaAcquired = () => ({
  type: FPGA_ACQUIRED
});

export const fpgaReleased = () => ({
  type: FPGA_RELEASED
});

export default (state=init, action) => {
  const switches = Array(...state.switches);
  const buttons = Array(...state.buttons);
  switch (action.type) {
  case OPEN_SWITCH:
  case CLOSE_SWITCH:
    switches[action.id] = SW_WAIT;
    return {
      ...state,
      switches
    };
  case OPEN_SWITCH_SUCC:
  case CLOSE_SWITCH_FAIL:
    switches[action.id] = SW_ON;
    return {
      ...state,
      switches
    };
  case OPEN_SWITCH_FAIL:
  case CLOSE_SWITCH_SUCC:
    switches[action.id] = SW_OFF;
    return {
      ...state,
      switches
    };
  case PRESS_BTN:
  case RELEASE_BTN:
    buttons[action.id] = BTN_WAIT;
    return {
      ...state,
      buttons
    };
  case RELEASE_BTN_FAIL:
  case PRESS_BTN_SUCC:
    buttons[action.id] = BTN_DOWN;
    return {
      ...state,
      buttons
    };
  case PRESS_BTN_FAIL:
  case RELEASE_BTN_SUCC:
    buttons[action.id] = BTN_UP;
    return {
      ...state,
      buttons
    };
  case TOGGLE_SETTING:
    return {
      ...state,
      setting: !state.setting 
    };
  case FPGA_ACQUIRED:
    return {
      ...state,
      occupied: true
    };
  case FPGA_RELEASED:
    return {
      ...state,
      occupied: false
    }
  default:
    return state;
  }
};
