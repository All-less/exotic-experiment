'use strict'
import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { Router, Route, IndexRoute, browserHistory } from 'react-router';
import { ReduxAsyncConnect } from 'redux-connect';
import { syncHistoryWithStore } from 'react-router-redux';

import store from './redux/store';

import App from './components/App';
import IndexPage from './components/IndexPage';
import DevicePage from './components/DevicePage';

const history = syncHistoryWithStore(browserHistory, store);

const routes = (
  <Provider store={store}>
    <Router history={history}
            render={(props) => (<ReduxAsyncConnect {...props}/>)} >
      <Route path="/" component={App} >
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
