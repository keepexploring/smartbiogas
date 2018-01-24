import React from 'react';


// function statusColor(status){
//     let colorstyle = status === 'active' ? '#63994e'
//     : status === 'inactive' ? '#8fc7d0'
//         : '#a8292f'
//         return colorstyle
// }

const UIstatus = (props) => {
    const status_style={
        color: props.info.color,
        borderColor:props.info.color
    }
    return (
        <div className='col-md-4 ui-status' style={status_style} >
         {props.info.value}
        </div>
    )
}
export default UIstatus;