import React from 'react';


export class Plants extends React.Component {
    render() {
        return (
            <div className="plants col-md-12 center-block" id="plants"> 

            </div>
        )
    }
}
const rootElement = document.getElementById('react-app');
ReactDOM.render(<Plants/>, rootElement);