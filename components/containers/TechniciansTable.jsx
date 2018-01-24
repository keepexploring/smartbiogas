import React from 'react';
import { Table } from '../tables/Table.jsx';
import TopBar from './TopBar.jsx';
import { TechnicianInfo } from '../containers/TechnicianInfo.jsx';
import BlockHeader from '../BlockHeader.jsx';
import { ModalPost } from './ModalPost.jsx';
import { ModalAccept } from './ModalAccept.jsx';
//import axios from 'axios';

const headers={
	full_name: 'Name',
	phone: 'Phone Number',
	location: 'Location',
	jobs_completed: 'Jobs',
	status: 'Status'
}
const statusOptions={
	active:'#63994e',
	inactive:'#a7d9e5',
	review: '#bf1622',
	withdrawn: '#fff'
}

export class TechniciansTable extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			statusOptions:statusOptions,
			tableData:{
				headers:headers,
				pageSize:10,
				values:this.props.values,
				selectRow: this.selectTechnician,
				statusOptions:statusOptions
			},
			values: this.props.values,
			currentTechnician: null,
			modalInfo: {
				header: 'Edit Technician',
				body: [],
				update: null
			}
		};
		// this.selectTechnician = this.selectTechnician.bind(this);
		this.toggleModal = this.toggleModal.bind(this);
		this.handleUpdate = this.handleUpdate.bind(this);
	}
	componentDidMount() {
		this.getModalInfo(this.state.values[0]);
	}
	// selectTechnician(rowInfo) {
	// 	this.setState({currentTechnician: rowInfo.original}, this.render);
	// }

	// componentDidUpdate(){
	// 	this.render();
	// }
	getModalInfo(profile) {
		/**
		 * Add job default 
		 * Should be added:
		 * 1.Autogenarated Job ID
		 * 2. Dropdown list for plant ID?
		 */
		const emptytech={}	
		emptytech.created_at='-';
		emptytech.image='true';
		this.setState({
			modalInfo: {
				body: {
					headers: headers,
					values: emptytech
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
		});
		this.getModalInfo(this.state.headers, this.state.values[0]);
	}
	render() {
        var technicianInfo = null;
        technicianInfo = <TechnicianInfo profile={this.state.currentTechnician} statusOptions={this.state.statusOptions} />
		const buttons={
			remove:{
				click_action: this.toggleModal,
				target: '#modalaccept',
				icon:'sbn-icon-subtrack',
				shape:'square-grey',
				size:'18',
				bootstrap:'col-md-2 col-sm-2 pull-right'
			},
			add:{
				click_action: this.toggleModal,
				target: '#modalpost',
				icon:'sbn-icon-add',
				shape:'square-grey',
				size:'18',
				bootstrap:'col-md-2 col-sm-2 pull-right'
			}
		};
		// if(this.state.currentTechnician != null) {
		// 	technicianInfo = <TechnicianInfo profile={this.state.currentTechnician} />
		// }

		return (
			<div className="technicians row center-block" >
				<div className="col-md-6  center-block">
					<BlockHeader title='Technicians List' />
					<div className="main-table row center-block" >
						<TopBar buttons={buttons} />
						<Table data={this.state.tableData} />
						<ModalPost header='Add Technician' show={this.state.isOpen} onClose={this.toggleModal} modalInfo={this.state.modalInfo} />
						<ModalAccept header='Delete Technician' show={this.state.isOpen} onClose={this.toggleModal} modalInfo={this.state.modalInfo} />
					</div>
				</div>
				{technicianInfo}
			</div>
		)
	}
}