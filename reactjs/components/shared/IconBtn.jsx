import React from 'react';
import SvgIcon from './SvgIcon.jsx';

const IconBtn = (props) => {
    const btnstyle={
        width: props.size * 2,
        height: props.size * 2
    }
    return (
        <div className={props.bootstrap} >
            <button className={props.shape} style={btnstyle} onClick={props.action} ><SvgIcon name={props.icon} size={props.size} color="icon-yellow" /></button>
        </div >
    )
}

export default IconBtn;
