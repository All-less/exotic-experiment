'use strict'
import React from 'react';

class Upload extends React.Component {

  handleChange(e) {
    console.log(e.target.files[0]);
  }

  render() {
    return (
      <div>
        <p>Bit file</p>
        <div id="bitfile_contain">
          <ul id="about_file">
            <li id="path_for_file"></li>
            <li id="file_input" >
              <input type="file" 
                     id="input_file" 
                     className="click_button" 
                     onChange={this.handleChange}/>···
            </li>
          </ul>
          <ul id="about_button">
            <li id="upload" className="click_button">UPLOAD</li>
            <li id="program" className="click_button">PROGRAM</li>
          </ul>
        </div>
      </div>
    );
  }
}

export default Upload;
