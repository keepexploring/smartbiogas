import React from 'react';
import base from '../../css/base.scss';
import TopBar from './TopBar.jsx';
import { Table } from '../tables/Table.jsx';

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
			}
		};
	}

	componentWillReceiveProps(props){		
		this.setState((prevState, props) => ({
			values: props.jobs
		}));
	}

	render() {
		if (this.state && this.state.values) {
			if(this.state.values.length < 1){ return('No jobs found') }
			return (
				<div>
					<TopBar btnExtra={this.props.extra} />
					<Table data={this.state} />
				</div>
			);
		}
		return ("Loading");
	}
}