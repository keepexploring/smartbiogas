import React from 'react';

import Table from '../components/tables/Table.jsx';
import TableList from '../components/tables/TableList.jsx';
import Notes from './info/Notes.jsx';
import StatusInfo from './info/StatusInfo.jsx';

//import { makeData, newProfile } from "../components/TableUtilities.jsx"; //Test data constructor


// const datafetch = makeData(20, 'newJob');
// const profileData = newProfile()

export class RightTables extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tableHeaders: {
                dateFlagged: 'Date Flagged',
                id: 'Job ID #',
                plantID: 'Plant ID #',
                faultDescription: 'Fault Description',
                status: 'Fault Status'
            },
            tableData: this.props.jobs.people,
            profileTable:{
                id: 'ID',
                techName:'Name',
                techPhoneNumber: 'Phone Number',
                techAddress :'Address',
                techLocation:'Operating Location',
                techSkills: 'Accreditted Skills',
                techLanguages: 'Languages Spoken',
                techStartDate: 'Joining Date'
            },
            profileData:this.props.profile,
            infobtn:['edit']
        };
    }
    render() {
        return (
            <div className="techprofile center-block" >
                <div className="profile row center-block">
                    <TableList headers={this.state.profileTable} data ={this.state.profileData} />
                    <Notes title='Additional information' info={this.props.profile.techAdditionalInfo} buttons={this.state.infobtn} icon='sbn-icon-edit' />
                    <StatusInfo title='' info={this.props.profile}  />

                </div>
                <div className="row center-block">
                <h4>Job History</h4>
                    <Table headers={this.state.tableHeaders} pageSize={5} data={this.state.tableData} />
                </div>

            </div>
        )
    }
}
