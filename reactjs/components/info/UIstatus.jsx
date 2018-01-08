import React from 'react';

//import BtnEdit from '../images/btn/SBNbuttonEdit.png';
function statusColor(status){
    let colorstyle = status === 'active' ? '#63994e'
    : status === 'inactive' ? '#8fc7d0'
        : '#a8292f'
        return colorstyle
}

const UIstatus = (props) => {
    const status_color = statusColor(props.title)
    const status_style={
        color: status_color,
        borderColor:status_color
    }
    return (
        <div className='col-md-4 ui-status' style={status_style} >
         {props.title}
        </div>
    )
}
export default UIstatus;