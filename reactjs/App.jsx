import React from 'react';
import ReactDOM from 'react-dom';
import base from './css/base.scss';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import Nav from './components/shared/Nav.jsx';
import Dashboard from './components/dashboard/Dashboard.jsx';
import Technicians from './components/technicians/Technicians.jsx';
import Jobs from './components/jobs/Jobs.jsx';
import Plants from './components/plants/Plants.jsx';

// import * as DataService from '../../services/DataService';
// import * as Helpers from '../../utils/Helpers';

export const routes = [
	{
		path: '/',
		// exact: true,
		main: () => <h2>Login</h2>
	},
	{
		path: '/#dashboard',
		main: () => <Dashboard />
	},
	{
		path: '/#technicians',
		main: () => <Technicians />
	},
	{
		path: '/#jobs',
		main: () => <Jobs />
	},
	{
		path: '/#plants',
		main: () => <Plants />
	}
]

export class SmartBiogas extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			loggedIn: false
		};
	}

	componentWillMount() {
		console.log(this);
	}

	render() {
		return (
			<Router>
				<Nav />
				{routes.map((route, index) => (
					// Render more <Route>s with the same paths as
					// above, but different components this time.
					<Route
						key={index}
						path={route.path}
						exact={route.exact}
						component={route.main}
					/>
				))}
			</Router>
		);
	}
}

const rootElement = document.getElementById('app');
ReactDOM.render(<app data={rootElement.getAttribute('data-data')} />, rootElement);
