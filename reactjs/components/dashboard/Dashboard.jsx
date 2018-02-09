import React from 'react';
import ReactDOM from 'react-dom';
import Websocket from 'react-websocket';
import base from '../../css/base.scss';

import DashBox from './DashBox.jsx';
import DashGraph from './DashGraph.jsx';
import DashButton from './DashButton.jsx';
import * as DataService from '../../services/DataService';
import * as Helpers from '../../utils/Helpers';

var dashboard_sock = 'ws://' + window.location.host + "/dashboard/"

export class Dashboard extends React.Component {
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
      icons:{
        totalPlants: "sbn-icon-leaf",
        activePlants: "sbn-icon-tick",
        totalFaults: "sbn-icon-alert",
        averageRepairTime: "sbn-icon-dial",
        ongoingJobs: "sbn-icon-case",
        faultsFixed: "sbn-icon-technician"
      },
      btnView: true,
      data:{
        totalPlants: 'No data',
        activePlants: 'No data',
        totalFaults: 'No data',
        averageRepairTime: 'No data',
        ongoingJobs: 'No data',
        faultsFixed: 'No data'
      },
      loaded: false
    };
    this.btnWidg=this.btnWidg.bind(this);
    this.btnGraph=this.btnGraph.bind(this);
  }

  componentWillMount() {
    var th = this;    
    DataService.getDashboardData().then((response) => {
      th.setState({
        data: {
          totalPlants: response.data.total_plants,
          activePlants: response.data.active_plants,
          totalFaults: response.data.total_faults,
          averageRepairTime: response.data.average_repair_time,
          ongoingJobs: response.data.ongoing_jobs,
          faultsFixed: response.data.faults_fixed
        },
        loaded: true
      })
    })
    .catch(function (error) {
      Helpers.handleHttpError(error);
    });
  }

  render() {
    /* --Dashbox loop--*/
    const titles = this.state.titles;
    const boxList = Object.keys(this.state.titles).map(function(key, index){ 
       let va = this.state.data[key];
       let ic = this.state.icons[key];
       let ti = this.state.titles[key];
       return(   
        <DashBox key={key} title={ti} value={String(va)} icon={ic} />   
      )
    },this);

    /*view*/
    const view=this.state.btnView;
    const graphView = <DashGraph />;
    
    if(this.state && this.state.loaded) {
      return (
          <div className="dashboard col-md-12 center-block" id="dashboard">
            <h1 className="text-center text-green">Data Widget</h1>
            
            <div className="col-md-1 dash-btn text-center">
              <DashButton icon="fa fa-info" action={this.btnWidg} item="1" active={this.state.btnView} />
              <DashButton icon="fa fa-signal" action={this.btnGraph} item="2" />
            </div>

            <div id="widgets" className="col-md-11 center-block">
              { view ? boxList : graphView }
            </div> 
          </div>
      )
    }
    return ("loading");
  }

  btnWidg(){
    this.setState({
      btnView:true
    })
    document.getElementById
  }

  btnGraph(){
    this.setState({
      btnView:false
    })
  }

}

// const rootElement = document.getElementById('dashboard');
// ReactDOM.render(<Dashboard data={rootElement.getAttribute('data-data') } socket = {dashboard_sock} />, rootElement);
