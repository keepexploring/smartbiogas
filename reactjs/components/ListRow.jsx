import React from 'react';

const ListRow = (props) => {
    return (
        <tr className='list-row'>
            <td>{props.header}</td>
            <td>{props.value}</td>
        </tr>

    )
}
export default ListRow;