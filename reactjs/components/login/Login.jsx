import React from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Link, Redirect, Switch } from 'react-router-dom';

import * as constants from '../../utils/Constants';
import SvgIcon from '../shared/SvgIcon.jsx';
import Loading from '../shared/Loading.jsx';
import AuthService from '../../services/AuthService';
import Authenticated from '../../models/Authenticated';
import HttpClient from '../../utils/HttpClient';
import Dashboard from '../dashboard/Dashboard.jsx';

export default class Login extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			username: '',
			password: '',
			errorMessage: '',
			isLoading: false,
			redirect: AuthService.isLoggedIn
		};

		this.usernameChange = this.usernameChange.bind(this);
		this.passwordChange = this.passwordChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
	}

	clearErrors() {
		if(this.state.errorMessage && this.state.errorMessage != ''){
			this.setState({errorMessage: ''});
		}
	}

	usernameChange(event) {
		this.setState({username: event.target.value});
		this.clearErrors();
	}
	
	passwordChange(event) {
		this.setState({password: event.target.value});
		this.clearErrors();
	}

	isDisabled(){
		return this.state.username === '' || this.state.password === '';
	}

	getErrors() {
		if(this.state.errorMessage && this.state.errorMessage != '') {
			return(<div className="text-danger text-center">{ this.state.errorMessage }</div>);
		}
	}

	getSubmitButton() {
		return(this.state.isLoading ? <Loading /> : 
			<button type="submit" className="btn-submit" disabled={this.isDisabled()} >
				<SvgIcon name="sbn-icon-tick" color="icon-white" />
			</button>);
	}

	processAuthenticationData(data) {
		// console.log(data);
		let authenticated;
		try {
			authenticated = new Authenticated (
				data.access_token, 
				data.token_type, 
				data.expires_in, 
				data.refresh_token,
				data.scope
			);
		} catch (err) {
			console.log(err);
		}
		return authenticated;
	}

	getToken(username, password) {
		let params = new URLSearchParams();
		params.append('username', username);
		params.append('password', password);
		params.append('grant_type', 'password');
		params.append('client_id', '123456');
		params.append('client_secret', '123456');
		let config = { headers: { 
			'Content-Type': 'application/x-www-form-urlencoded',
			'Accept': 'application/json',
		} };
		return axios.post(constants.tokenEndpoint, params, config);
	};

	handleSubmit(event) {
		event.preventDefault();
		this.setState({isLoading: true});

		this.getToken(this.state.username, this.state.password).then((response) => {
			let authenticated = this.processAuthenticationData(response.data);
			AuthService.setCurrentUser(authenticated);
			HttpClient.initialise(authenticated.access_token);
			this.setState({redirect: true});
		})
		.catch((error) => {
			if (error.response) {
				this.setState({ errorMessage: error.response.data.error_description });
			}
			this.render();
		})
		.finally(() => { 
			this.setState({ isLoading: false }); 
		});
	}

	render() {
		if(this.state.redirect) {
			return(
				<Router>
					<div>
						<Redirect to='/' />
						<Route exact path="/" component={Dashboard} />
					</div>
				</Router>
			);
		}

		let loginView = <div className="login-template container form-horizontal margin-top">
			<header>
				<h1 className="text-center fancy text-white">Login</h1>
			</header>
			<form onSubmit={this.handleSubmit}>
				<input type="hidden" name="grant_type" value="password" />
				<input type="hidden" name="client_id" value="123456" />
				<input type="hidden" name="client_secret" value="123456" />
				<div className="form-group">
					<label className="col-sm-2 control-label text-white {this.isLoading ? 'disabled': ''}" htmlFor="username">Username</label>
					<div className="col-sm-10">
						<input className="form-control" type="text" name="username" value={this.state.username} onChange={this.usernameChange}/>
					</div>
				</div>
				<div className="form-group">
					<label className="col-sm-2 control-label text-white" htmlFor="password">Password</label>
					<div className="col-sm-10">
						<input className="form-control" type="password" name="password" value={this.state.password} onChange={this.passwordChange} />
					</div>
				</div>
				<div className="form-group text-center">
					{ this.getSubmitButton() }
				</div>
			</form>
			{ this.getErrors() }
		</div>;



		return (loginView);
	};

	
}
