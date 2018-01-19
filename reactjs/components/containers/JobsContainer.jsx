import React from 'react';
import TopBar from './TopBar.jsx';
import { JobsTable } from '../containers/JobsTable.jsx';
import { JobInfo } from '../containers/JobInfo.jsx';
import BlockHeader from '../BlockHeader.jsx';
//import axios from 'axios';

export class JobsContainer extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			values: this.props.values,
			currentJob: null,
		};
		// this.selectJob = this.selectJob.bind(this);
	}

	// selectJob(rowInfo) {
	// 	this.setState({currentJob: rowInfo.original}, this.render);
	// }

	// componentDidUpdate(){
	// 	this.render();
	// }

	render() {
        var jobInfo = null;
        jobInfo = <JobInfo profile={this.state.currentJob} />
		// if(this.state.currentJob != null) {
		// 	technicianInfo = <TechnicianInfo profile={this.state.currentTechnician} />
		// }

		return (
			<div className="jobs row center-block" >
				<div className="col-md-6  center-block">
					<BlockHeader title='Jobs List' />
					<div className="main-table row center-block" >
						{/* <TopBar btnExtra={true} /> */}
                        <JobsTable jobs={this.state.values} size={10} extra={true} />
					</div>
				</div>
				{jobInfo}
			</div>
		)
	}
}