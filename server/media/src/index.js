'use strict'
import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { Router, Route, IndexRoute, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';

import store from './store';

import LoginPage from './components/LoginPage';
import DevicePage from './components/DevicePage';

const history = syncHistoryWithStore(browserHistory, store);

const routes = (
  <Provider store={store}>
    <Router history={history}>
      <Route path="/" >
        <IndexRoute component={LoginPage} />
        <Route path="/device/:id" component={DevicePage} />
      </Route>
    </Router>
  </Provider>
);

ReactDOM.render(
  routes,
  document.getElementById('react-root')
);
