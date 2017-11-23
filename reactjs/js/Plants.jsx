import React from 'react';


export class Plants extends React.Component {
    render() {
        return (
            <h1>Hello plants</h1>

        )
    }
}
const rootElement = document.getElementById('react-app');
ReactDOM.render(<Plants/>, rootElement);