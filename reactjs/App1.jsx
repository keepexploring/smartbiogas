 import React from "react"
 import { render } from "react-dom"
 //var ReactDOM = require('react-dom');
//import React from 'react';
//import ReactDOM from 'react-dom';

class App1 extends React.Component {
  render() {
    return <h1>Hello how are you </h1>;

  }
}

render(<App1/>, document.getElementById('App1'))
