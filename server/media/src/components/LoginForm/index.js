'use strict';
import React from 'react';
import {
  FormGroup, FormControl, HelpBlock, ControlLabel, SplitButton, MenuItem,
  InputGroup
} from 'react-bootstrap';
import { connect } from 'react-redux';
import QueueAnim from 'rc-queue-anim';
import is from 'is_js';

import style from './style';

import { changeForm, login } from '../../redux/account';

@connect(
  (state) => ({
    formState: state.account.formState,
    loggingIn: state.account.loggingIn,
    login_msg: state.account.login_msg
  }),
  { changeForm, login }
)
class LoginForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      fields: {
        email: { touched: false, value: '', error: '此项为必填项。' },
        password: { touched: false, value: '', error: '此项为必填项。' }
      }
    };
  }

  handleLoginClick() {
    const { email, password } = this.state.fields;
    if (email.error || password.error || this.props.loggingIn)
      return;
    this.props.login(email.value, password.value);
  }

  validate(key, val) {
    switch(key) {
      case 'email':
        return !val           ? '此项为必填项。' :
               !is.email(val) ? '邮箱地址不合法。' :
                                '';
      case 'password':
        return !val ? '此项为必填项。' : 
                      '';
    }
  }

  handleChange(key, event) {
    let fields = this.state.fields;
    let val = event.target.value;
    fields[key].value = val;
    fields[key].error = this.validate(key, val)
    this.setState({ fields });
  }

  handleBlur(field) {
    let fields = this.state.fields;
    fields[field].touched = true;
    this.setState({ fields });
  }

  render() {
    const { email, password } = this.state.fields;
    return (
      <form>
        <QueueAnim duration={1000}>
        {[
          <FormGroup controlId="formBasicText" key="input-mail">
            <InputGroup>
              <InputGroup.Addon><i className="fa fa-envelope-o fa-fw" aria-hidden="true"/></InputGroup.Addon>
              <FormControl type="text" placeholder="请输入邮箱地址"
                           onChange={this.handleChange.bind(this, 'email')} onBlur={this.handleBlur.bind(this, 'email')}/>
            </InputGroup>
            <HelpBlock>{(email.touched && email.error) || '　'}</HelpBlock>
          </FormGroup>,
          <FormGroup controlId="formBasicText" key="input-pass">
            <InputGroup>
              <InputGroup.Addon><i className="fa fa-lock fa-fw" aria-hidden="true"/></InputGroup.Addon>
              <FormControl type="password" placeholder="请输入登录密码"
                           onChange={this.handleChange.bind(this, 'password')} onBlur={this.handleBlur.bind(this, 'password')}/> 
            </InputGroup>
            <HelpBlock>{(password.touched && password.error) || '　'}</HelpBlock>
          </FormGroup>,
          <div className={style.container} key="input-btn">
            <div className={style.error} key="input-error">{this.props.login_msg || '　'}</div>
            <SplitButton className={style.button} bsStyle="default" id="btn" onSelect={this.props.changeForm}
                         title={<span>登录{this.props.loggingIn && <i className="fa fa-spinner fa-spin fa-fw" />}</span>}
                         onClick={this.handleLoginClick.bind(this)}>
              <MenuItem eventKey="register">注册</MenuItem>
              <MenuItem divider />
              <MenuItem eventKey="find">找回密码</MenuItem>
              <MenuItem eventKey="reset">修改密码</MenuItem>
            </SplitButton>  
          </div>
        ]}
        </QueueAnim>
      </form>
    );
  }
}

export default LoginForm;
