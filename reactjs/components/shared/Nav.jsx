import React from 'react';
import ReactDOM from 'react-dom';

export class Nav extends React.Component {
	constructor(props) {
		super(props);
		this.state = {};
	}
	render() {
		return (
			<div id="header">
				<div class="head-nav navbar navbar-fixed-top" role="navigation">
					<nav class="navbar-header" id="main-nav">
						<div class="navbar-default">
							<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar-collapse-1">
								<span class="sr-only">Toggle navigation</span>
								<span class="icon-bar"></span>
								<span class="icon-bar"></span>
								<span class="icon-bar"></span>
							</button>
							<div class="logo">
								<a class="img_icon" href="/dashboard">
									{/* TODO */}
									<img src='/basetemplates/img/sb-logo-color.png' alt="Smart Biogas" />
								</a>
								<a class="profile_icon" href="#profile_data" data-toggle="collapse">
									<i class="fa fa-caret-down"></i>
								</a>
								<div class="list-group collapse profile_box" id="profile_data">
									<nav id="mysidebarmenu" class="amazonmenu">
										<ul>
											{/* {% if userimg %} */}
											{/* TODO */}
											<li><img src="http://placehold.it/100/100" alt="User image" /><b>Sunil Ku. Sahu</b></li>
											{/* {% endif %} */}
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
						<div class="collapse navbar-collapse" id="navbar-collapse-1">
							<ul class="nav navbar-nav ">
								<li >
									<a href="/#dashboard">
										<i class="c-icon fa fa-dashboard"></i>
										<span>Dashboard</span>
									</a>
								</li>
								<li>
									<a href="/#plants">
										<i class="c-icon fa fa-leaf"></i>
										<span>Biogas Plants</span>
									</a>
								</li>
								<li>
									<a href="/#technicians">
										<i class="c-icon fa fa-wrench"></i>
										<span>Technicians</span>
									</a>
								</li>
								<li>
									<a href="/#jobs">
										<i class="c-icon fa fa-suitcase"></i>
										<span>Jobs</span>
									</a>
								</li>
							</ul>
						</div>
					</nav>
				</div>
			</div>
		);
	}
}
