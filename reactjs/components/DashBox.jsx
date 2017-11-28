import React from 'react';
import SvgIcon from './SvgIcon.jsx';

const DashBox = (props) => {
 
    return (
        <div className="box col-md-4 col-sm-12"  >
            <div className="box_cont">
                <i className="box-icon" key={props.key} >
                   <SvgIcon name={props.icon} size="50px" color="icon-white" />
                </i>
                <h1 className="text-white" >{props.value}</h1>
                <h4 className="text-white" >{props.title}</h4>
            </div>
        </div>

    )
}

export default DashBox;