import React from 'react';
import SvgIcon from './SvgIcon.jsx';

const SearchInput = (props) => {
    return (
        <div className="col-md-6 search">
            <input type="text" className="searchTerm" placeholder="Search..." />
            <button type="submit" className="searchButton">
                <i className="fa fa-search" />
            </button>
        </div>
    )
}
export default SearchInput;