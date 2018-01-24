import React from 'react';
import SearchInput from '../SearchInput.jsx';
import IconBtn from '../IconBtn.jsx';

// function btnConstructor(isTrue,buttons) {
//     if (isTrue) {
//         return (
//             <div className='col-md-6 col-sm-6 col-xs-6' >
//                 <IconBtn icon='sbn-icon-subtrack' shape='square-grey' size='18' action={buttons.remove} bootstrap='col-md-2 col-sm-2 pull-right' />
//                 <IconBtn icon='sbn-icon-add' shape='square-grey' size='18' action={buttons.add} bootstrap='col-md-2 col-sm-2 pull-right' />
//             </div>
//         )
//     }
// }
function btnConstructor(buttons) {
    let printBtn = Object.keys(buttons).map(function (key, index) {
        if (buttons[key]) {
            return <IconBtn key={key} button={buttons[key]} />
        }
    });
    return printBtn;
}

const TopBar = (props) => {
    //const buttons = btnConstructor(props.btnExtra,props.buttons);
    const buttons = btnConstructor(props.buttons)
    return (
        <div className="col-md-12 col-sm-12 col-xs-12 top-bar">
            <SearchInput />
            <div className="col-xs-6" >
                {buttons}
            </div>
        </div>
    )
}
export default TopBar;