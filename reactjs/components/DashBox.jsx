import React from 'react';

const DashBox = (props) => {
    return (
        
        <div className="box col-md-4 col-sm-12">
          {/* <div className={`box_cont ${props.color}`}> */}
          <div className="box_cont ">
             <i className="fa "></i>
            <h1>{props.value}</h1>
            <p>{props.title}</p>
          </div>
         </div>

    )
}

export default DashBox;