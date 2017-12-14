import React from 'react';


import ReactTable from "react-table";
import "react-table/react-table.css";




function columnsConstructor(headers, rows) {
    const testColumn = Object.keys(headers).map(function (key, index) {
        return {
            Header: headers[key],
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

const Table = (props) => {
    const data = props.data
    const columns = columnsConstructor(props.headers, data)
    const borders = "1px solid #6e6e6e";
    console.log(columns)
    return (
        <ReactTable
            data={data}
            columns={columns}
            defaultPageSize={props.pageSize}
            className="-highlight"
            getTdProps={(state, rowInfo, column, instance) => {
                return {
                    onClick: (e, handleOriginal) => {
                        console.log('id:', rowInfo.original.id)

                        // IMPORTANT! React-Table uses onClick internally to trigger
                        // events like expanding SubComponents and pivots.
                        // By default a custom 'onClick' handler will override this functionality.
                        // If you want to fire the original onClick handler, call the
                        // 'handleOriginal' function.
                        if (handleOriginal) {
                            handleOriginal()
                        }
                    }
                }
            }}
            getPaginationProps={(components) => {
                //console.log(components);
                return {
                    nextText: '\U02C2',
                }
            }}
            getTrProps={(state, rowInfo, column) => {
                return {
                    style: {
                        borderBottom: borders
                    }
                }
            }}
            getTdProps={(state, rowInfo, column) => {
                return {
                    style: {
                        borderRight: borders
                    }
                }
            }}
        />
    )
}
export default Table;