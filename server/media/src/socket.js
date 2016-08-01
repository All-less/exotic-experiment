import store from './store';
import {
  openSwitch,
  openSwitchSucc,
  openSwitchFail,
  closeSwitch,
  closeSwitchSucc,
  closeSwitchFail,
  pressButton,
  pressButtonSucc,
  pressButtonFail,
  releaseButton,
  releaseButtonSucc,
  releaseButtonFail,
  fpgaAcquired,
  fpgaReleased
} from './redux';

const TYPE_ACTION = 0;
const TYPE_STATUS = 1;
const TPYE_OPERATION = 2;
const TYPE_INFO = 3;
const switchTimeout = Array(4).fill(undefined);
const buttonTimeout = Array(4).fill(undefined);

/*
const socket = new WebSocket(`ws://${location.host}/socket${location.pathname}`);
*/
const socket = {};

/* The last sent comment. Store it in order to filter broadcast from the server. */
let lastComment;

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  switch (data.type) {
  case TYPE_STATUS:
    switch (data.status) {
    case 'switch_on':
      store.dispatch(openSwitchSucc(data.id));
      clearTimeout(switchTimeout[data.id])
      break;
    case 'switch_off':
      store.dispatch(closeSwitchSucc(data.id));
      clearTimeout(switchTimeout[data.id]);
      break;
    case 'button_pressed':
      store.dispatch(pressButtonSucc(data.id));
      clearTimeout(buttonTimeout[data.id]);
      break;
    case 'button_released':
      store.dispatch(releaseButtonSucc(data.id));
      clearTimeout(buttonTimeout[data.id]);
      break;
    }
  case TYPE_INFO:
    switch (data.info) {
    case 'user_changed':
      if (data.user === config.nickname) {
        store.dispatch(fpgaAcquired());
      } else if (data.user === null) {
        store.dispatch(fpgaReleased())
      }
      break;
    case 'broadcast':
      if (data.content !== lastComment)
        $("#danmu").danmu("addDanmu", {
          text: data.content,
          color: "white", 
          size: 1, 
          position: 0, 
          time: $('#danmu').data("nowTime")+10
        });
    }
  }
};

const send = (obj) => {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(obj));
  } else {
    console.error('Attempted to send data while socket is not opened.');
  }
};

const remote = {
  openSwitch: (id) => {
    socket.send(JSON.stringify({type: 0, action: 'acquire'}));
    send({
      type: TPYE_OPERATION, 
      operation: 2,
      id
    });
    store.dispatch(openSwitch(id));
    switchTimeout[id] = setTimeout(
      () => {store.dispatch(openSwitchFail(id))}, 30000
    );
  },
  closeSwitch: (id) => {
    send({
      type: TPYE_OPERATION,
      operation: 3,
      id
    });
    store.dispatch(closeSwitch(id));
    switchTimeout[id] = setTimeout(
      () => {store.dispatch(closeSwitchFail(id))}, 30000
    );
  },
  pressButton: (id) => {
    send({
      type: TPYE_OPERATION,
      operation: 4,
      id
    });
    store.dispatch(pressButton(id));
    buttonTimeout[id] = setTimeout(
      () => {store.dispatch(pressButtonFail(id))}, 30000
    );
  },
  releaseButton: (id) => {
    send({
      type: TPYE_OPERATION,
      operation: 5,
      id
    });
    store.dispatch(releaseButton(id));
    buttonTimeout[id] = setTimeout(
      () => {store.dispatch(releaseButtonFail(id))}, 30000
    );
  },
  broadcast: (content) => {
    lastComment = content;
    send({
      type: TYPE_ACTION,
      action: 'broadcast',
      content
    });
  },
  acquire: () => {
    send({
      type: TYPE_ACTION,
      action: 'acquire'
    });
  },
  release: () => {
    send({
      type: TYPE_ACTION,
      action: 'release'
    });
  }
};

export default remote;
