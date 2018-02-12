import React from 'react';

import SvgIcon from '../shared/SvgIcon.jsx';
import { requestToken } from '../../services/AuthService';
import Loading from '../shared/Loading.jsx';

export default class Login extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			username: '',
			password: '',
			errorMessage: '',
			isLoading: false,
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

	handleSubmit(event) {
		event.preventDefault();
		this.setState({isLoading: true});
		requestToken(this.state.username, this.state.password).then((response) => {
			console.log('TODO: Handle response', response);
		})
		.catch((error) => {
			if (error.response) {
				this.setState({ errorMessage: error.response.data.error_description });
			}
			this.render();
		}).finally(() => { this.setState({ isLoading: false }); });
	}

	render() {

		let isDisabled = this.state.username === '' || this.state.password === '';

		let errors;
		if(this.state.errorMessage && this.state.errorMessage != '') {
			errors = <div className="text-danger text-center">{ this.state.errorMessage }</div>;
		}

		let submitButton;
		if(this.state.isLoading) {
			submitButton = <Loading />;
		} else {
			submitButton = <button type="submit" className="btn-submit" disabled={isDisabled} >
				<SvgIcon name="sbn-icon-tick" color="icon-white" />
			</button>;
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
					{ submitButton }
				</div>
			</form>
			{ errors }
		</div>;

		return (loginView);
	};

	
}
