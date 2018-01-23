import React from 'react';
import base from '../../css/base.scss';
import TopBar from './TopBar.jsx';
import { Table } from '../tables/Table.jsx';
import { ModalPost } from './ModalPost.jsx';

export class JobsTable extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			values: this.props.jobs,
			headers: {
				created_at: 'Date Flagged',
				id: 'Job ID #',
				plant_id: 'Plant ID #',
				fault_description: 'Fault Description',
				fault_status: 'Fault Status'
			},
			pageSize:this.props.size,
			statusOptions:{
				complete:'#63994e',
				resolving:'#a7d9e5',
				unassigned: '#a7d9e5',
				overdue: '#bf1622',
				assistance: '#bf1622',
				feedback: '#bf1622'
			},
			isOpen: false,
			modalInfo:{
				header: 'Add Job',
				body: [],
				update: null
			}
		};
		this.toggleModal = this.toggleModal.bind(this);
		this.handleUpdate = this.handleUpdate.bind(this);
	}
	componentDidMount() {
		this.getModalInfo(this.state.headers, this.state.values[0]);
	}
	componentWillReceiveProps(props){		
		this.setState((prevState, props) => ({
			values: props.jobs
		}));
		//this.getModalInfo(this.state.headers, this.state.values[0]);
	}

	getModalInfo(headers, profile) {
		let emptyobj={}	
		let empty=Object.keys(profile).map(function (key, index) {
			emptyobj[key]='-'
		});
		console.log(emptyobj);
		this.setState({
			modalInfo: {
				body: {
					headers: headers,
					values: emptyobj
				},
				update: this.handleUpdate
			}

		});
	}
	toggleModal() {
		this.setState({
			isOpen: !this.state.isOpen,
		});
	}
	handleUpdate(newData) {
		this.setState({
			isOpen: !this.state.isOpen,
		})
	}

	render() {
		const buttons={
			add:{
				click_action: this.toggleModal,
				target: '#modalpost',
			},
			remove:{
				click_action: this.toggleModal,
				target: '#modalpost',
			}
		}
		
		if (this.state && this.state.values) {
			if(this.state.values.length < 1){ return('No jobs found') }
			return (
				<div>
					<TopBar btnExtra={this.props.extra} buttons={buttons}/>
					<Table data={this.state} />
					<ModalPost show={this.state.isOpen} onClose={this.toggleModal} modalInfo={this.state.modalInfo} />
				</div>
			);
		}
		return ("Loading");
	}
}