import React from 'react';

import { Table } from '../tables/Table.jsx';
import TableList from '../tables/TableList.jsx';
import Notes from '../info/Notes.jsx';
import StatusInfo from '../info/StatusInfo.jsx';
import TopBar from './TopBar.jsx';

export class RightSide extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            pageID: this.props.profile.pageID,
            profileHeaders: this.props.profile.profileHeaders,
            profileData: this.props.profile.profilevalues,
            tableHeaders: this.props.profile.secondTableHeaders,
            tableData: this.props.profile.secondTableData,
            infobtn: ['edit']
        };
    }
    render() {
        let moduleExtra = renderConstructor(this.state);
        let statusTitle=this.state.pageID=='jobs'?'Job status':this.state.pageID=='technicians'?'Technician status' :'';
        return (
            <div className="selected-details center-block" >
                <div className="profile col-md-12 center-block">
                    <TableList headers={this.state.profileHeaders} data={this.state.profileData} page ={this.state.pageID}/>
                </div>
                <div className="col-md-12 profile center-block border-top">
                    <Notes title='Additional information' info={this.state.profileData.additionalInfo} buttons={this.state.infobtn} icon='sbn-icon-edit' />
                    <StatusInfo title={statusTitle} info={this.state.profileData} page ={this.state.pageID} />
                </div>
                {moduleExtra}
            </div>
        )
    }
};

function renderConstructor(t) {
    switch (t.pageID) {
        case 'technicians':
            return (
                <div className="col-md-12 profile-table border-top">
                    <h4>Job History</h4>
                    <TopBar btnExtra={false} />
                    <Table headers={t.tableHeaders} pageSize={5} data={t.tableData} />
                </div>
            )
        case 'jobs':
            return (
                <div className="col-md-12 profile-table border-top">
                    <h4>Client Feedback</h4>
                    
                </div>
            )
        // case 'error':
        //     return <Error text={text} />;
        default:
            return null;
    }
}
