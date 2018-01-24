import React from 'react';
import CloseBtn from '../CloseBtn.jsx';
import AddForm from '../tables/AddForm.jsx';


export class ModalPost extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      header: this.props.header,
      body: '',
      postData: null,
      buttons: {
        close: {
          click_action: this.props.onClose,
          target: '#modalpost',
          icon: 'sbn-icon-cross',
          shape: 'round-form',
          size: '25',
          bootstrap: 'col-md-2 col-sm-2 pull-right'
        },
        submit: {
          click_action: null,
          target: '#modalpost',
          icon: 'sbn-icon-tick',
          shape: 'round-form',
          size: '25',
          bootstrap: 'col-md-2 col-sm-2 pull-left'
        }
      }
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  componentWillMount() {
    this.componentWillReceiveProps();

  }
  componentWillReceiveProps(props) {
    this.setState({
      body: this.props.modalInfo.body,
      postData: this.props.modalInfo.body.values,
      buttons: { submit: { click_action: this.handleSubmit } }
    });
  }

  handleChange(event) {
    const field = event.target.name;
    const tempData = this.state.body.values;
    tempData[field] = event.target.value;
    this.setState({
      postData: tempData,
      //errors:dateErrors   
    });
  }
  /*POST values*/
  handleSubmit(event) {
    /**
  * POST data to database
  * Currently to state
  */
    event.preventDefault();
    console.log(this.state.postData);
    console.log('EXAMPLE SERVER UPDATE REQUEST');
    this.props.modalInfo.update(this.state.postData);
    this.setState({
      postData: null,
    });
  }

  render() {
    // Render nothing if the "show" prop is false
    if (!this.props.show) {
      return null;
    } else {
      return (
        <div className="modal fade" role="dialog" id='modalpost' >
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <button type="button" className="close" onClick={this.state.buttons.close.click_action} data-dismiss="modal">&times;</button>
                <h4 className="modal-title">{this.state.header}</h4>
              </div>
              <div className="modal-body">
                <AddForm headers={this.state.body.headers} data={this.state.body.values} onChange={this.handleChange} />
              </div>
              <div className="modal-footer">
                <CloseBtn button={this.state.buttons.close} />
                <CloseBtn button={this.state.buttons.submit} />
              </div>
            </div>
          </div>
        </div>
      );
    }
  }
}
