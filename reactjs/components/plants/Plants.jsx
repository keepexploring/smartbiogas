import React from 'react';

export default class Plants extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
        console.log('loaded plants');
    }

    render() {
        return (
            <h1>Plants</h1>
        )
    }
}
