'use strict'
import React from 'react';
import { connect } from 'react-redux';

@connect(
  (state) => ({
    occupied: state.occupied
  })
)
class Upload extends React.Component {

  state = {
    file: null
  };

  handleChange = (e) => {
    this.setState({file: e.target.files[0]});
  };

  handleUpload = () => {
    const formData = new FormData();
    formData.append('file', $('#input_file')[0].files[0]);
    formData.append('filetype', 'bit');
    const req = new XMLHttpRequest();
    req.open('post', `file`);
    req.send(formData);
  };

  render() {
    const color = this.props.occupied ? '#fff' : '#777';
    return (
      <div>
        <p style={{color: color }}>Bit file</p>
        <div id="bitfile_contain">
          <ul id="about_file">
            <li id="path_for_file" style={{borderColor: color}}>
              {(this.state.file && this.state.file.name) || null}
            </li>
            <li id="file_input" style={{backgroundColor: color, borderColor: color}}>
              <input type="file" 
                     id="input_file" 
                     onChange={this.handleChange} />···
            </li>
          </ul>
          <ul id="about_button">
            <li id="upload" className="click_button" onClick={this.handleUpload}
                style={{
                  backgroundColor: color,
                  borderColor: color
                }}>UPLOAD</li>
            <li id="program" className="click_button"
                style={{
                  backgroundColor: color,
                  borderColor: color
                }}>PROGRAM</li>
          </ul>
        </div>
      </div>
    );
  }
}

export default Upload;
