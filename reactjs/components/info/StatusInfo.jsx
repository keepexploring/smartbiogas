import React from 'react';

import UIextras from './UIextras.jsx'
import UIstatus from './UIstatus.jsx'

const StatusInfo = (props) => {
    return (
        <div className='row status-info'>
            <h4>{props.title}</h4>
            <UIextras title='Jobs Completed' info={props.info.jobs_completed} icon='sbn-icon-case' />
            <UIextras title='Years Active' info={props.info.years_active} icon='sbn-icon-dial' />
           <UIstatus title={props.info.status} />
        </div>
    )
}
export default StatusInfo;