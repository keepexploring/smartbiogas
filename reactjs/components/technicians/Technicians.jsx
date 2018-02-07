import React from 'react';
import ReactDOM from 'react-dom';
import base from '../../css/base.scss';

import { TechniciansTable } from './TechniciansTable.jsx';
import * as TechniciansService from '../../services/TechniciansService';
import * as Helpers from '../../utils/Helpers';

export class Technicians extends React.Component {
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
			Helpers.handleError();
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

const rootElement = document.getElementById('technicians');
ReactDOM.render(<Technicians />, rootElement);
