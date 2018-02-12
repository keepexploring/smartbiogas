import React from 'react';
import { BrowserRouter as Router, Route, Link, Redirect, Switch } from 'react-router-dom';

import HttpClient from './utils/HttpClient.js';
import AuthService from './services/AuthService';

import Nav from './components/shared/Nav.jsx';
import Login from './components/login/Login.jsx';
import Dashboard from './components/dashboard/Dashboard.jsx';
import Jobs from './components/jobs/Jobs.jsx';
import Plants from './components/plants/Plants.jsx';
import Technicians from './components/technicians/Technicians.jsx';

export default class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			isLoggedIn: false
		};
	}

	componentWillMount() {
		AuthService.initialise();
		console.log(AuthService.isLoggedIn, AuthService.currentUser);
		if (AuthService.isLoggedIn) {
			HttpClient.initialise(AuthService.currentUser.access_token);
		}
	}

	render() {
		if(!AuthService.isLoggedIn){
			console.log('Logged OUT');
			return(
				<Router>
					<div>
						<Redirect to='/login' />
						<Route exact path="/login" component={Login} />
					</div>
				</Router>
			);
		}

		console.log('Logged IN');

		return(
			<Router>
				<div>
					<Nav />
					<Route exact path="/" component={Dashboard} />
					<Route path="/jobs" component={Jobs} />
					<Route path="/plants" component={Plants} />
					<Route path="/technicians" component={Technicians} />
					<Route path="/login" component={Login} />
				</div>
			</Router>
		);

	}
}
