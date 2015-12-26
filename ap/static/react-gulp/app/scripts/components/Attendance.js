var attendanceStore = require("../stores/attendanceStore");
var actions = require("../actions");

// rendered by react-gulp/app/scripts/app.js
var Attendance = React.createClass({
  mixins: [
    Reflux.connect(attendanceStore)
  ],
  render: function() {
    console.log('render attendance');
    return (
    <div>
      <div>
        <Trainee
          trainee={this.state.trainee}
        />
        <WeekBar
          date={this.state.date}
        />
        <hr />
        <div className="row">
          <DaysRow date={this.state.date} />
        </div>
        <div className="row">
          <TimesColumn />
          <EventGrid
            events={this.state.events}
            rolls={this.state.rolls}
            slips={this.state.slips}
            date={this.state.date}
          />
          <div className="col-md-4 action-col">
            <RollView
              selectedEvents={this.state.selectedEvents}
              showLeaveSlip={this.state.showLeaveSlip}
            />
          </div>
        </div>
      </div>
      <hr />
    </div>
    );
  }
});

var ATTENDANCE_STATUS_LOOKUP = {
  P: 'present',
  A: 'absent',
  T: 'tardy',
  U: 'uniform',
  L: 'left-class'
};

var SLIP_STATUS_LOOKUP = {
  'A': 'approved',
  'P': 'pending',
  'F': 'fellowship',
  'D': 'denied',
  'S': 'approved'
};

var joinValidClasses = function(classes) {
  return _.compact(classes).join(' ');
};

var Trainee = React.createClass({
  render: function() {
    var name = this.props.trainee.name;
    return (
      <div>
        <h2>{name}&#39;s Schedule</h2>
      </div>
    );
  }
});

var WeekBar = React.createClass({
  render: function() {
    var startdate = this.props.date.weekday(0).format('M/D/YY');
    var enddate = this.props.date.weekday(6).format('M/D/YY');
    return (
      <div className="btn-toolbar" role="toolbar">
        <div className="controls btn-group">
          <button className="btn btn-info"><span className="glyphicon glyphicon-calendar"></span></button>
        </div>
        <div className="controls btn-group">
          <button className="btn btn-default clndr-previous-button" onClick={actions.prevWeek}>Prev</button>
          <div className="daterange btn btn-default disabled">
            {startdate} to {enddate}
          </div>
          <button className="btn btn-default clndr-next-button" onClick={actions.nextWeek}>Next</button>
        </div>
      </div>
    );
  }
});

var DaysRow = React.createClass({
  render: function() {
    var days = [];
    for(var i = 0; i < 7; i++) {
      var name = this.props.date.day(i).format('ddd');
      var num = this.props.date.day(i).format('M/D');
      var isToday = this.props.date.day(i).isSame(moment(), 'day');
      var today = isToday ? 'today' : '';
      var classes = joinValidClasses(['schedule-header', today]);
      days.push(
        <div className="col-md-1 no-padding" key={i}>
          <div className={classes}>
            {name} <br />
            {num}
          </div>
        </div>
      );
    }
    return (
      <div>
        <div className="col-md-1">
          <div className="col-md-1 no-padding">
            <div className="schedule-header dead-space"></div>
          </div>
        </div>
        {days}
      </div>
    );
  }
});


var EventView = React.createClass({
  toggleEvent: function(ev) {
    actions.toggleEvent(this.props.event);
  },
  render: function() {
    var ev = this.props.event;
    var slips = this.props.slips;
    console.log("Event", ev);
    console.log("Rolls", this.props.rolls)
    console.log("Slips", slips);

    //creates box on schedule according to the time
    var divStyle = {
      top: moment.duration(moment(ev['start']).format('H:m')).subtract(6, 'hours').asMinutes()/2,
      height: moment(ev['end']).diff(moment(ev['start']), 'minutes')/2,
      position: 'relative',
      border: '1px solid black',
    };
    //writes name of event on calendar, selects event on click.
    return(
      <div onClick={this.toggleEvent} style={divStyle}>{ev.name}</div>
    );
  }
});

//creates the calendar
var EventGrid = React.createClass({
  render: function() {
    var cols = [],
        weekStart = moment(this.props.date).startOf('week'),
        weekEnd = moment(this.props.date).endOf('week'),
        now = moment();
    //get events only from the state's week
    var week_events = _.filter(this.props.events, function(ev) {
        return (weekStart < moment(ev['start']) && weekEnd > moment(ev['end']));
    }, this);

    // If today is within current week, add the event marker
    // if (weekStart < now && weekEnd > now) {
    //   var todayEventMarker = new Event({
    //     id: 'TODAY',
    //     selected: '',
    //     start: moment(),
    //     end: moment()
    //   });

    //   week_events.push(todayEventMarker);
    // }
    
    console.log(week_events, this.props.events.models);

    for(var i = 0; i < 7; i++) {
      //get events for one day
      var day_events = _.filter(week_events, function(ev) {
        return moment(ev['start']).weekday() === i; // this == i
      });

      var day_col = [];
      day_events.forEach(function(event) { // we should double check or make sure that day_events is an ordered array by start time otherwise this will break
        day_col.push(<EventView event={event} slips={this.props.slips} rolls={this.props.rolls} selectEvent={this.props.selectEvent} key={event.id} />);
      }, this);

      var isToday = this.props.date.day(i).isSame(now, 'day');
      var today = isToday ? 'today' : '';
      var classes = joinValidClasses(['day event-col col-md-1 no-padding', today]);
      cols.push(<div key={i} className={classes}>{day_col}</div>);
    }
    return (
      <div>
        {cols}
      </div>
    );
  }
});


