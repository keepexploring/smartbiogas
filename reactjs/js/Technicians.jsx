import React from 'react';
import ReactDOM from 'react-dom';
import base from '../css/base.scss';
import { TechniciansTable } from '../components/containers/TechniciansTable.jsx';
import http from '../HttpClient';

export class Technicians extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			technicians: [],
		};
	}

	componentWillMount() {
		http.get('technicians')
			.then((response) => {
				this.setState({
					technicians: response.data
				});
				this.render();
			})
			.catch(function (error) {
				console.log(error);
			});
	}

	render() {
		if (this.state && this.state.technicians.length > 0) {
			return (
				<TechniciansTable values={this.state.technicians} />
			);
		}
		return ("loading");
	}
}

const rootElement = document.getElementById('technicians');
ReactDOM.render(<Technicians />, rootElement);
