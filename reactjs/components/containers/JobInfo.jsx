import React from 'react';
import TableList from '../tables/TableList.jsx';
import Notes from '../info/Notes.jsx';
import StatusInfo from '../info/StatusInfo.jsx';
import BlockHeader from '../BlockHeader.jsx';
import { ModalPost } from './ModalPost.jsx';
//import http from '../../HttpClient';

import { makeData, detailsJob } from "../tables/TableUtilities.jsx"; //Test data constructor
const profileData = detailsJob();

export class JobInfo extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			jobHeaders: {
                id: 'Job ID',
                plant_id:'Plant ID',
                tech_id: 'Technician ID',
                created_at: 'Date Flagged',
                overdue: 'Overdue Date',
                fault_description: 'Issue Identified',
            },
            jobStatus:{
                complete:'#63994e',
                resolving:'#63994e',
                unassigned: '#63994e',
                overdue: '#63994e',
            },
            //job: this.props.profile,
            job:profileData,
			infobtn: ['edit'],
			isOpen: false,
			modalInfo: {
				header: 'Edit Job Details',
				body: [],
				update:null
			}
        };
		this.toggleModal = this.toggleModal.bind(this);
		this.handleUpdate = this.handleUpdate.bind(this);
	}

	componentDidMount(){
		//this.getJobsForCurrentUser(this.state.job);
		this.getModalInfo(this.state.jobHeaders,this.state.job);
	}

	componentWillReceiveProps(props){
		//this.getJobsForCurrentUser(props.profile);
		this.getModalInfo(this.state.jobHeaders,this.state.job);   
	}

	// getJobsForCurrentUser(profile){
    //     this.setState({ 
    //         jobs: techJobsData.people
    // 	});
	// 	// http.get('jobs/by-user/' + profile.id)
	// 	// .then((response) => {
	// 	// 	this.setState({ 
	// 	// 		jobs: response.data,
	// 	// 		technician: profile
	// 	// 	});
	// 	// })
	// 	// .catch(function (error) {
	// 	// 	console.log(error);
	// 	// });
	// }

	/*Edit form and update*/
	getModalInfo(headers, profile) {
		this.setState({
			modalInfo: {
				body: {
					headers: {
						created_at: 'Date Flagged',
						id: 'Job ID #',
						plant_id:'Plant ID #',
						fault_description: 'Fault Description',
						additional_info: 'Additional Information'
					},
					values: profile
				},
				update:this.handleUpdate
			}

		});
	}
	toggleModal() {
		this.setState({
			isOpen: !this.state.isOpen,
		});
	}
	handleUpdate(newData){
		this.setState({
			technician: newData,
			isOpen: !this.state.isOpen,
		  })
	}

	render() {
		const edit = {
			click_action: this.toggleModal,
			target: '#modalpost',
		}

		const infoPills={
			status_pill:{
				value:this.state.job.status,
				color:this.state.jobStatus[this.state.job.status]
			}
		}
		if(this.state && this.state.job){
			return (
				<div className="col-md-6  center-block">
					<BlockHeader title='Job Details' />
					<div className="jobprofile center-block" >
						<div className="profile col-md-12 center-block">
							<TableList headers={this.state.jobHeaders} data={this.state.job} />
						</div>
						
						<div className="col-md-12 profile center-block border-top">
							<Notes title='Additional information' info={this.state.job.additional_info} buttons={edit} icon='sbn-icon-edit' />
							<StatusInfo title='Job status' info={infoPills} />
						</div>

						<div className="col-md-12 profile-table border-top">
							<h4>Client Feedback</h4>	
						</div>
						<ModalPost show={this.state.isOpen} onClose={this.toggleModal} modalInfo={this.state.modalInfo} />
					</div>
				</div>
			)
		}
		return('Loading');
		
	}
}