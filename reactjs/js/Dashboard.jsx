import React from 'react';
import ReactDOM from 'react-dom';
import base from '../css/base.scss';

import DashBox from '../components/DashBox.jsx';
import DashGraph from '../components/DashGraph.jsx';
import IconButton from '../components/IconButton.jsx';


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
      values: ["-", "-", "-", "-", "-"],
      titles: [
        "No. Plants",
        "No. Active Plants",
        "Total Faults",
        "Average Repair Time (Days)",
        "Ongoing Jobs",
        "Faults fixed"
      ],
      icons:[
        "sbn-icon-leaf",
        "sbn-icon-tick",
        "sbn-icon-alert",
        "sbn-icon-dial",
        "sbn-icon-case",
        "sbn-icon-technician"
      ],
      btnView: true
    };
    this.btnWidg=this.btnWidg.bind(this);
    this.btnGraph=this.btnGraph.bind(this);
  }
  componentDidMount() {
    /**
  * Entrty point of data
  * Currently from JS object
  * Parse data thought API, RSS, websocket or any other alternative
  */
    const d = { testData };
    const values = Object.keys(d.testData).map(function (item, index) {
      return d.testData[item]
    });
    this.componentWillReceiveProps(values);
  }
  componentWillReceiveProps(data) {
    this.setState({
      values: data
    });
  }
  componentDidUpdate() {

  }
  render() {
    /* --Dashbox loop--*/
    const boxes = this.state.titles;
    const text = this.state.values;
    const icon = this.state.icons;
    const boxList = boxes.map(function (item, index) {
      let v = text[index];
      let ic = icon[index]
      return <DashBox title={item.toString()} value={v} icon={ic} />
    });
    /*view*/
    const view=this.state.btnView;
    const graphView = <DashGraph />;
    
    return (
      
        <div className="dashboard col-md-12 center-block" id="dashboard">
          <h1 className="text-center text-green">Data Widget </h1>
          <div className="col-md-1 dash-btn text-center">
            <IconButton icon="fa fa-info" action={this.btnWidg} key="1" active={this.state.btnView} />
            <IconButton icon="fa fa-signal" action={this.btnGraph} key="2" />
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
ReactDOM.render(<Dashboard />, rootElement);
