import React from 'react';
import SvgIcon from './SvgIcon.jsx';

const CloseBtn = (props) => {
    const btnstyle={
        width:props.size*2,
        height:props.size*2
    }
    return (
        <div className={props.bootstrap} >
            <button className={props.shape} style={btnstyle} onClick={props.action.click_action} data-dismiss="modal" data-target={props.action.target}><SvgIcon name={props.icon} size={props.size} color="icon-yellow" /></button>
        </div >
    )
}
export default CloseBtn;