import React from 'react';
import ReactDOM from 'react-dom';
import base from '../css/base.scss';

import BlockHeader from '../components/BlockHeader.jsx';
import Table from '../components/Table.jsx';


//var dashboard_sock = 'ws://' + window.location.host + "/technicians/"

export class Technicians extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tableHeaders:['Name','Phone Number','Location','Jobs','Status']
        };

    }
    render() {
        return (
            <div className="technicians col-md-12 center-block" >
                <div className="col-md-6  center-block">
                    <BlockHeader title='Technicians List' />
                    <Table headers={this.state.tableHeaders} />

                </div>
                <div className="col-md-6  center-block">
                    <BlockHeader title='Technician Profile' />
                </div>

            </div>
        )
    }
}
const rootElement = document.getElementById('technicians');
ReactDOM.render(<Technicians />, rootElement);