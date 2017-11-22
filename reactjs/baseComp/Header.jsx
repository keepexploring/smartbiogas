import React from 'react';
import {Logo} from './Logo.jsx'
import {NavSecond} from './NavSecond.jsx'
import {Navigation} from './Navigation.jsx'

export class Header extends React.Component {
    render() {
        return (
          <div className= "head-nav navbar-fixed-top" >
            <Logo />
            <NavSecond />
            <Navigation />
          </div>

        )
    }
}
