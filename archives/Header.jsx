import React from 'react';
import ReactDOM from 'react-dom';

// import base from '../css/base.scss';
// import {Logo} from '../baseComp/Logo.jsx'
// import {Navigation} from '../baseComp/Navigation.jsx'

export class Header extends React.Component {
    render() {
        return (
          <div className= "head-nav navbar-fixed-top" >
            <Logo />
            <Navigation />
          </div>

        )
    }
}
// const rootElement = document.getElementById('header');
// ReactDOM.render(<Header/>, rootElement);
