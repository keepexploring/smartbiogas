import React from 'react';

import DashBox from './DashBox.jsx';
import DashGraph from './DashGraph.jsx';
import DashButton from './DashButton.jsx';
import * as DataService from '../../services/DataService';
import * as Helpers from '../../utils/Helpers';

export default class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      titles: {
        totalPlants: "No. Plants",
        activePlants: "No. Active Plants",
        totalFaults: "Total Faults",
        averageRepairTime: "Average Repair Time (Days)",
        ongoingJobs: "Ongoing Jobs",
        faultsFixed: "Faults fixed"
      },
      icons: {
        totalPlants: "sbn-icon-leaf",
        activePlants: "sbn-icon-tick",
        totalFaults: "sbn-icon-alert",
        averageRepairTime: "sbn-icon-dial",
        ongoingJobs: "sbn-icon-case",
        faultsFixed: "sbn-icon-technician"
      },
      btnView: true,
      data: {
        totalPlants: 'No data',
        activePlants: 'No data',
        totalFaults: 'No data',
        averageRepairTime: 'No data',
        ongoingJobs: 'No data',
        faultsFixed: 'No data'
      },
      loaded: false
    };
    this.btnWidg = this.btnWidg.bind(this);
    this.btnGraph = this.btnGraph.bind(this);
  }

  componentWillMount() {
    var th = this;
    DataService.getDashboardData().then((response) => {
      let dashboardData = response.data.objects[0];
      console.log('dashboard', dashboardData);
      th.setState({
        data: {
          totalPlants: dashboardData.plants,
          activePlants: dashboardData.active,
          totalFaults: dashboardData.faults,
          averageRepairTime: dashboardData.avtime,
          ongoingJobs: dashboardData.jobs,
          faultsFixed: dashboardData.fixed
        },
        loaded: true
      })
    })
      .catch(function (error) {
        Helpers.handleHttpError(error);
      });
  }

  render() {
    const boxList = Object.keys(this.state.titles).map(function (key, index) {
      return (
        <DashBox 
          key={key}
          title={this.state.titles[key]}
          value={String(this.state.data[key])}
          icon={this.state.icons[key]} 
        />
      )
    }, this);

    if (this.state && this.state.loaded) {
      return (
        <div className="dashboard col-md-12 center-block" id="dashboard">
          <h1 className="text-center text-green">Dashboard</h1>
          <div className="col-md-1 dash-btn text-center">
            <DashButton icon="fa fa-info" action={this.btnWidg} item="1" active={this.state.btnView} />
            <DashButton icon="fa fa-signal" action={this.btnGraph} item="2" />
          </div>
          <div id="widgets" className="col-md-11 center-block">
            {this.state.btnView ? boxList : <DashGraph />}
          </div>
        </div>
      )
    }
    return ("loading...");
  }

  btnWidg() {
    this.setState({
      btnView: true
    })
    document.getElementById
  }

  btnGraph() {
    this.setState({
      btnView: false
    })
  }
}