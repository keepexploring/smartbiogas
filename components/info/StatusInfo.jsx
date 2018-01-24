import React from 'react';

import UIextras from './UIextras.jsx'
import UIstatus from './UIstatus.jsx'



function btnConstructor(pills) {
    if (pills.years_pill != null && pills.jobs_pill != null) {
        return (
            <div>
                <UIextras info={pills.years_pill} />
                <UIextras  info={pills.jobs_pill}/>
                <UIstatus info={pills.status_pill} />
            </div>)
    } else {
        return <UIstatus info={pills.status_pill}/>
    }
}

const StatusInfo = (props) => {
    let buttons = btnConstructor(props.info)
    return (
        <div className='row status-info'>
            <h4>{props.title}</h4>
            {buttons}
        </div>
    )
}
export default StatusInfo;