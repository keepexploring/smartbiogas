import React from 'react';

const SvgIcon = (props) => {
    const xTag = "#" + props.name;
    const useClass = props.name + " " + props.color;
    const viewbox = props.type === 'icon'?'0 0 210.27 210.27': '0 0 133.44 133.42'
    return (
        <svg viewBox={viewbox} width={props.size} height={props.size} >
            <use xlinkHref={xTag} className={useClass} ></use></svg>


    )
}

export default SvgIcon;