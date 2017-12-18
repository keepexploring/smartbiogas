import React from 'react';
import ReactDOM from 'react-dom';
import Websocket from 'react-websocket';
import base from '../css/base.scss';

import DashBox from '../components/dashboard/DashBox.jsx';
import DashGraph from '../components/dashboard/DashGraph.jsx';
import IconButton from '../components/IconButton.jsx';


var dashboard_sock = 'ws://' + window.location.host + "/dashboard/"


export class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      titles: {
        plants:"No. Plants",
        active:"No. Active Plants",
        faults:"Total Faults",
        avtime:"Average Repair Time (Days)",
        jobs:"Ongoing Jobs",
        fixed:"Faults fixed"
      },
      icons:{
        plants:"sbn-icon-leaf",
        active:"sbn-icon-tick",
        faults:"sbn-icon-alert",
        avtime:"sbn-icon-dial",
        jobs:"sbn-icon-case",
        fixed:"sbn-icon-technician"
      },
      btnView: true,
      data:{
        plants: 'No data',
        active: 'No data',
        faults: 'No data',
        avtime: 'No data',
        jobs: 'No data',
        fixed: 'No data'
      }
    };
    this.btnWidg=this.btnWidg.bind(this);
    this.btnGraph=this.btnGraph.bind(this);
    this.sendSocketMessage = this.sendSocketMessage.bind(this);
  }

  componentWillMount() {
    //receives messages
    let parsed_data = JSON.parse(this.props.data);
    this.setState({
      data:{
        plants:parsed_data.plants, 
        active:parsed_data.active,
        faults:parsed_data.faults,
        avtime:parsed_data.avtime,
        jobs:parsed_data.jobs,
        fixed:parsed_data.fixed
      }
        })
}
handleData(data) {
  //receives messages from the connected websocket
  let parsed_data = JSON.parse(data);
  this.setState({
      data:{
        plants:parsed_data.plants, 
        active:parsed_data.active,
        faults:parsed_data.faults,
        avtime:parsed_data.avtime,
        jobs:parsed_data.jobs,
        fixed:parsed_data.fixed
      }
   });
}

sendSocketMessage(message){
  // sends message to channels back-end
 const socket = this.refs.socket
 socket.state.ws.send(JSON.stringify(message))
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
    
    return (
      
        <div className="dashboard col-md-12 center-block" id="dashboard">
        <Websocket ref="socket" url={this.props.socket} onMessage={this.handleData.bind(this)} reconnect={true}/>
          <h1 className="text-center text-green">Data Widget </h1>
          <div className="col-md-1 dash-btn text-center">
            <IconButton icon="fa fa-info" action={this.btnWidg} item="1" active={this.state.btnView} />
            <IconButton icon="fa fa-signal" action={this.btnGraph} item="2" />
          </div>
          <div id="widgets" className="col-md-11 center-block" >
         {view? boxList : graphView} 
          </div> 
        </div>
    )
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

const rootElement = document.getElementById('dashboard');
ReactDOM.render(<Dashboard data={rootElement.getAttribute('data-data') } socket = {dashboard_sock}/>, rootElement);
