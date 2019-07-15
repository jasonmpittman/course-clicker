// css style to align text to the center of it's container
var Align = {
    textAlign: 'center',
    fontFamily: 'EB Garamond'
  };
  
  var StudentAttendanceForm = React.createClass({
  
    getInitialState: function(){
      // set initial state of form inputs
      return {title: '', option: '', options: []}
    },
  
    handleTitleChange: function(e){
      //change title as the user types
      this.setState({title: e.target.value});
    },
  
    handleOptionChange: function(e){
      this.setState({option: e.target.value});
    },
  
    handleOptionAdd: function(e){
      //update poll options and reset options to an empty string
      this.setState({
      options: this.state.options.concat({name: this.state.option}),
      option: ''
      });
    },
  
    handleSubmit: function(e){
      //TODO handle form submit
      e.preventDefault();
    },
  
    render: function(){
      return (
      <div>
       <form id="attendance_form" className="form-signin" onSubmit={this.handleSubmit}>
          <h2 className="form-signin-heading" style={Align}>Submit Attendance</h2>
  
          <div className="form-group has-success">
            <label htmlFor="option" className="sr-only">Option</label>
            <input type="text" id="option" name="option" className="form-control" placeholder="Enter keyword here" onChange={this.handleOptionChange}
            value={this.state.option ? this.state.option: ''} required autoFocus />
          </div>
  
          <div className="row form-group">
            <button className="btn btn-lg btn-success btn-block" type="submit">I'm Here!</button>
          </div>
          <br />
        </form>
      </div>
      );
    }
  });
    
  ReactDOM.render(
    <div>
      <StudentAttendanceForm />
    </div>,
    document.getElementById('form_container')
  );