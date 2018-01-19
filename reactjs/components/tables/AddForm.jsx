import React from 'react';
import ListRow from './ListRow.jsx'

const imgStyle = {
    height: '200px',
    background: 'grey'
}

const AddForm = (props) => {
    const rowList = Object.keys(props.headers).map(function (key, index) {
        let title = props.headers[key]
        let value = props.data[key];
        return (
            <tr className='list-row' key={key}>
                <td className='col-md-6' >{title}</td>
                <td className='list-value col-md-6' ><input className='input-holder' type='text' name={key} value={value} onChange={props.onChange} /></td>
            </tr>
        )
    }, this);

    return (
        <div className='table-list'>
            <div className=''>
                <table className="table">
                    <tbody>
                        {rowList}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
export default AddForm;