import React from 'react';

const ListRow = (props) => {
    return (
        <tr className='list-row'>
            <td className='col-md-6' >{props.header}</td>
            <td className='list-value col-md-6' >{props.value}</td>
        </tr>

    )
}
export default ListRow;
