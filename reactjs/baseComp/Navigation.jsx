import React from 'react';

export class Navigation extends React.Component {
    render() {
        return (

            <div id="main-nav">
                <div className="navbar-header navbar-default">
                    <button type="button" className="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                        <span className="sr-only">Toggle navigation</span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                    </button>
                </div>
                <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                    <ul className="nav navbar-nav ">
                        <li className="  active"><a  href="/dashboard">
                            <i className="c-icon fa fa-dashboard"></i>
                            <span>Dashboard</span></a>
                        </li>
                        <li className=" "><a  href="/plants">
                            <i className="c-icon fa fa-leaf"></i>
                            <span>BIOGAS PLANTS</span></a></li>
                        <li className=" "><a  href="/technicians">
                            <i className="c-icon fa fa-wrench"></i>
                            <span>TECHNICIANS</span></a></li>
                        <li className=" "><a  href="/jobs">
                            <i className="c-icon fa fa-suitcase"></i>
                            <span>Jobs</span></a></li>
                    </ul>
                </div>
            </div>

        )
    }
}