var Time = React.createClass({
  render: function() {
    var hour = moment().hour(this.props.hour).format('h A');
    return(
      <div className="hour">
        <div className="hour-text">{hour}</div>
      </div>
    );
  }
});

var TimesColumn = React.createClass({
  render: function() {
    var times = [];
    for(var i = 6; i < 24; i++) {
      times.push(<Time hour={i} key={i} />);
    }
    return (
      <div className="col-md-1 timebar">
        {times}
      </div>
    );
  }
});

//roll view contains sessions selected, submit roll, and leave slip 
var RollView = React.createClass({
  setRoll: function(ev) {
    var btn = ev.target;
    var status = btn.id;
    actions.setRollStatus(status);
  },
  toggleEvent: function(ev) {
    var key = ev.target.id;
    actions.toggleEvent(this.props.selectedEvents[key]);
  },
  toggleLeaveSlip: function(ev) {
    actions.toggleLeaveSlip();
  },
  disableLeaveSlip: function() {
    actions.disableLeaveSlip();
  },
  setLeaveSlip: function(ev) {
    console.log('setLeaveSlip', arguments, this);
    var btn = ev.target;
    var reason = btn.id;
    console.log('reason',reason)
    actions.setLeaveSlipReason(reason);
  },
  submitLeaveSlip: function() {
    actions.submitLeaveSlip();
  },
  render: function() {
    var disabled = _.size(this.props.selectedEvents) <= 0,
        rollPane, rollHeading, rollStyle, sessionsSelectedPane, slipStyle;
    
    //disabled is whether there are events selected or not.
    if (!disabled) {
      //sessions pane
      var keys = [];
      for(var k in this.props.selectedEvents) {
        keys.push(<button id={k} type="button" key={k} onClick={this.toggleEvent} className="btn btn-default">{this.props.selectedEvents[k].name}</button>);
      }
      sessionsSelectedPane = (
        <div>
          {keys}
        </div>
      );

      //roll pane
      rollHeading = (
        <div>
          <h3 className="panel-title" id="event-title">Submit Roll</h3>
        </div>
      );
      rollStyle = {display: 'block'};
      rollPane = (
        <div>
          <button id="present" type="button" onClick={this.setRoll} className="btn btn-info btn-block">Present</button>
          <button id="absent" type="button" onClick={this.setRoll} className="btn btn-info btn-block">Absent</button>
          <button id="tardy" type="button" onClick={this.setRoll} className="btn btn-info btn-block">Tardy</button>
          <button id="uniform" type="button" onClick={this.setRoll} className="btn btn-info btn-block">Uniform</button>
          <button id="left-class" type="button" onClick={this.setRoll} className="btn btn-info btn-block">Left Class</button>
          <button id="submitleaveslip" type="button" onClick={this.toggleLeaveSlip} className="btn btn-link">Submit Leaveslip</button>
        </div>
      );
    } else {
      sessionsSelectedPane = (
        <span className="info-message">Please select event(s) to record attendance</span>
      );
      rollHeading = (
        <div
          style = {{display: 'none'}}>
        </div>
      )
      rollStyle = {display: 'none'};
      rollPane = (
        <div
          style = {{display: 'none'}}>
        </div>
      )
      if (this.props.showLeaveSlip) {
        this.disableLeaveSlip();
      }
    }
    
    //leave slip pane
    var leaveSlipPane = (
      <div className="panel-heading">
        <h3 className="panel-title" id="event-title" style={{fontSize: '20px'}}>Reason </h3>
        <button id="sick" type="button" onClick={this.setLeaveSlip} className="btn btn-info btn-primary custom">Sick</button>
        <button id="service" type="button" onClick={this.setLeaveSlip} className="btn btn-info btn-primary custom">Service</button>
        <button id="night out" type="button" onClick={this.setLeaveSlip} className="btn btn-info btn-primary custom">Night Out</button>
        <button id="meal out" type="button" onClick={this.setLeaveSlip} className="btn btn-info btn-primary custom">Meal Out</button>
        <button id="fellowship" type="button" onClick={this.setLeaveSlip} className="btn btn-info btn-primary custom">Fellowship</button>
        <h3 className="panel-title" id="event-title" style={{fontSize: '20px'}}>Comments </h3>
        <div class="form-group">
          <textarea class="form-control" rows="5" id="comment" style={{boxSizing: 'borderBox', width: '310px', height: '100px'}}></textarea>
          <button id="submit" type="button" onClick={this.submitLeaveSlip} className="btn btn-warning btn-primary custom">Submit</button>
        </div>
      </div>
    );
    if (!this.props.showLeaveSlip){
      slipStyle = {display: 'none'};
    } else {
      slipStyle = {display: 'block'};
    }

    return (
      <div className="panel panel-default">
        <div className="panel-heading">
          {<h3 className="panel-title" id="event-title">Sessions Selected</h3>}
        </div>
        <div className="panel-body event-info">
          {sessionsSelectedPane}
        </div>
        
        <div className="panel-heading" style={rollStyle}>
          {rollHeading}
        </div>
        <div className="panel-body event-info" style={rollStyle}>
          {rollPane}
        </div>
        <div className="panel-heading" style={slipStyle}>
          <h3 className="panel-title" id="event-title">Submit Leave Slip </h3>
        </div>
        <div className="panel-body event-info" style = {slipStyle}>
          {leaveSlipPane}
        </div>
      </div>
    );
  }
});

module.exports = Attendance;



























