import React from 'react';
import SvgIcon from './SvgIcon.jsx';

const SquareBtn = (props) => {
    const btnstyle={
        width:props.size*2,
        height:props.size*2
    }
    return (
        <div className={props.bootstrap} >
            <button className='square-grey' style={btnstyle} onClick={props.action} ><SvgIcon name={props.icon} size={props.size} color="icon-yellow" type='button' /></button>
        </div >
    )
}

export default SquareBtn;
