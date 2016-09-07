'use strict';
import React from 'react';
import { connect } from 'react-redux';
import {
  FormGroup, FormControl, HelpBlock, ControlLabel, SplitButton, MenuItem,
  InputGroup
} from 'react-bootstrap';
import QueueAnim from 'rc-queue-anim';
import is from 'is_js';

import style from './style';

import { changeForm, changePassword } from '../../redux/account';

const regex = /(?=.*\d)(?=.*[a-zA-Z])[\da-zA-Z]{8,20}/;

@connect(
  (state) => ({
    formState: state.account.formState,
    changing: state.account.changing,
    change_msg: state.account.change_msg
  }),
  { changeForm, changePassword }
)
class ChangePasswordForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      fields: {
        email: { touched: false, value: '', error: '此项为必填项。' },
        oldpass: { touched: false, value: '', error: '此项为必填项。' },
        newpass: { touched: false, value: '', error: '此项为必填项。' }
      }
    };
  }

  validate(key, val) {
    switch(key) {
      case 'email':
        return !val           ? '此项为必填项。' :
               !is.email(val) ? '邮箱地址不合法。' :
                                '';
      case 'newpass':
        return !val             ? '此项为必填项。' : 
               !regex.test(val) ? '密码长度可为8至20位，其中必须包含数字和字母组合。' :
                                  '';
      case 'oldpass':
        return !val ? '此项为必填项。' :
                      '';
    }
  }

  handleChangeClick() {
    const { email, oldpass, newpass } = this.state.fields;
    if (email.error || oldpass.error || newpass.error || this.props.changing)
      return;
    this.props.changePassword(email.value, oldpass.value, newpass.value);
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
    const { email, oldpass, newpass } = this.state.fields;
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
          <FormGroup controlId="formBasicText" key="input-old">
            <InputGroup>
              <InputGroup.Addon><i className="fa fa-unlock fa-fw" aria-hidden="true"/></InputGroup.Addon>
              <FormControl type="password" placeholder="请输入旧登录密码"
                           onChange={this.handleChange.bind(this, 'oldpass')} onBlur={this.handleBlur.bind(this, 'oldpass')}/>
            </InputGroup>
            <HelpBlock>{(oldpass.touched && oldpass.error) || '　'}</HelpBlock>
          </FormGroup>,
          <FormGroup controlId="formBasicText" key="input-new">
            <InputGroup>
              <InputGroup.Addon><i className="fa fa-lock fa-fw" aria-hidden="true"/></InputGroup.Addon>
              <FormControl type="password" placeholder="请输入新登录密码"
                           onChange={this.handleChange.bind(this, 'newpass')} onBlur={this.handleBlur.bind(this, 'newpass')}/> 
            </InputGroup>
            <HelpBlock>{(newpass.touched && newpass.error) || '　'}</HelpBlock>
          </FormGroup>,
          <div className={style.container} key="input-btn">
            <div className={style.error} key="input-error">{this.props.change_msg || '　'}</div>
            <SplitButton className={style.button} bsStyle="default" id="btn" onSelect={this.props.changeForm}
                         title={<span>修改密码{this.props.changing && <i className="fa fa-spinner fa-spin fa-fw" />}</span>}
                         onClick={this.handleChangeClick.bind(this)}>
              <MenuItem eventKey="login">登录</MenuItem>
              <MenuItem eventKey="register">注册</MenuItem>
              <MenuItem divider />
              <MenuItem eventKey="find">找回密码</MenuItem>
            </SplitButton>
          </div>
        ]}
        </QueueAnim>
      </form>
    );
  }
}

export default ChangePasswordForm;
