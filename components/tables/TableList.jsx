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
        return <ListRow key={index} header={title} value={value} />
    }, this);

    let image = null;
    let tableClass;
    if (props.page == 'technicians') {
        image = <div className='col-md-3' style={imgStyle}>Test image</div>
        tableClass = 'col-md-9'
    } else {
        tableClass = 'col-md-12'
    }
    return (
        <div className='row table-list'>
            {image}
            <div className={tableClass}>
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