import React from 'react';
import ReactDOM from 'react-dom';
import base from '../../css/base.scss';
import SvgIcon from '../shared/SvgIcon.jsx';

export class Login extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
		};
	}

	componentWillMount() {

	}

	render() {
		return (
			<form method="post" action="">
				<div className="form-group">
					<label class="form-label" htmlFor="username">Username</label>
					<input class="form-control" type="text" name="username"/>
				</div>
				<div className="form-group">
					<label class="form-label" htmlFor="password">Password</label>
					<input class="form-control" type="password" name="password"/>
				</div>
				<div className="form-group">
					<label class="checkbox" htmlFor="password">
						<input type="checkbox"/> Remember me
					</label>
				</div>
				<div className="form-group">
					<button type="submit" class="btn btn-primary"><SvgIcon name="sbn-icon-tick" color="white" /> Login</button>
				</div>
			</form>
		);
	};
}

const rootElement = document.getElementById('login');
ReactDOM.render(<Login data={rootElement.getAttribute('data-data')} />, rootElement);
