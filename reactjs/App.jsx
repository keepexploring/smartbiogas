import React from 'react';
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom';

import Nav from './components/shared/Nav.jsx';
import Login from './components/login/Login.jsx';
import Dashboard from './components/dashboard/Dashboard.jsx';
import Jobs from './components/jobs/Jobs.jsx';
import Plants from './components/plants/Plants.jsx';
import Technicians from './components/technicians/Technicians.jsx';

// import * as DataService from '../../services/DataService';
// import * as Helpers from '../../utils/Helpers';

export default class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	render() {
		console.log('app');
		return (
			<Router>
				<div>
					<Nav />
					<Route exact path="/" component={Login} />
					<Route path="/dashboard" component={Dashboard} />
					<Route path="/jobs" component={Jobs} />
					<Route path="/plants" component={Plants} />
					<Route path="/technicians" component={Technicians} />
				</div>
			</Router>
		);
	}
}
