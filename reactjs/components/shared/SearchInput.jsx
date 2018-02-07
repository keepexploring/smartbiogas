import React from 'react';
import SvgIcon from './SvgIcon.jsx';


const SearchInput = (props) => {
    const setSize = 18
    const btnstyle = {
        width: setSize * 2,
        height: setSize * 2
    }
    const barstyle={
        height:setSize*2
    }
    return (
        <div className="col-xs-6 search" style={barstyle}>
            <input type="text" id='searchInput' className="col-xs-9 search-term" placeholder="Search..." />
            <button  className="square-grey pull-right" style={btnstyle}  >
                <SvgIcon name='sbn-icon-search' size={setSize} color="icon-yellow" type='button' />
            </button>
        </div>
    )
}

export default SearchInput;
