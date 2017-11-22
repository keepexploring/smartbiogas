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
                    <ul className="nav nav-tabs ">
                        <li className="c-tabs active"><a data-toggle="tab" href="#dashboard">
                            <i className="c-icon fa fa-dashboard"></i>
                            <span>Dashboard</span></a>
                        </li>
                        <li className="c-tabs"><a data-toggle="tab" href="#plants">
                            <i className="c-icon fa fa-leaf"></i>
                            <span>BIOGAS PLANTS</span></a></li>
                        <li className="c-tabs"><a data-toggle="tab" href="#technicians">
                            <i className="c-icon fa fa-wrench"></i>
                            <span>TECHNICIANS</span></a></li>
                        <li className="c-tabs"><a data-toggle="tab" href="#jobs">
                            <i className="c-icon fa fa-suitcase"></i>
                            <span>Jobs</span></a></li>
                    </ul>
                </div>
            </div>

        )
    }
}