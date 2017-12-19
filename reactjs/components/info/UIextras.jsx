import React from 'react';
import SvgIcon from '../SvgIcon.jsx';

const UIextras = (props) => {
    return (
        <div className='col-md-4 col-sm-4 col-xs-10 ui-extras'>
            <div className='pill-icon' ><SvgIcon name={props.icon} size="50px" color="icon-white" type ='icon' /></div>
            <div className='col-md-6 col-sm-6 col-xs-6 pill-text' ><p>{props.title}</p></div>
            <div className='col-md-3 col-sm-3 col-xs-3 pill-text'> <h3>{props.info}</h3></div>
        </div>
    )
}
export default UIextras;