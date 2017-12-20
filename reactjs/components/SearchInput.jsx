import React from 'react';
import SvgIcon from './SvgIcon.jsx';
import IconBtn from './IconBtn.jsx';

const SearchInput = (props) => {
    const setSize=18
    const btnstyle={
        width:setSize*2,
        height:setSize*2
    }
    const barstyle={
        height:setSize*2
    }
    return (
        <div className="col-md-6 col-sm-6 col-xm-6 search" style={barstyle}>
            <input type="text" className="search-term" placeholder="Search..." />
            <button type="submit" className="square-grey pull-right" style={btnstyle}  >
                <SvgIcon name='sbn-icon-search' size={setSize} color="icon-yellow" type='button' />
            </button>
        </div>
    )
}
export default SearchInput;