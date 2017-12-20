import React from 'react';
import IconBtn from '../IconBtn.jsx';

function editEntry() {
    /**
     * Popup window to edit data
     */
    alert('Edit tech');
}

const Notes = (props) => {
    return (
        <div className='row extra-info'>
            <h4>{props.title}</h4>
            <div className='col-md-10 col-sm-10 note-text'><p>{props.info}</p></div>
            <IconBtn icon={props.icon} shape='round-yellow' size='20' action={editEntry} bootstrap='col-md-2 col-sm-2' />
        </div>
    )
}
export default Notes;