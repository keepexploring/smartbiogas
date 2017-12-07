import React from 'react';
import ReactDOM from 'react-dom';
import Websocket from 'react-websocket';
import base from '../css/base.scss';

import DashBox from '../components/DashBox.jsx';
import DashGraph from '../components/DashGraph.jsx';
import IconButton from '../components/IconButton.jsx';


var dashboard_sock = 'ws://' + window.location.host + "/dashboard/"

const testData = {
  "plants": 407,
  "active": 396,
  "faults": 27,
  "avtime": 9.5,
  "jobs": 11,
  "fixed": 16
}


export class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      // values: ["-", "-", "-", "-", "-"],
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
        plants: 407,
        active: 396,
        faults: 27,
        avtime: 9.5,
        jobs: 11,
        fixed: 16
      }
    };
    this.btnWidg=this.btnWidg.bind(this);
    this.btnGraph=this.btnGraph.bind(this);
    // this.handleData=this.handleData.bind(this);
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
    console.log(this.props.data)
}
handleData(data) {
  //receives messages from the connected websocket
  console.log(data);
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
   console.log(this.state.data);
}

sendSocketMessage(message){
  // sends message to channels back-end
 const socket = this.refs.socket
 socket.state.ws.send(JSON.stringify(message))
}

  //componentDidMount() {
  //   /**
  // * Entrty point of data
  // * Currently from JS object
  // * Parse data thought API, RSS, websocket or any other alternative
  // */
  //   const d = { testData };
  //   const values = Object.keys(d.testData).map(function (item, index) {
  //     return d.testData[item]
  //   });
  //   this.componentWillReceiveProps(values);
  // }
  // componentWillReceiveProps(data) {
  //   this.setState({
  //     values: data
  //   });
  // }
  componentDidUpdate() {

  }
  render() {
    /* --Dashbox loop--*/
    const titles = this.state.titles;
    // const text = this.state.values;
   // const icons = this.state.icons;
    const boxList = Object.keys(this.state.titles).map(function(key, index){ 
       let va = this.state.data[key];
       let ic = this.state.icons[key];
       let ti = this.state.titles[key];
       console.log(va);
       return(
      <div>
        <DashBox title={'hello'}  title={ti} value={String(va)} icon={ic} />
        
      </div>
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
            <IconButton icon="fa fa-info" action={this.btnWidg} _item_="1" active={this.state.btnView} />
            <IconButton icon="fa fa-signal" action={this.btnGraph} _item_="2" />
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
