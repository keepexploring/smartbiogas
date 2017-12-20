import React from 'react';

import Table from '../tables/Table.jsx';
import TopBar from './TopBar.jsx';


export class LeftSide extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          tableHeaders:this.props.data.tableHeaders,
          tableValues:this.props.data.tableValues
        };
    }
    render() {
        return (
            <div className="main-table col-md-12 center-block" >
                <TopBar btnExtra={true} />
                <Table headers={this.state.tableHeaders} pageSize={10} data={this.state.tableValues} />
            </div>
        )
    }
}
