import React from 'react';
import ReactDOM from 'react-dom';
import base from '../css/base.scss';
import {Header} from '../baseComp/Header.jsx';


export class App extends React.Component {
    render() {
        return (
          <div className= "main" >
            < Header />
          </div>

        )
    }
}

const rootElement = document.getElementById('header');
ReactDOM.render(<App/>, rootElement);