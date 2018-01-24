import React from 'react';
import SvgIcon from './SvgIcon.jsx';

const CloseBtn = (props) => {
    const btnstyle={
        width:props.button.size*2,
        height:props.button.size*2
    }
    return (
        <div className={props.button.bootstrap} >
            <button className={props.button.shape} style={btnstyle} onClick={props.button.click_action} data-dismiss="modal" data-target={props.button.target}><SvgIcon name={props.button.icon} size={props.button.size} color="icon-yellow" /></button>
        </div >
    )
}
export default CloseBtn;