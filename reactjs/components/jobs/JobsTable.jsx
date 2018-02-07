import React from 'react';
import ReactDOM from 'react-dom';
import base from '../../css/base.scss';
import TopBar from '../containers/TopBar.jsx';
import { Table } from '../tables/Table.jsx';

export class JobsTable extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			jobs: this.props.jobs,
			headers: {
				created_at: 'Date Flagged',
				id: 'Job ID #',
				plant_id: 'Plant ID #',
				fault_description: 'Fault Description',
				fault_status: 'Fault Status'
			},
		};
	}

	componentWillReceiveProps(props){		
		this.setState((prevState, props) => ({
			jobs: props.jobs
		}));
	}

	render() {
		if (this.state && this.state.jobs) {
			if(this.state.jobs.length < 1){ return('No jobs found') }
			return (
				<div>
					<TopBar btnExtra={false} />
					<Table headers={this.state.headers} pageSize={5} data={this.state.jobs} />
				</div>
			);
		}
		return ("Loading");
	}
}
