import React from 'react';
import ReactDOM from 'react-dom';
import base from '../css/base.scss';

import BlockHeader from '../components/BlockHeader.jsx';
import Table from '../components/tables/Table.jsx';
import { RightTables } from '../components/RightTables.jsx';

import { makeData, newProfile } from "../components/tables/TableUtilities.jsx"; //Test data constructor

//var dashboard_sock = 'ws://' + window.location.host + "/technicians/"
const techData = makeData(20, 'newTechnician');
const techJobsData = makeData(20, 'newJob');
const profileData = newProfile();

export class Technicians extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tableHeaders: {
                techName: 'Name',
                techPhoneNumber: 'Phone Number',
                techLocation: 'Location',
                techJobs: 'Jobs',
                status: 'Status'
            },
            techJobsData:techJobsData,
            profileData:profileData,
            techData: techData.people,
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
            <div className="technicians row center-block" >
                <div className="col-md-6  center-block">
                    <BlockHeader title='Technicians List' />
                    <Table headers={this.state.tableHeaders} pageSize={10} data={this.state.techData} />

                </div>
                <div className="col-md-6  center-block">
                    <BlockHeader title='Technician Profile' />
                    <RightTables profile={this.state.profileData} jobs={this.state.techJobsData} />
                </div>

            </div>
        )
    }
}
const rootElement = document.getElementById('technicians');
ReactDOM.render(<Technicians />, rootElement);