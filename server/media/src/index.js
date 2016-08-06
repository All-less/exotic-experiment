'use strict'
import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { Router, Route, IndexRoute, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';

import store from './redux/store';

import IndexPage from './components/IndexPage';
import DevicePage from './components/DevicePage';

const history = syncHistoryWithStore(browserHistory, store);

const routes = (
  <Provider store={store}>
    <Router history={history}>
      <Route path="/" >
        <IndexRoute component={IndexPage} />
        <Route path="/device/:id" component={DevicePage} />
      </Route>
    </Router>
  </Provider>
);

ReactDOM.render(
  routes,
  document.getElementById('react-root')
);
