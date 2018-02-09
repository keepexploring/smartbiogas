import React from 'react';

import { TechniciansTable } from './TechniciansTable.jsx';
import * as TechniciansService from '../../services/TechniciansService';
import * as Helpers from '../../utils/Helpers';

export default class Technicians extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			technicians: [],
	};
	}

	componentWillMount() {
		TechniciansService.getTechnicians().then((response) => {
			this.setState({ technicians: response.data });
			this.render();
		})
		.catch(function (error) {
			Helpers.handleHttpError();
		});
	}

	render() {
		if (this.state && this.state.technicians.length > 0) {
			return (
				<TechniciansTable values={this.state.technicians} />
			);
		}
		return ("loading...");
	}
}
