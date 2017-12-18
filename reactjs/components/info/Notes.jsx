import React from 'react';
import SvgIcon from '../SvgIcon.jsx';
//import BtnEdit from '../images/btn/SBNbuttonEdit.png';

const Notes = (props) => {
    return (
        <div className='extra-info'>
            <h4>{props.title}</h4>
            <div className='note-text'>
            <p>{props.info}</p> 
            <button className='round-yellow' ><SvgIcon name={props.icon} size="20px" color="icon-yellow" type='button' /></button>
             {/* <button><img src= {BtnEdit}/></button> */}
            </div>
        </div>
    )
}
export default Notes;