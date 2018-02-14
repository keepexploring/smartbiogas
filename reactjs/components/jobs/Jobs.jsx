import React from 'react';

export default class Jobs extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
	}
  render() {
    console.log(this.props.location);
		return(
      <h1>Jobs</h1>
    );
  }
}