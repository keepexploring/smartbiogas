import React from 'react';

import ListRow from './ListRow.jsx'

const imgStyle = {
    height: '200px',
    background: 'grey'
}

const TableList = (props) => {
    const rowList = Object.keys(props.headers).map(function (key, index) {
        let title = props.headers[key]
        let value = props.data[key];
        return (
            <ListRow key={index} header={title} value={value} />
        )
    }, this);
    return (
        <div className='table-list'>
            <div className='col-md-3' style={imgStyle}>
                Test image
            </div>
            <div className='col-md-9'>
                <table className="table">
                    <tbody>
                        {rowList}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
export default TableList;