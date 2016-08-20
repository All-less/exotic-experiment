import store from './store';
import { push } from 'react-router-redux';

import { updateDevices } from './device';

const CHANGE_FORM = 'Exotic/account/CHANGE_FORM';
const VERIFY_EMAIL = 'Exotic/account/VERIFY_EMAIL';
const VERIFY_EMAIL_SUCC = 'Exotic/account/VERIFY_EMAIL_SUCC';
const VERIFY_EMAIL_FAIL = 'Exotic/account/VERIFY_EMAIL_FAIL';
const VCODE_COUNTDOWN = 'Exotic/account/VCODE_COUNTDOWN';
const REGISTER = 'Exotic/account/REGISTER';
const REGISTER_SUCC = 'Exotic/account/REGISTER_SUCC';
const REGISTER_FAIL = 'Exotic/account/REGISTER_FAIL';
const LOGIN = 'Exotic/account/LOGIN';
const LOGIN_SUCC = 'Exotic/account/LOGIN_SUCC';
const LOGIN_FAIL = 'Exotic/account/LOGIN_FAIL';
const FIND = 'Exotic/account/FIND';
const FIND_SUCC = 'Exotic/account/FIND_SUCC';
const FIND_FAIL = 'Exotic/account/FIND_FAIL';
const CHANGE = 'Exotic/account/CHANGE';
const CHANGE_SUCC = 'Exotic/account/CHANGE_SUCC';
const CHANGE_FAIL = 'Exotic/account/CHANGE_FAIL';
const LOAD_STATUS = 'Exotic/account/LOAD_STATUS';
const LOAD_STATUS_SUCC = 'Exotic/account/LOAD_STATUS_SUCC';
const LOAD_STATUS_FAIL = 'Exotic/account/LOAD_STATUS_FAIL';
const LOGOUT = 'Exotic/account/LOGOUT';
const LOGOUT_SUCC = 'Exotic/account/LOGOUT_SUCC';
const LOGOUT_FAIL = 'Exotic/account/LOGOUT_FAIL';

const init = {
  formState: 'login',
  vcode_count: 0
};

export const changeForm = (formState) => ({
  type: CHANGE_FORM,
  formState
});

export const verifyEmail = (email) => ({
  types: [VERIFY_EMAIL, VERIFY_EMAIL_SUCC, VERIFY_EMAIL_FAIL],
  promise: (client) => client.post('/api/verify', { email })
});

export const vcodeCountdown = () => ({
  type: VCODE_COUNTDOWN
});

export const register = (email, password) => ({
  types: [REGISTER, REGISTER_SUCC, REGISTER_FAIL],
  promise: (client) => client.post('/api/register', { email, password })
});

export const login = (email, password) => ({
  types: [LOGIN, LOGIN_SUCC, LOGIN_FAIL],
  promise: (client) => client.post('/api/login', { email, password })
});

export const findPassword = (email) => ({
  types: [FIND, FIND_SUCC, FIND_FAIL],
  promise: (client) => client.post('/api/find', { email })
});

export const changePassword = (email, oldpass, newpass) => ({
  types: [CHANGE, CHANGE_SUCC, CHANGE_FAIL],
  promise: (client) => client.post('/api/change', { email, oldpass, newpass })
});

export const loadStatus = () => ({
  types: [LOAD_STATUS, LOAD_STATUS_SUCC, LOAD_STATUS_FAIL],
  promise: (client) => client.get('/api/status')
});

export const logout = () => ({
  types: [LOGOUT, LOGOUT_SUCC, LOGOUT_FAIL],
  promise: (client) => client.post('/api/logout')
});

