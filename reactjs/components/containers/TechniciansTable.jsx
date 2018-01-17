import React from 'react';
import { Table } from '../tables/Table.jsx';
import TopBar from './TopBar.jsx';
import { TechnicianInfo } from '../containers/TechnicianInfo.jsx';
import BlockHeader from '../BlockHeader.jsx';
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
	inactive:'#63994e',
	review: '#63994e',
	withdrawn: '#63994e'
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
			currentTechnician: null
		};
		// this.selectTechnician = this.selectTechnician.bind(this);
	}

	// selectTechnician(rowInfo) {
	// 	this.setState({currentTechnician: rowInfo.original}, this.render);
	// }

	// componentDidUpdate(){
	// 	this.render();
	// }

	render() {
        var technicianInfo = null;
        technicianInfo = <TechnicianInfo profile={this.state.currentTechnician} statusOptions={this.state.statusOptions} />

		// if(this.state.currentTechnician != null) {
		// 	technicianInfo = <TechnicianInfo profile={this.state.currentTechnician} />
		// }

		return (
			<div className="technicians row center-block" >
				<div className="col-md-6  center-block">
					<BlockHeader title='Technicians List' />
					<div className="main-table row center-block" >
						<TopBar btnExtra={true} />
						<Table data={this.state.tableData} />
					</div>
				</div>
				{technicianInfo}
			</div>
		)
	}
}