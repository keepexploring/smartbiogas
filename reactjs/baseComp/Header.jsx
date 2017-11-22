import React from 'react';
import {Logo} from './Logo.jsx'

export class Header extends React.Component {
    render() {
        return (
          <div className= "head-nav navbar-fixed-top" >
            <h1>Hello Django - hest changes</h1>
            <Logo />
          </div>

        )
    }
}