export default (state=init, action) => {
  switch (action.type) {
    case CHANGE_FORM:
      return {
        ...state,
        formState: action.formState, 
        vcode_msg: null,
        reg_msg: null,
        change_msg: null,
        find_msg: null,
        login_msg: null
      };
    case VERIFY_EMAIL:
      return {
        ...state,
        vcode_sending: true,
        vcode_msg: null
      };
    case VERIFY_EMAIL_SUCC:
      setTimeout(() => { store.dispatch(vcodeCountdown()); }, 1000);
      return {
        ...state,
        vcode_sending: false,
        vcode: action.result.code,
        vcode_sent: true,
        vcode_count: 60,
        vcode_msg: null
      };
    case VERIFY_EMAIL_FAIL:
      return {
        ...state,
        vcode_sending: false,
        vcode_msg: '获取验证码失败，请重试。'
      };
    case VCODE_COUNTDOWN:
      if (state.vcode_count !== 0) {
        setTimeout(() => { store.dispatch(vcodeCountdown()); }, 1000);
        return {
          ...state,
          vcode_count: state.vcode_count - 1
        };
      } else {
        return {
          ...state,
          vcode_sent: false,
          vcode_msg: null
        };
      }
    case REGISTER:
      return {
        ...state,
        registering: true,
        reg_msg: ''
      };
    case REGISTER_SUCC:
      setTimeout(() => {
        store.dispatch({...action, type: LOAD_STATUS_SUCC });
      }, 0);
      if (action.result.status.devices.length === 0) {
        return {
          ...state,
          registering: false,
          reg_msg: '当前无可用设备。'
        };
      } else {
        return {
          ...state,
          registering: false
        };
      }
    case REGISTER_FAIL:
      return {
        ...state,
        registering: false,
        reg_msg: action.error.err === 'DUPLICATE_EMAIL' ? '该邮箱已被注册。' : '出现未知错误。'
      };
    case LOGIN:
      return {
        ...state, 
        loggingIn: true,
        login_msg: null
      };
    case LOGIN_SUCC:
      setTimeout(() => {
        store.dispatch({...action, type: LOAD_STATUS_SUCC });
      }, 0);
      if (action.result.status.devices.length === 0) {
        return {
          ...state,
          loggingIn: false,
          login_msg: '当前无可用设备。'
        };
      } else {
        return {
          ...state,
          loggingIn: false
        };
      }
    case LOGIN_FAIL:
      return {
        ...state,
        loggingIn: false,
        login_msg: action.error.err === 'NO_USER'        ? '该邮箱未注册。' :
                   action.error.err === 'WRONG_PASSWORD' ? '登录密码错误。' :
                                                           '出现未知错误。'
      }
    case CHANGE:
      return {
        ...state,
        changing: true,
        change_msg: null
      };
    case CHANGE_SUCC:
      return {
        ...state,
        changing: false,
        change_msg: '密码修改成功。'
      };
    case CHANGE_FAIL:
      return {
        ...state,
        changing: false,
        change_msg: action.error.err === 'NO_USER'        ? '该邮箱未注册。' :
                    action.error.err === 'WRONG_PASSWORD' ? '登录密码错误。' :
                                                            '出现未知错误。'
      };
    case FIND:
      return {
        ...state,
        finding: true,
        find_msg: null
      };
    case FIND_SUCC:
      return {
        ...state,
        finding: false,
        find_msg: '重置后密码已发送至邮箱。'
      };
    case FIND_FAIL:
      return {
        ...state,
        finding: false,
        find_msg: action.error.err === 'NO_USER'  ? '该邮箱未注册。' : 
                  action.error.err === 'SMTP_ERR' ? '密码重置邮件发送失败。' :
                                                    '出现未知错误。'
      }
    case LOAD_STATUS_SUCC:
      console.log(action.result);
      setTimeout(() => {
        store.dispatch(updateDevices(action.result.status.devices));
      }, 0);
      if (action.result.status.devices.length > 0 &&
          !location.pathname.startsWith('/device')) {
        setTimeout(() => {
          const len = action.result.status.devices.length;
          const index = Math.floor(Math.random() * len);
          store.dispatch(push(`device/${action.result.status.devices[index]}`));
        }, 0);
      }
      return state;
    case LOAD_STATUS_FAIL:
    case LOGOUT_SUCC:
      if (location.pathname !== '/') {
        setTimeout(() => { store.dispatch(push('/')); }, 0);
      }
      return state;
    case LOGOUT_FAIL:
      // TODO
    default:
      return state;
  }
};
