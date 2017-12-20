import React from 'react';
import SearchInput from '../SearchInput.jsx';
import IconBtn from '../IconBtn.jsx';

function btnConstructor(isTrue) {
    if (isTrue) {
        return (
            <div className='col-md-6 col-sm-6 ' >
                <IconBtn icon='sbn-icon-edit' shape='square-grey' size='20' action={addEntry} bootstrap='col-md-2 col-sm-2 pull-right' />
                <IconBtn icon='sbn-icon-edit' shape='square-grey' size='20' action={addEntry} bootstrap='col-md-2 col-sm-2 pull-right' />
            </div>
        )
    }
}
function addEntry() {
    /**
     * Popup window to edit data
     */
    alert('Addtech');
}

const TopBar = (props) => {
    const buttons = btnConstructor(props.btnExtra)

    return (
        <div className="row top-bar">
            <SearchInput />
            {buttons}
        </div>
    )
}
export default TopBar;