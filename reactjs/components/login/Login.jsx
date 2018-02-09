import React from 'react';
import SvgIcon from '../shared/SvgIcon.jsx';

export default class Login extends React.Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	render() {
		return (
			<form method="post" action="">
				<div className="form-group">
					<label className="form-label" htmlFor="username">Username</label>
					<input className="form-control" type="text" name="username"/>
				</div>
				<div className="form-group">
					<label className="form-label" htmlFor="password">Password</label>
					<input className="form-control" type="password" name="password"/>
				</div>
				<div className="form-group">
					<label className="checkbox" htmlFor="password">
						<input type="checkbox"/> Remember me
					</label>
				</div>
				<div className="form-group">
					<button type="submit" className="btn btn-primary">
						<SvgIcon name="sbn-icon-tick" color="white" /> Login
					</button>
				</div>
			</form>
		);
	};
}
