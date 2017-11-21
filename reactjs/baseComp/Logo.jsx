import React from 'react';
import {logoimg} from '../images/logo_150.png ';

export class Logo extends React.Component {
    render() {
        return (
          <div class="logo">
          <a class="img_icon" href="#">
            <img src={logoimg} alt="."/>
          </a>
      </div>

        )
    }
}
