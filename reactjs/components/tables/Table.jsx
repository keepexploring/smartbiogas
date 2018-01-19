import React from 'react';
import SvgIcon from '../SvgIcon.jsx';

import ReactTable from "react-table";
import "react-table/react-table.css";

//Custom buttons
const next = <SvgIcon name='sbn-arrow-right' size='20' color="icon-yellow" type='button' />
const previous = <SvgIcon name='sbn-arrow-left' size='20' color="icon-yellow" type='button' />

function cellConstructor(value, column, options) {
    let colorstyle = '',
        textUpper = '',
        colorValue = '';
    if (options) {
        colorValue = options[value];
        //console.log(options[value])
    }

    if (column == 'status' || column == 'fault_status') {
        colorstyle = colorValue;
        textUpper = 'uppercase';
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
            loading: true,
            statusOptions: this.props.data.statusOptions
        };
        this.fetchData = this.fetchData.bind(this);
        this.columnsConstructor = this.columnsConstructor.bind(this);
        //this.cellConstructor=this.cellConstructor.bind(this);        
    }
    /*  -------Real data parse-------*/
    componentWillMount() {
        let table = this.props.data;
        this.setState({
            data: table.values,
            columns: this.columnsConstructor(table.headers, table.values),
            pageSize: table.pageSize
        })
    }
    columnsConstructor(headers, rows) {
        const options = this.state.statusOptions;
        const testColumn = Object.keys(headers).map(function (key, index) {
            return {
                Header: <span >{headers[key]}</span>,
                accessor: key,
                Cell: row => (cellConstructor(row.value, key, options))
            }
        })
        return testColumn
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
                            console.log('id:', rowInfo.original.id)

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
