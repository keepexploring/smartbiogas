import React from 'react';
import ListRow from './ListRow.jsx';
import moment from 'moment';

const imgStyle = {
    height: '200px',
    background: 'grey'
}


const AddForm = (props) => {
    const rowList = Object.keys(props.headers).map(function (key, index) {
        let title = props.headers[key]
        let value = props.data[key];
        //let dateValid = moment(value, 'DD-MM-YYYY', true).isValid();
        let dateValid = key==='created_at'|| key==='overdue';
        
        if (dateValid) {
            return (
                <tr className='list-row' key={key}>
                    <td className='list-title col-sm-6' >{title}:</td>
                    <td className='list-value col-sm-6' ><input className='input-holder' type='date' name={key} value={value} onChange={props.onChange} /></td>
                </tr>
            )
        } else {
            return (
                <tr className='list-row' key={key}>
                    <td className='list-title col-sm-6' >{title}:</td>
                    <td className='list-value col-sm-6' ><input className='input-holder' type='text' name={key} value={value} onChange={props.onChange} /></td>
                </tr>
            )
        }
    }, this);

    return (
        <div className='table-form'>
            <table className="table">
                <tbody>
                    {rowList}
                </tbody>
            </table>
            <div className='list-row table-info' >
                <p>Additional Information: </p>
                <textarea name={'additional_info'} value={props.data.additional_info} onChange={props.onChange} />
            </div>
        </div>
    )
}
export default AddForm;