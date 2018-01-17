import React from 'react';
import ReactDOM from 'react-dom';
import base from '../css/base.scss';

import { JobsContainer } from '../components/containers/JobsContainer.jsx';
//import http from '../HttpClient';

import { makeData, newProfile } from "../components/tables/TableUtilities.jsx"; //Test data constructor

const jobData = makeData(20, 'newJob');

//const profileData = detailsJob();

export class Jobs extends React.Component {
    constructor(props) {
		super(props);
		this.state = {
			jobs: [],
		};
	}
    componentWillMount() {
		// http.get('jobs')
		// 	.then((response) => {
		// 		this.setState({
		// 			jobs: response.data
		// 		});
		// 		this.render();
		// 	})
		// 	.catch(function (error) {
		// 		console.log(error);
        // 	});
        this.setState({
            jobs: jobData.people
        })
	}
    render() {
		if (this.state && this.state.jobs.length > 0) {
			return (
				<JobsContainer values={this.state.jobs} />
			);
		}
		return ("loading");
	}
    
}
const rootElement = document.getElementById('jobs');
ReactDOM.render(<Jobs />, rootElement);