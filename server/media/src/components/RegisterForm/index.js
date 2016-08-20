'use strict';
import React from 'react';
import { connect } from 'react-redux';
import {
  FormGroup, FormControl, HelpBlock, ControlLabel, SplitButton, MenuItem,
  InputGroup, Button
} from 'react-bootstrap';
import QueueAnim from 'rc-queue-anim';
import is from 'is_js';

import style from './style';

import { changeForm, verifyEmail, register } from '../../redux/account';

const regex = /(?=.*\d)(?=.*[a-zA-Z])[\da-zA-Z]{8,20}/;

@connect(
  (state) => ({
    formState: state.account.formState,
    vcode_sending: state.account.vcode_sending,
    vcode_sent: state.account.vcode_sent,
    vcode: state.account.vcode,
    vcode_msg: state.account.vcode_msg,
    vcode_count: state.account.vcode_count,
    registering: state.account.registering,
    reg_msg: state.account.reg_msg
  }),
  { 
    changeForm, verifyEmail, register
  }
)
class RegisterForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      fields: {
        email: { touched: false, value: '', error: '此项为必填项。' },
        password: { touched: false, value: '', error: '此项为必填项。' },
        vcode: { touched: false, value: '', error: '此项为必填项。' }
      }
    };
  }

  handleRegisterClick() {
    const { email, password, vcode } = this.state.fields;
    if (email.error || password.error || vcode.error || this.props.vcode_msg || this.props.registering)
      return;
    this.props.register(email.value, password.value);
  }

  handleVcodeClick() {
    this.props.verifyEmail(this.state.fields.email.value);
  }

  validate(key, val) {
    switch(key) {
      case 'email':
        return !val           ? '此项为必填项。' :
               !is.email(val) ? '邮箱地址不合法。' :
                                '';
      case 'password':
        return !val             ? '此项为必填项。' : 
               !regex.test(val) ? '密码长度可为8至20位，其中必须包含数字和字母组合。' :
                                  '';
      case 'vcode':
        return val !== this.props.vcode ? '验证码输入有误。' :
               !val                     ? '此项为必填项。' :
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
    const { email, password, vcode } = this.state.fields;
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
          <FormGroup controlId="formBasicText" key="input-vcode">
            <InputGroup>
              <InputGroup.Addon><i className="fa fa-key fa-fw" aria-hidden="true"/></InputGroup.Addon>
              <FormControl type="text" placeholder="请输入验证码" 
                           onChange={this.handleChange.bind(this, 'vcode')} onBlur={this.handleBlur.bind(this, 'vcode')}/> 
              <InputGroup.Button>
                <Button onClick={this.handleVcodeClick.bind(this)} disabled={this.props.vcode_sent || !!email.error}>
                  {this.props.vcode_sent ?  this.props.vcode_count + '秒后重新获取' : '获取验证码'} 
                  {this.props.vcode_sending && <i className="fa fa-spinner fa-pulse fa-fw" />}
                </Button>
              </InputGroup.Button>
            </InputGroup>
            <HelpBlock>{this.props.vcode_msg || (vcode.touched && vcode.error) || '　'}</HelpBlock>
          </FormGroup>,
          <div className={style.container} key="input-btn">
            <div className={style.error} key="input-error">{this.props.reg_msg || '　'}</div>
            <SplitButton className={style.button} bsStyle="default" id="btn" onSelect={this.props.changeForm}
                         title={<span>注册{this.props.registering && <i className="fa fa-spinner fa-spin fa-fw" />}</span>}
                         onClick={this.handleRegisterClick.bind(this)}>
              <MenuItem eventKey="login">登录</MenuItem>
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

export default RegisterForm;
