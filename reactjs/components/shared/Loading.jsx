import React from 'react';

export default class Loading extends React.Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	render() {
		return (
			<span className='loading text-white'>Loading...</span>
		)
	}
}
