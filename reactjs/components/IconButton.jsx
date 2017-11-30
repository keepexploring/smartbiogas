import React from 'react';


const IconButton = (props) => {
    let activeClass=""
    if(props.active==true ){
        if(props.key==1){
            activeClass = "btn-icon ";
        }else{
            activeClass = "btn-icon active";
        } 
    }else{
        if(props.key==1){
            activeClass = "btn-icon active";
        }else{
            activeClass = "btn-icon ";
        } 
    }  
    return (
        <button className={activeClass} onClick={props.action} ><i className={props.icon} ></i></button>
    )
}

export default IconButton;