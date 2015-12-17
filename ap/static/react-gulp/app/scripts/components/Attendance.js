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
    //console.log('render event', this.props.event.attributes.start);
    var ev = this.props.event;

    console.log("ev", ev);

    var rolls = this.props.rolls;
    console.log("rolls!", rolls);
    var i = 0;
    while (i < rolls.length) {
      if (rolls[i].event == ev.id) {
        console.log("roll", rolls[i]);
        break;
      }
      i++;
    }

    console.log("roll", rolls[i]);
    var roll = rolls[i]

    var status = roll ? ATTENDANCE_STATUS_LOOKUP[roll['status']] : '';
    var todayClass = (ev.id === 'TODAY') ? 'today-marker' : '';

    var slips = this.props.slips;
    var i = 0;
    while (i < slips.length) {
      if (slips[i].events[0] == ev.id) { //this is broken!!!!
        break;
      }
      i++;
    }

    var leaveslip = slips[i]
    var slipStatus = leaveslip ? leaveslip['status'] : '';
    var classes = joinValidClasses(['schedule-event', status, SLIP_STATUS_LOOKUP[slipStatus], todayClass]); //ev['selected']
    var classes = '';
    // ev['rolls').at(ev['rolls').length - 1)['roll')
    var divStyle = {
      top: moment.duration(moment(ev['start']).format('H:m')).subtract(6, 'hours').asMinutes()/2,
      height: moment(ev['end']).diff(moment(ev['start']), 'minutes')/2,
      position: 'relative',
      border: '1px solid black',
    };
    //data-roll={ev['roll_id']}
    return(
      <div className={classes} onClick={this.toggleEvent} style={divStyle} data-id={ev['id']} data-roll={roll['id']}>
        {ev['code']}
        <div className="slip-event-status">{SLIP_STATUS_LOOKUP[slipStatus]}</div>
      </div>
    );
  }
});

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

var Leaveslip = React.createClass({
  getInitialState:function(){
      return {
        type: '',
        comments: '',
        description: '',
        texted: false,
        informed: false
      }
  },
  render: function() {
    var slip = this.props.slip,
        comments = slip['comments'],
        comments = (comments && comments !== '') ? comments : (<i>No Comments</i>),
        description = slip['description'],
        description = (description && description !== '') ? description : (<i>No Description</i>),
        status = SLIP_STATUS_LOOKUP[slip['status']],
        titleClasses = joinValidClasses(['list-group-item active', status]);
    return (
      <div className="leaveslip-container">
        <div className="list-group">
          <a href="#" className={titleClasses}>
            {slip['type']}
            <span className="badge">{status}</span>
          </a>
          <div className="list-group-item">{description}</div>
          <div className="list-group-item">{comments}</div>
        </div>
      </div>
    );
  }
});

var Leaveslips = React.createClass({
  render: function() {
    var selectedSlips = this.props.selectedSlips,
        slips = [],
        i, _len;

    for (i = 0, _len = this.props.selectedSlips.length; i < _len; i++) {
      slips.push(<Leaveslip slip={selectedSlips[i]} />);
    }

    if (slips.length === 0) {
      slips = (
        <div>
          <i>No event(s) with leaveslip(s) selected</i>
          <div className="form-group center-padded">
            <button className="btn btn-primary"><span className="glyphicon glyphicon-pencil"></span> Write New Leaveslip</button>
          </div>
        </div>
      );
    }

    console.log('selected slips', selectedSlips);
    return (
      <div className="panel panel-default" id="submit-leaveslip">
        <div className="panel-heading">
          <h3 className="panel-title" id="event-title">Leave Slip(s)</h3>
        </div>
        <div className="panel-body event-info leaveslip-info">
          {slips}
        </div>
      </div>
    );
  }
});

var RollView = React.createClass({
  setRoll: function(ev) {
    console.log('setRoll', arguments, this);
    var btn = ev.target;
    var status = (btn.id.charAt(0)).toUpperCase();
    actions.setRollStatus(status);

    if (btn.id === 'present') {
      console.log('present');
    } else if (btn.id === 'absent') {
      console.log('absent');
    } else if (btn.id === 'tardy') {
      console.log('tardy');
    } else if (btn.id === 'uniform') {
      console.log('uniform');
    } else if (btn.id === 'left-class') {
      console.log('left-class');
    } else {
      console.log('not recognized button');
    }
  },
  render: function() {
    var disabled = _.size(this.props.selectedEvents) <= 0,
        rollPane;

    if (!disabled) {
      rollPane = (
        <div>
          <button id="present" type="button" onClick={this.setRoll} className="btn btn-default btn-block" disabled={disabled}>Present</button>
          <button id="absent" type="button" onClick={this.setRoll} className="btn btn-danger btn-block" disabled={disabled}>Absent</button>
          <button id="tardy" type="button" onClick={this.setRoll} className="btn btn-warning btn-block" disabled={disabled}>Tardy</button>
          <button id="uniform" type="button" onClick={this.setRoll} className="btn btn-warning btn-block" disabled={disabled}>Uniform</button>
          <button id="left-class" type="button" onClick={this.setRoll} className="btn btn-warning btn-block" disabled={disabled}>Left Class</button>
        </div>
      );
    } else {
      rollPane = (
        <span className="info-message">Please select event(s) to record attendance</span>
      );
    }

    return (
      <div className="panel panel-default" id="submit-roll">
        <div className="panel-heading">
          <h3 className="panel-title" id="event-title">Submit Roll</h3>
        </div>
        <div className="panel-body event-info">
          {rollPane}
        </div>
      </div>
    );
  }
});


module.exports = Attendance;
// working on viewing the leaveslips *not working*

// var slipsBar = React.createClass({
//   render: function() {
//     var selectedSlips = this.props.selectedSlips,
//         slips = [],
//         i, _len;

//     for (i = 0, _len = this.props.selectedSlips.length; i < _len; i++) {
//       slips.push(<Leaveslip slip={selectedSlips[i]} />);
//     }

//     if (slips.length === 0) {
//       slips = (
//         <div>
//           <i>No event(s) with leaveslip(s) selected</i>
//           <div className="form-group center-padded">
//             <button className="btn btn-primary"><span className="glyphicon glyphicon-pencil"></span> Write New Leaveslip</button>
//           </div>
//         </div>
//       );
//     }
//     return (
//       <div className="panel panel-default leaveslip-container">
//         <div className="list-group">
//           <a href="#" className={titleClasses}>
//             {slip['type')}
//             <span className="badge">{status}</span>
//           </a>
//           <div className="list-group-item">{description}</div>
//           <div className="list-group-item">{comments}</div>
//         </div>
//       </div>
//     );
//   }
// });



























