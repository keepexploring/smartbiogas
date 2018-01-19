import React from 'react';
import CloseBtn from '../CloseBtn.jsx';
import AddForm from '../tables/AddForm.jsx';


export class ModalPost extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      header: this.props.modalInfo.header,
      body: this.props.modalInfo.body,
      postData: [],
      closeModal: {
        click_action: this.props.onClose,
        target: '#modalpost'
      },
      submitModal:{
        click_action:this.handleChange,
        target:'#modalpost'
      }
    };
    this.handleChange = this.handleChange.bind(this);
  }
  componentWillMount() {
    this.componentWillReceiveProps()
  }
  componentWillReceiveProps(props) {
    this.setState({
      body: this.props.modalInfo.body
    });
  }

  handleChange(event) {
    const field = event.target.name;
    const postData = this.state.body.values;
    postData[field] = event.target.value;
    this.setState({
      postData: postData,
      //errors:dateErrors   
    });
  }
  /*POST values*/
  handleSubmit(event) {
    /**
  * POST data to database
  * Currently to state
  */
  console.log('pass')
    event.preventDefault();
    console.log(this.state.postData);
    console.log('EXAMPLE SERVER UPDATE REQUEST');
    //this.props.update(this.state.postData);

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
                <button type="button" className="close" data-dismiss="modal">&times;</button>
                <h4 className="modal-title">{this.state.header}</h4>
              </div>
              <div className="modal-body">
                <AddForm headers={this.state.body.headers} data={this.state.body.values} onChange={this.handleChange} />
              </div>
              <div className="modal-footer">
                <CloseBtn icon='sbn-icon-cross' shape='round-yellow' size='18' action={this.state.closeModal} bootstrap='col-md-2 col-sm-2 pull-right' />
                <CloseBtn icon='sbn-icon-tick' shape='round-yellow' size='18' action={this.state.submitModal} bootstrap='col-md-2 col-sm-2 pull-right' />

              </div>
            </div>
          </div>
        </div>
      );
    }
  }
}
