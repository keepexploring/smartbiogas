import React from 'react';
import SvgIcon from '../SvgIcon.jsx';

import ReactTable from "react-table";
import "react-table/react-table.css";


const next=<SvgIcon name='sbn-arrow-right' size='20' color="icon-yellow" type='button'/>
const previous=<SvgIcon name='sbn-arrow-left' size='20' color="icon-yellow" type='button'/>


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

const Table = (props) => {
    const data = props.data
    const columns = columnsConstructor(props.headers, data)
    const borders = "1px solid #6e6e6e";
    return (
        <ReactTable
            data={data}
            columns={columns}
            defaultPageSize={props.pageSize}
            className="-highlight"
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
            getTrProps={(state, rowInfo, column) => {
                return {
                    style: {
                        borderBottom: borders,
                        cursor:'pointer'
                    }
                }
            }}
        />
    )
}
export default Table;