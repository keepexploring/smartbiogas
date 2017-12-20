import React from 'react';
import SvgIcon from './SvgIcon.jsx';
import IconBtn from './IconBtn.jsx';

const SearchInput = (props) => {
    return (
        <div className="col-md-6 search">
            <input type="text" className="searchTerm" placeholder="Search..." />
            <button type="submit" className="square-grey">
            <SvgIcon name='' size='20' color="icon-yellow" type='button' />
                <i className="fa fa-search " />
            </button>
        </div>
    )
}
export default SearchInput;