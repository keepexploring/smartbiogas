import React from 'react';
import SearchInput from '../SearchInput.jsx';
import SquareBtn from '../SquareBtn.jsx';

function btnConstructor(isTrue) {
    if (isTrue) {
        return (
            <div >
                <SquareBtn icon='sbn-icon-edit' size='20' action='test' bootstrap='col-md-2 col-sm-2' />
                <SquareBtn icon='sbn-icon-edit' size='20' action='test' bootstrap='col-md-2 col-sm-2' />
            </div>
        )
    }
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