import React from 'react';
import SvgIcon from '../shared/SvgIcon.jsx';

const DashBox = (props) => {
 
    return (
        <div className="box col-md-3 col-sm-5"  >
            <div className="box_cont">
                <i className="box-icon" >
                   <SvgIcon name={props.icon} size="50px" color="icon-white" type='icon' />
                </i>
                <h1 className="text-white" >{props.value}</h1>
                <h4 className="text-white" >{props.title}</h4>
            </div>
        </div>

    )
}

export default DashBox;