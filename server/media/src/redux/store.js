'use strict'
import { createStore, applyMiddleware, compose } from 'redux';
import { browserHistory } from 'react-router';
import { routerMiddleware } from 'react-router-redux';
import { combineReducers } from 'redux';
import { routerReducer as routing } from 'react-router-redux';

import device from './device';
import account from './account';

import qwest from 'qwest';

const ajax = {
  get: async function ajax$get(url, params = {}, options = {}) {
    options.responseType = options.responseType || 'text';
    params.timestamp = params.timestamp || Date.now();
    let res;
    try {
      const xhr = await qwest.get(url, params, options);
      res = JSON.parse(xhr.response);
    } catch (err) {
      throw err;
    }
    if (res.code !== 0) {
      throw res.error;
    }
    return res.data;
  },
  post: async function ajax$post(url, params = {}, options = {}) {
    options.dataType = options.dataType || 'json';
    options.responseType = options.responseType || 'text';
    let res;
    try {
      const xhr = await qwest.post(url, params, options);
      res = JSON.parse(xhr.response);
    } catch (err) {
      throw err;
    }
    if (res.code !== 0) {
      throw res.error;
    }
    return res.data;
  }
};

function ajaxMiddleware(client) {
  return ({dispatch, getState}) => {
    return next => action => {
      if (typeof action === 'function') {
        return action(dispatch, getState);
      }
      const { promise, types, ...rest } = action;
      if (!promise) {
        return next(action);
      }
      const [REQUEST, SUCCESS, FAILURE] = types;
      next({...rest, type: REQUEST});
      const actionPromise = promise(client);
      actionPromise.then(
        (result) => next({...rest, result, type: SUCCESS}),
        (error) => next({...rest, error, type: FAILURE})
      ).catch((error) => {
        console.error('MIDDLEWARE ERROR:', error);
        next({...rest, error, type: FAILURE});
      });
      return actionPromise;
    };
  };
}

const _ajaxMiddleware = ajaxMiddleware(ajax);
const _routerMiddleware = routerMiddleware(browserHistory);

export default createStore(combineReducers({account, device, routing}), compose(
    applyMiddleware(_ajaxMiddleware, _routerMiddleware),
    window.devToolsExtension && window.devToolsExtension()
  )
);
