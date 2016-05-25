'use strict'
import { createStore } from 'redux';
import reducer from './redux';

export default createStore(reducer, undefined, 
  window.devToolsExtension && window.devToolsExtension());
