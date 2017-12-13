import React from 'react';
import { makeData } from "./TableUtilities.jsx"; //Test data constructor

import ReactTable from "react-table";
import "react-table/react-table.css";

const datafetch = makeData()
const data = datafetch.people

function columnsConstructor(headers,rows){
    const testColumn = headers.map(function(key,index){
        const sample= rows[0];
        const dataKeys = Object.keys(sample)
        const accessorValue = dataKeys[index+1]
        return {
            Header: key,
            accessor: accessorValue,
            Cell:row =>(cellConstructor(row.value))
        }
    })
    return testColumn
}

function cellConstructor(value){
    const classValue = 'column-'+ value
    const styling =value === 'active' ? '#63994e'
                    : value === 'inactive' ? '#8fc7d0'
                        : 'black'
    return <span className={classValue} style={{color:styling}} >{value}</span>
}

const Table = (props) => {
    const columns = columnsConstructor(props.headers,data)

    //     Cell: row => (
    //         <span className='status' style={{
    //             color: row.value === 'active' ? '#63994e'
    //                 : row.value === 'inactive' ? '#8fc7d0'
    //                     : '#a8292f'
    //         }}>
    //             {row.value}
    //         </span>)
        return (
            <ReactTable
                data={data}
                columns={columns}
                defaultPageSize={10}
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
                        nextText: '\&#7678;',

                    }
                }}
            />
            )
    }
    export default Table;