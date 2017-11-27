import React from 'react';
import ReactDOM from 'react-dom';

import base from '../css/base.scss';
export class Dashboard extends React.Component {
    render() {
        return (
          <div className= "main top-margin" >
            test
          </div>

        )
    }
}

const rootElement = document.getElementById('dashboard');
ReactDOM.render(<Dashboard/>, document.getElementById('dashboard'));
