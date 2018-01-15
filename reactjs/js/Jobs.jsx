import React from 'react';
import ReactDOM from 'react-dom';
import base from '../css/base.scss';

import BlockHeader from '../components/BlockHeader.jsx';
import Table from '../components/tables/Table.jsx';
import { RightSide } from '../components/containers/RightSide.jsx';
import { LeftSide } from '../components/containers/LeftSide.jsx';

import { makeData, detailsJob } from "../components/tables/TableUtilities.jsx"; //Test data constructor

//var dashboard_sock = 'ws://' + window.location.host + "/jobs/"
const jobData = makeData(20, 'newJob');
const techJobsData = makeData(20, 'newJob');
const profileData = detailsJob();

const mainHeaders={
    dateFlagged: 'Date Flagged',
    id: 'Job ID #',
    plantID: 'Plant ID #',
    idTech: 'Tech ID #',
    faultDescription: 'Fault Description',
    status: 'Fault Status'
}
const listHeaders={
    id: 'Job ID',
    plantID:'Plant ID',
    techID: 'Technician ID',
    dateFlagged: 'Date Flagged',
    overdueDate: 'Overdue Date',
    faultDescription: 'Issue Identified'
}

export class Jobs extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mainTableData:{
                tableHeaders: mainHeaders,
                tableValues: jobData.people
            },
            profileData:{
                pageID: "jobs",
                profileHeaders:listHeaders,
                profilevalues:profileData,
            },
            
            /*techData: {
                techName: '',
                techPhoneNumber: '',
                techLocation: '',
                techJobs: '',
                status: ''
            }*/
        };

    }
    /*  -------Real data parse-------
    componentWillMount() {
        //receives messages
        let parsed_data = JSON.parse(this.props.data);
        this.setState({
            techData: {
                techName: parsed_data.techName,
                techPhoneNumber: parsed_data.techPhoneNumber,
                techLocation: parsed_data.techLocation,
                techJobs: parsed_data.techLocation,
                status: parsed_data.techStatus
            }
        })
    }
    handleData(data) {
        //receives messages from the connected websocket
        let parsed_data = JSON.parse(data);
        this.setState({
            techData: {
                techName: parsed_data.techName,
                techPhoneNumber: parsed_data.techPhoneNumber,
                techLocation: parsed_data.techLocation,
                techJobs: parsed_data.techLocation,
                status: parsed_data.techStatus
            }
        });
    }
    **/
    render() {
        return (
            <div className="row center-block" >
                <div className="col-md-6  center-block">
                    <BlockHeader title='Job List' />
                    <LeftSide data = {this.state.mainTableData} />
                </div>
                <div className="rightSide col-md-6 center-block">
                    <BlockHeader title='Job Details' />
                    <RightSide profile={this.state.profileData} />
                </div>
            </div>
        )
    }
}
const rootElement = document.getElementById('jobs');
ReactDOM.render(<Jobs />, rootElement);