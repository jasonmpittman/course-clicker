// css style to align text to the center of it's container
var Align = {
    textAlign: 'center',
  };
  
  var StudentAttendanceForm = React.createClass({
    
    //don't need this
    getInitialState: function(){
      // set initial state of form inputs
      return {title: '', option: '', options: []}
    },
  
    handleCourseChange: function(e){
      //change title as the user types
      this.setState({course: e.target.value});
    },
  
    handleKeywordChange: function(e){
      this.setState({keyword: e.target.value});
    },
  
    //don't need this
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
            <label htmlFor="course" className="sr-only">Course</label>
            <input type="text" id="course" name="course" className="form-control" placeholder="Enter course code here" onChange={this.handleCourseChange}
            value={this.state.course ? this.state.course: ''} required autoFocus />
          </div>

          <div className="form-group has-success">
            <label htmlFor="keyword" className="sr-only">Keyword</label>
            <input type="text" id="keyword" name="keyword" className="form-control" placeholder="Enter keyword here" onChange={this.handleKeywordChange}
            value={this.state.keyword ? this.state.keyword: ''} required autoFocus />
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