import React from 'react';

import UIextras from './UIextras.jsx'
import UIstatus from './UIstatus.jsx'

function btnConstructor(t) {
    console.log(t.page)
    switch (t.page) {
        case 'technicians':
            return (
                <div>
                    <UIextras title='Jobs Completed' info={t.info.techJobsCompleted} icon='sbn-icon-case' />
                    <UIextras title='Years Active' info={t.info.techYearsActive} icon='sbn-icon-dial' />
                    <UIstatus title={t.info.status} />
                </div>
            )
        case 'jobs':
            return  <UIstatus title={t.info.status} />
                
        // case 'error':
        //     return <Error text={text} />;
        default:
            return null;
    }
}

const StatusInfo = (props) => {
    let buttons = btnConstructor(props)
    // let extrabtn = function () {
    //     if (props.page == 'technicians') {
    //         return (
    //             <div>
    //                 <UIextras title='Jobs Completed' info={props.info.techJobsCompleted} icon='sbn-icon-case' />
    //                 <UIextras title='Years Active' info={props.info.techYearsActive} icon='sbn-icon-dial' />
    //                 <UIstatus title={props.info.status} />
    //             </div>
    //         )
    //     }else{
    //         return <UIstatus title={props.info.status} />
    //     }
    // }

    return (

        <div className='row status-info'>
            <h4>{props.title}</h4>
            {/* {extrabtn} */}

            {buttons}
        </div>
    )
}
export default StatusInfo;