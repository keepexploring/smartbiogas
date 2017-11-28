import React from 'react';
import ReactDOM from 'react-dom';
import base from '../css/base.scss';

import DashBox from '../components/DashBox.jsx';

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
      ]
    };
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
    const boxList = boxes.map(function (item, index) {
      let v = text[index];
      return <DashBox title={item.toString()} value={v} />
    });

    return (

        <div className="dashboard col-md-12" id="dashboard">
          <h1 className="text-center">Data Widget </h1>
          <div id="widgets"className="" >
          {boxList}
          </div>
        </div>


    )
  }
}

const rootElement = document.getElementById('app');
ReactDOM.render(<Dashboard />, document.getElementById('app'));
