'use strict';
import React from 'react';
import { connect } from 'react-redux';
import {
  FormGroup, FormControl, HelpBlock, ControlLabel, SplitButton, MenuItem,
  InputGroup
} from 'react-bootstrap';
import QueueAnim from 'rc-queue-anim';

import style from './style';

import { changeForm } from '../../redux/account';

@connect(
  (state) => ({
    formState: state.account.formState
  }),
  { changeForm }
)
class FindPasswordForm extends React.Component {
  render() {
    return (
      <form>
        <QueueAnim duration={1000}>
        {[
          <FormGroup controlId="formBasicText" key="input-mail">
            <InputGroup>
              <InputGroup.Addon><i className="fa fa-envelope-o fa-fw" aria-hidden="true"/></InputGroup.Addon>
              <FormControl type="text" placeholder="请输入邮箱地址"/>
            </InputGroup>
            <HelpBlock>　</HelpBlock>
          </FormGroup>,
          <FormGroup controlId="formBasicText" key="input-code">
            <InputGroup>
              <InputGroup.Addon><i className="fa fa-key fa-fw" aria-hidden="true"/></InputGroup.Addon>
              <FormControl type="text"placeholder="请输入验证码"/> 
            </InputGroup>
            <HelpBlock>　</HelpBlock>
          </FormGroup>,
          <div className={style.container} key="input-btn">
            <SplitButton className={style.button} bsStyle="default" title="找回密码" id="btn" onSelect={this.props.changeForm}>
              <MenuItem eventKey="login">登录</MenuItem>
              <MenuItem eventKey="register">注册</MenuItem>
              <MenuItem divider />
              <MenuItem eventKey="reset">修改密码</MenuItem>
            </SplitButton>
          </div>
        ]}
        </QueueAnim>
      </form>
    );
  }
}

export default FindPasswordForm;
