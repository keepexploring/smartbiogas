import React from 'react';
import { Link } from 'react-router-dom';

export default class Nav extends React.Component {
	constructor(props) {
		super(props);
		this.state = {};
		console.log('loaded nav');
	}

	render() {
		return (
			<nav className="navbar-header" id="main-nav">


				<div className="navbar-default">
					<button type="button" className="navbar-toggle" data-toggle="collapse" data-target="#navbar-collapse-1">
						<span className="sr-only">Toggle navigation</span>
						<span className="icon-bar"></span>
						<span className="icon-bar"></span>
						<span className="icon-bar"></span>
					</button>
					<div className="logo">
						<a className="img_icon" href="/dashboard">
							<img src='basetemplates/img/sb-logo-color.png' alt="." />
						</a>
						<a className="profile_icon" href="#profile_data" data-toggle="collapse">
							<i className="fa fa-caret-down"></i>
						</a>
						<div className="list-group collapse profile_box" id="profile_data">
							<nav id="mysidebarmenu" className="amazonmenu">
								<ul>
									<li><img src="" alt="." /><b>Sunil Ku. Sahu</b></li>
								</ul>
								<ul>
									<li><a href="#">Messages</a></li>
									<li><a href="#">Alerts</a></li>
									<li><a href="#">Account Details</a></li>
									<li><a href="#">Settings</a></li>
									<li><a href="/logout/">logout</a></li>
								</ul>
							</nav>
						</div>
					</div>
				</div>
				<div className="collapse navbar-collapse" id="navbar-collapse-1">
					<ul className="nav navbar-nav ">
						<li >
							<Link to="/dashboard">
								<span className="c-icon fa fa-dashboard"></span>
								<span>Dashboard</span>
							</Link>
						</li>
						<li>
							<Link to="/plants">
								<span className="c-icon fa fa-leaf"></span>
								<span>Biogas Plants</span>
							</Link>
						</li>
						<li>
							<Link to="/technicians">
								<span className="c-icon fa fa-wrench"></span>
								<span>Technicians</span>
							</Link>
						</li>
						<li>
							<Link to="/jobs">
								<span className="c-icon fa fa-suitcase"></span>
								<span>Jobs</span>
							</Link>
						</li>
					</ul>
				</div>
			</nav>
		)
	}
}
