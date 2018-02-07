import React from 'react';
import { Table } from '../tables/Table.jsx';
import TopBar from '../containers/TopBar.jsx';
import BlockHeader from '../BlockHeader.jsx';
import { TechnicianInfo } from './TechnicianInfo.jsx';
import axios from 'axios';

export class TechniciansTable extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			headers: {
				full_name: 'Name',
				phone: 'Phone Number',
				location: 'Location',
				jobs_completed: 'Jobs',
				status: 'Status'
			},
			values: this.props.values,
			currentTechnician: null
		};
		this.selectTechnician = this.selectTechnician.bind(this);
	}

	selectTechnician(rowInfo) {
		this.setState({currentTechnician: rowInfo.original}, this.render);
	}

	componentDidUpdate(){
		this.render();
	}

	render() {
		var technicianInfo = null;
		if(this.state.currentTechnician != null) {
			technicianInfo = <TechnicianInfo profile={this.state.currentTechnician} />
		}

		return (
			<div className="technicians row center-block" >
				<div className="col-md-6  center-block">
					<BlockHeader title='Technicians List' />
					<div className="main-table row center-block" >
						<TopBar btnExtra={true} />
						<Table headers={this.state.headers} pageSize={10} data={this.state.values} selectRow={this.selectTechnician} />
					</div>
				</div>
				{technicianInfo}
			</div>
		)
	}
}
