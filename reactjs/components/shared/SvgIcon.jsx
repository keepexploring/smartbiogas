import React from 'react';

const SvgIcon = (props) => {
    const xTag = "#" + props.name;
    const useClass = props.name + " " + props.color;
    return (
        <svg viewBox='0 0 210.27 210.27' width={props.size} height={props.size} >
            <use xlinkHref={xTag} className={useClass} ></use>
        </svg>
    )
}

export default SvgIcon;
