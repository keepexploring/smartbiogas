import React from 'react';


export class Technicians extends React.Component {
    render() {
        return (
            <div className="technicians col-md-12 center-block" id="technicians"> 
                Hello
            </div>
        )
    }
}
const rootElement = document.getElementById('dashboard');
ReactDOM.render(<Technicians/>, rootElement);