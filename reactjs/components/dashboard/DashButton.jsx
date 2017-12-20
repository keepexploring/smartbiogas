import React from 'react';


const DashButton = (props) => {
    let activeClass="btn-icon";
    if(props.active){
        activeClass=props.item==1?"btn-icon selected": 'btn-icon'    
    }
    if(props.active==false){
        activeClass=props.item==1?"btn-icon ": 'btn-icon selected'
    }
    
    return (
        <button className={activeClass} onClick={props.action} ><i className={props.icon} ></i></button>
    )
}

export default DashButton;