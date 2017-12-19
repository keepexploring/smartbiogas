import React from 'react';

import Table from '../tables/Table.jsx';
import TableList from '../tables/TableList.jsx';
import Notes from '../info/Notes.jsx';
import StatusInfo from '../info/StatusInfo.jsx';
import TopBar from './TopBar.jsx';

export class RightSide extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            profileHeaders: this.props.profile.profileHeaders,
            profileData: this.props.profile.profilevalues,
            tableHeaders: this.props.profile.secondTableHeaders,
            tableData: this.props.profile.secondTableData,
            infobtn: ['edit']
        };
    }
    render() {
        return (
            <div className="techprofile center-block" >
                <div className="profile row center-block">
                    <TableList headers={this.state.profileHeaders} data={this.state.profileData} />
                </div>
                <div className="row profile center-block border-top">
                    <Notes title='Additional information' info={this.state.profileData.additionalInfo} buttons={this.state.infobtn} icon='sbn-icon-edit' />
                    <StatusInfo title='' info={this.state.profileData} />
                </div>
                <div className="row profile-table border-top">
                    <h4>Job History</h4>
                    <TopBar btnExtra={false} />
                    <Table headers={this.state.tableHeaders} pageSize={5} data={this.state.tableData} />
                </div>
            </div>
        )
    }
}
