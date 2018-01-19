import React from 'react';
import TableList from '../tables/TableList.jsx';
import Notes from '../info/Notes.jsx';
import StatusInfo from '../info/StatusInfo.jsx';
import BlockHeader from '../BlockHeader.jsx';
import {JobsTable} from './JobsTable.jsx';
import {ModalPost} from './ModalPost.jsx';
//import http from '../../HttpClient';
import { makeData, newProfile } from "../tables/TableUtilities.jsx"; //Test data constructor
const profileData = newProfile();
const techJobsData = makeData(20, 'newJob');



export class TechnicianInfo extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			technicianHeaders: {
				id: 'ID',
				full_name: 'Name',
				phone: 'Phone Number',
				address: 'Address',
				location: 'Operating Location',
				skills: 'Accreditted Skills',
				languages: 'Languages Spoken',
				created_at: 'Joining Date'
			},
			techStatus:props.statusOptions,
            //technician: this.props.profile,
            technician:profileData,
			jobs: [],
			isOpen: false,
			modalInfo:{
				header:'Edit Technician',
				body:[]
			}
		}
		this.toggleModal=this.toggleModal.bind(this);
	}

	componentDidMount(){
		this.getJobsForCurrentUser(this.state.technician);
		this.getModalInfo(this.state.technicianHeaders,this.state.technician);
	}

	componentWillReceiveProps(props){
        //this.getJobsForCurrentUser(props.profile);
		this.getJobsForCurrentUser(this.state.technician);
		this.getModalInfo(this.state.technician);
	}
	getModalInfo(headers,profile){
		this.setState({ 
			modalInfo:{
				body:{
					headers:headers,
					values:profile
				}
			  } 
			
    	});
	}
	getJobsForCurrentUser(profile){
        this.setState({ 
			jobs: techJobsData.people,
			
    	});
		// http.get('jobs/by-user/' + profile.id)
		// .then((response) => {
		// 	this.setState({ 
		// 		jobs: response.data,
		// 		technician: profile
		// 	});
		// })
		// .catch(function (error) {
		// 	console.log(error);
		// });
	}

	toggleModal(){
		console.log('pass')
		this.setState({
		  isOpen: !this.state.isOpen,
		});
	  }

	render() {
		const edit={
			click_action:this.toggleModal,
			target:'#modalpost',
		}
		if(this.state && this.state.technician){
			const infoPills={
				years_pill:{
					title:'Years Active',
					value:this.state.technician.years_active,
					icon:'sbn-icon-dial'
				},
				jobs_pill:{
					title:'Jobs Completed',
					value:this.state.technician.jobs_completed,
					icon:'sbn-icon-case'
				},
				status_pill:{
					value:this.state.technician.status,
					color:this.state.techStatus[this.state.technician.status]
				}
			}

			return (
				<div className="col-md-6  center-block">
					<BlockHeader title='Technician Profile' />
					<div className="techprofile center-block" >
						
						<div className="profile col-md-12 center-block">
							<TableList headers={this.state.technicianHeaders} data={this.state.technician} editable={false}/>
						</div>
						
						<div className="col-md-12 profile center-block border-top">
							<Notes title='Additional information' info={this.state.technician.additional_info} buttons={edit} icon='sbn-icon-edit' />
							<StatusInfo title='' info={infoPills} />
						</div>

						<div className="col-md-12 profile-table border-top">
							<h4>Job History</h4>
							<JobsTable jobs={this.state.jobs} size={5} extra={false} />
						</div>
				
						<ModalPost show={this.state.isOpen} onClose={this.toggleModal} modalInfo={this.state.modalInfo} />
					</div>
				</div>
			)
		}
		return('Loading');
		
	}
}