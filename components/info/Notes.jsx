import React from 'react';
import IconBtn from '../IconBtn.jsx';

const Notes = (props) => {
    return (
        <div className='row extra-info'>
            <h4>{props.title}</h4>
            <div className='col-md-10 col-sm-10 note-text'><p>{props.info}</p></div>
            {/* <IconBtn icon={props.icon} shape='round-yellow' size='20' action={props.buttons} bootstrap='col-md-2 col-sm-2' /> */}
            <IconBtn button={props.buttons.edit} />
        </div>
    )
}
export default Notes;