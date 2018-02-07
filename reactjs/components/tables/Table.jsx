import React from 'react';
import SvgIcon from '../shared/SvgIcon.jsx';

import ReactTable from "react-table";
import "react-table/react-table.css";

//Custom buttons
const next = <SvgIcon name='sbn-arrow-right' size='20' color="icon-yellow" type='button' />
const previous = <SvgIcon name='sbn-arrow-left' size='20' color="icon-yellow" type='button' />


function columnsConstructor(headers, rows) {
	const testColumn = Object.keys(headers).map(function (key, index) {
		return {
			Header: <span >{headers[key]}</span>,
			accessor: key,
			Cell: row => (cellConstructor(row.value, key))
		}
	})
	return testColumn
}

function cellConstructor(value, column) {
	//const classValue = 'column-'+ column
	let colorstyle = ''
	let textUpper = ''
	if (column == 'status') {
		colorstyle = value === 'active' ? '#63994e'
			: value === 'inactive' ? '#8fc7d0'
				: '#a8292f'
		textUpper = 'uppercase'
	} else {
		colorstyle = 'white'
		textUpper = 'none'
	}
	return <span className={column} style={{ color: colorstyle, textTransform: textUpper }} >{value}</span>
}

const requestData = (pageSize, page, filtered, data) => {
	return new Promise((resolve, reject) => {
		// You can retrieve your data however you want, in this case, we will just use some local data.
		let filteredData = data;

		// You can use the filters in your request, but you are responsible for applying them.
		if (filtered.length) {
			filteredData = filtered.reduce((filteredSoFar, nextFilter) => {
				return filteredSoFar.filter(row => {
					return (row[nextFilter.id] + "").includes(nextFilter.value);
				});
			}, filteredData);
		}

		// You must return an object containing the rows of the current page, and optionally the total pages number.
		const res = {
			rows: sortedData.slice(pageSize * page, pageSize * page + pageSize),
			pages: Math.ceil(filteredData.length / pageSize)
		};

		// Here we'll simulate a server response with 500ms of delay.
		setTimeout(() => resolve(res), 500);
	});
};

export class Table extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			data: [],
			columns: [],
			pageSize: 10,
			pages: null,
			loading: true
		};
		this.fetchData = this.fetchData.bind(this);
	}
	/*  -------Real data parse-------*/
	componentWillMount() {
		this.setState({
			data: this.props.data,
			columns: columnsConstructor(this.props.headers, this.props.data),
			pageSize: this.props.pageSize
		})
	}

	componentWillReceiveProps(props) {
		this.setState((prevState, props) => ({
			data: props.data,
			columns: columnsConstructor(props.headers, props.data),
			pageSize: props.pageSize
		}));
	}

	fetchData(state, instance) {
		// Whenever the table model changes, or the user sorts or changes pages, this method gets called and passed the current table model.
		// You can set the `loading` prop of the table to true to use the built-in one or show you're own loading bar if you want.
		this.setState({ loading: true });
		// Request the data however you want.  Here, we'll use our mocked service we created earlier
		requestData(
			state.pageSize,
			state.page,
			state.filtered,
			state.data
		).then(res => {
			// Now just get the rows of data to your React Table (and update anything else like total pages or loading)
			this.setState({
				data: res.rows,
				pages: res.pages,
				loading: false
			});
		});
	}


	/*handleData(data) {
			//receives messages from the connected websocket
			let parsed_data = JSON.parse(data);
			this.setState({
					techData: {
							techName: parsed_data.techName,
							techPhoneNumber: parsed_data.techPhoneNumber,
							techLocation: parsed_data.techLocation,
							techJobs: parsed_data.techLocation,
							status: parsed_data.techStatus
					}
			});
	}
	**/

	render() {
		const borders = "1px solid #6e6e6e";
		return (
			<ReactTable
				data={this.state.data}
				columns={this.state.columns}
				defaultPageSize={this.state.pageSize}
				className="-highlight"
				//filterable
				getTdProps={(state, rowInfo, column, instance) => {
					return {
						style: {
							borderRight: borders
						},
						onClick: (e, handleOriginal) => {
							
							if (this.props && this.props.selectRow) {
								this.props.selectRow(rowInfo);
							}


							// IMPORTANT! React-Table uses onClick internally to trigger
							// events like expanding SubComponents and pivots.
							// By default a custom 'onClick' handler will override this functionality.
							// If you want to fire the original onClick handler, call the
							// 'handleOriginal' function.
							if (handleOriginal) {
								// handleOriginal()
							}
						}
					}
				}}
				getPaginationProps={(components) => {
					return {
						nextText: next,
						previousText: previous
					}
				}}
				getTrProps={() => {
					return {
						style: {
							borderBottom: borders,
							cursor: 'pointer'
						}
					}
				}}
			/>
		)
	}
}
