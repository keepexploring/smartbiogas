import React from 'react';



export class ModalContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          
        };
    }
    render() {
        // Render nothing if the "show" prop is false
        if(!this.props.show) {
          return null;
        }
    
    
    
        return (
          <div className="backdrop"  >
            <div className="modal" >
              {/* {this.props.children} */}
    
              <div className="footer">
                <button onClick={this.props.onClose}>
                  Close
                </button>
              </div>
            </div>
          </div>
        );
      }
}
