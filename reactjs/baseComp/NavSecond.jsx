import React from 'react';
import userimg from '../images/prof_img.jpg';

export class NavSecond extends React.Component {
    render() {
        return (
         
        <div className="list-group collapse profile_box" id="profile_data">
            <nav id="mysidebarmenu" className="amazonmenu">
               <ul>
               <li><img src={userimg} alt="."/><b>Sunil Ku. Sahu</b></li>
               </ul>
             <ul>
               <li><a href="#">Messages</a></li>
                 <li><a href="#">Alerts</a></li>
                 <li><a href="#">Account Details</a></li>
                 <li><a href="#">Settings</a></li>
                 <li><a href="/logout">Log Out</a></li>
               </ul>
            </nav>
        </div>

        )
    }
}