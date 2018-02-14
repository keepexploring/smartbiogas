import React from 'react';

import TableList from '../tables/TableList.jsx';
import Notes from '../info/Notes.jsx';
import StatusInfo from '../info/StatusInfo.jsx';
import BlockHeader from '../shared/BlockHeader.jsx';
import JobsTable from '../jobs/JobsTable.jsx';
import * as TechniciansService from '../../services/TechniciansService';
import * as Helpers from '../../utils/Helpers';

export default class TechnicianInfo extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			technicianHeaders: {
				id: 'ID',
				full_name: 'Name',
				phone_number: 'Phone Number',
				address: 'Address',
				location: 'Operating Location',
				skills: 'Accreditted Skills',
				languages: 'Languages Spoken',
				datetime_created: 'Joining Date'
			},
			technician: this.props.profile,
			jobs: [],
			infobtn: ['edit']
		};
	}
	
	componentDidUpdate(){ }

	componentDidMount(){
		// this.getJobsForCurrentUser(this.state.technician);
	}

	componentWillReceiveProps(props){
		this.setState({ 
			technician: props.profile
		});
		// this.getJobsForCurrentUser(props.profile);
	}

	getJobsForCurrentUser(profile){
		TechniciansService.getJobs(profile.id).then((response) => {
			this.setJobs(response.data);
		})
		.catch(function (error) {
			Helpers.handleHttpError(error);
		});
	}

	setJobs(jobs){
		this.setState({ 
			jobs: jobs
		});
	}

	render() {
		if(this.state && this.state.technician){
			return (
				<div className="col-md-6  center-block">
					<BlockHeader title='Technician Profile' />
					<div className="techprofile center-block" >
						<div className="profile col-md-12 center-block">
							<TableList headers={this.state.technicianHeaders} data={this.state.technician} />
						</div>
						<div className="col-md-12 profile center-block border-top">
							<Notes title='Additional information' info={this.state.technician.additional_info} buttons={this.state.infobtn} icon='sbn-icon-edit' />
							<StatusInfo title='' info={this.state.technician} />
						</div>
						<div className="col-md-12 profile-table border-top">
							<h4>Job History</h4>
							<JobsTable jobs={this.state.jobs} />
						</div>
					</div>
				</div>
			)
		}
		return('Loading');
	}
}
